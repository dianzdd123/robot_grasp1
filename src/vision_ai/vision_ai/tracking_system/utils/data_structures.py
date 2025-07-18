#!/usr/bin/env python3
"""
追踪系统数据结构
定义所有核心数据结构和类型
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from ..utils.config import TrackingState, TrackingMode

@dataclass
class TrackingTarget:
    """追踪目标数据结构"""
    object_id: str
    class_id: int
    class_name: str
    description: str
    reference_features: Dict[str, Any]
    
    # 可选的额外信息
    confidence: float = 0.0
    last_seen_time: float = 0.0
    detection_count: int = 0

@dataclass
class DetectionResult:
    """检测结果数据结构"""
    # 基本信息
    object_id: str
    class_id: int
    class_name: str
    confidence: float
    
    # 空间信息
    bounding_box: List[float]  # [x1, y1, x2, y2]
    centroid_2d: Tuple[float, float]  # (x, y) 像素坐标
    centroid_3d: Optional[Tuple[float, float, float]] = None  # (x, y, z) 世界坐标
    
    # 分割信息
    mask: Optional[np.ndarray] = None
    mask_area: float = 0.0
    
    # 特征信息
    features: Dict[str, Any] = field(default_factory=dict)
    
    # 匹配信息
    match_confidence: float = 0.0
    match_method: str = "unknown"
    
    # 时间戳
    timestamp: float = 0.0
    
    def get_bbox_center(self) -> Tuple[float, float]:
        """获取边界框中心"""
        if len(self.bounding_box) != 4:
            return (0.0, 0.0)
        x1, y1, x2, y2 = self.bounding_box
        return ((x1 + x2) / 2, (y1 + y2) / 2)
    
    def get_bbox_area(self) -> float:
        """获取边界框面积"""
        if len(self.bounding_box) != 4:
            return 0.0
        x1, y1, x2, y2 = self.bounding_box
        return (x2 - x1) * (y2 - y1)
    
    def is_valid(self) -> bool:
        """检查检测结果是否有效"""
        return (
            self.object_id and
            self.class_id >= 0 and
            self.confidence > 0 and
            len(self.bounding_box) == 4 and
            self.bounding_box[2] > self.bounding_box[0] and
            self.bounding_box[3] > self.bounding_box[1]
        )

@dataclass
class TrackingCommand:
    """追踪控制命令"""
    # 状态信息
    current_state: TrackingState
    target_state: TrackingState
    tracking_mode: TrackingMode
    
    # 目标位姿
    target_pose: Dict[str, Any]
    
    # 运动信息
    movement_type: str  # "proportional", "approach", "grasp", "return"
    distance_to_target: float
    yaw_adjustment: float
    
    # 夹爪控制
    gripper_command: Optional[Dict[str, Any]] = None
    
    # 执行参数
    speed: float = 60.0
    wait_for_completion: bool = True
    
    # 元数据
    command_id: str = ""
    timestamp: float = 0.0
    
    def is_valid(self) -> bool:
        """检查命令是否有效"""
        return (
            self.target_pose and
            'position' in self.target_pose and
            'orientation' in self.target_pose and
            self.speed > 0
        )

@dataclass
class MotionRecord:
    """运动记录"""
    # 时间信息
    timestamp: float
    duration: float = 0.0
    
    # 位姿信息
    from_pose: List[float]  # [x, y, z, roll, pitch, yaw]
    to_pose: List[float]
    
    # 运动信息
    command_type: str
    movement_type: str
    success: bool
    
    # 目标信息
    target_object_id: str = ""
    target_pixel_pos: Tuple[float, float] = (0.0, 0.0)
    distance_to_target: float = 0.0
    
    # 状态信息
    tracking_state: TrackingState = TrackingState.IDLE
    
    def get_distance_moved(self) -> float:
        """计算移动距离"""
        if len(self.from_pose) < 3 or len(self.to_pose) < 3:
            return 0.0
        
        dx = self.to_pose[0] - self.from_pose[0]
        dy = self.to_pose[1] - self.from_pose[1]
        dz = self.to_pose[2] - self.from_pose[2]
        
        return np.sqrt(dx*dx + dy*dy + dz*dz)

@dataclass
class FeatureMatch:
    """特征匹配结果"""
    target_id: str
    reference_id: str
    
    # 匹配分数
    overall_score: float
    class_score: float
    hu_moments_score: float
    color_histogram_score: float
    spatial_continuity_score: float
    
    # 匹配方法
    match_method: str
    
    # 置信度
    confidence: float
    
    # 调试信息
    debug_info: Dict[str, Any] = field(default_factory=dict)
    
    def is_good_match(self, threshold: float = 0.6) -> bool:
        """判断是否是好的匹配"""
        return self.overall_score >= threshold and self.confidence >= threshold

@dataclass
class TrackingStatus:
    """追踪状态信息"""
    # 基本状态
    current_state: TrackingState
    tracking_mode: TrackingMode
    target_id: str
    
    # 时间信息
    tracking_duration: float
    state_duration: float
    
    # 检测信息
    detection_count: int
    lost_frames: int
    last_detection_time: float
    
    # 目标信息
    distance_to_target: float
    yaw_error: float
    
    # 运动信息
    current_pose: List[float]
    target_pose: List[float]
    
    # 性能信息
    detection_fps: float
    tracking_fps: float
    
    # 错误信息
    error_count: int
    recovery_attempts: int
    
    # 特征匹配信息
    last_match_score: float
    match_method: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'current_state': self.current_state.value,
            'tracking_mode': self.tracking_mode.value,
            'target_id': self.target_id,
            'tracking_duration': self.tracking_duration,
            'state_duration': self.state_duration,
            'detection_count': self.detection_count,
            'lost_frames': self.lost_frames,
            'last_detection_time': self.last_detection_time,
            'distance_to_target': self.distance_to_target,
            'yaw_error': self.yaw_error,
            'current_pose': self.current_pose,
            'target_pose': self.target_pose,
            'detection_fps': self.detection_fps,
            'tracking_fps': self.tracking_fps,
            'error_count': self.error_count,
            'recovery_attempts': self.recovery_attempts,
            'last_match_score': self.last_match_score,
            'match_method': self.match_method
        }

@dataclass
class CameraFrame:
    """相机帧数据"""
    timestamp: float
    
    # 图像数据
    color_image: np.ndarray
    depth_image: Optional[np.ndarray] = None
    
    # 相机信息
    camera_info: Optional[Dict[str, Any]] = None
    
    # 图像质量
    blur_score: float = 0.0
    brightness_score: float = 0.0
    
    def is_valid(self) -> bool:
        """检查帧是否有效"""
        return (
            self.color_image is not None and
            self.color_image.size > 0 and
            len(self.color_image.shape) == 3 and
            self.color_image.shape[2] == 3
        )
    
    def get_image_shape(self) -> Tuple[int, int]:
        """获取图像尺寸"""
        if not self.is_valid():
            return (0, 0)
        return (self.color_image.shape[1], self.color_image.shape[0])  # (width, height)

@dataclass
class RecoveryAction:
    """回退动作"""
    action_type: str  # "return_to_pose", "search_waypoints", "rescan"
    
    # 目标位姿（用于return_to_pose）
    target_pose: Optional[List[float]] = None
    
    # 搜索路径（用于search_waypoints）
    waypoints: Optional[List[List[float]]] = None
    
    # 执行参数
    timeout: float = 30.0
    speed: float = 60.0
    
    # 元数据
    reason: str = ""
    attempt_count: int = 0
    
    def is_valid(self) -> bool:
        """检查回退动作是否有效"""
        if self.action_type == "return_to_pose":
            return self.target_pose is not None and len(self.target_pose) >= 6
        elif self.action_type == "search_waypoints":
            return self.waypoints is not None and len(self.waypoints) > 0
        elif self.action_type == "rescan":
            return True
        return False

# 工具函数
def create_detection_result(object_id: str, class_id: int, class_name: str, 
                          bbox: List[float], confidence: float = 1.0) -> DetectionResult:
    """创建检测结果的便捷函数"""
    centroid_2d = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
    
    return DetectionResult(
        object_id=object_id,
        class_id=class_id,
        class_name=class_name,
        confidence=confidence,
        bounding_box=bbox,
        centroid_2d=centroid_2d,
        timestamp=time.time()
    )

def create_tracking_command(state: TrackingState, target_pose: Dict[str, Any],
                          movement_type: str = "proportional") -> TrackingCommand:
    """创建追踪命令的便捷函数"""
    return TrackingCommand(
        current_state=state,
        target_state=state,
        tracking_mode=TrackingMode.FULL_MATCHING,
        target_pose=target_pose,
        movement_type=movement_type,
        distance_to_target=0.0,
        yaw_adjustment=0.0,
        timestamp=time.time()
    )

def create_motion_record(from_pose: List[float], to_pose: List[float],
                       command_type: str, success: bool) -> MotionRecord:
    """创建运动记录的便捷函数"""
    return MotionRecord(
        timestamp=time.time(),
        from_pose=from_pose,
        to_pose=to_pose,
        command_type=command_type,
        movement_type="proportional",
        success=success
    )

# 类型别名
DetectionList = List[DetectionResult]
MotionHistory = List[MotionRecord]
FeatureDatabase = Dict[str, Dict[str, Any]]

# 测试数据结构
if __name__ == "__main__":
    import time
    
    # 测试检测结果
    print("Testing DetectionResult...")
    detection = create_detection_result(
        object_id="lemon_0",
        class_id=4,
        class_name="lemon",
        bbox=[100, 100, 200, 200],
        confidence=0.9
    )
    print(f"Detection valid: {detection.is_valid()}")
    print(f"Bbox center: {detection.get_bbox_center()}")
    print(f"Bbox area: {detection.get_bbox_area()}")
    
    # 测试追踪命令
    print("\nTesting TrackingCommand...")
    target_pose = {
        'position': {'x': 100, 'y': 200, 'z': 300},
        'orientation': {'roll': 180, 'pitch': 0, 'yaw': 0}
    }
    command = create_tracking_command(TrackingState.TRACKING, target_pose)
    print(f"Command valid: {command.is_valid()}")
    
    # 测试运动记录
    print("\nTesting MotionRecord...")
    motion = create_motion_record([0, 0, 0, 180, 0, 0], [100, 100, 300, 180, 0, 0], "move", True)
    print(f"Distance moved: {motion.get_distance_moved():.2f}")
    
    # 测试特征匹配
    print("\nTesting FeatureMatch...")
    match = FeatureMatch(
        target_id="lemon_0",
        reference_id="lemon_0",
        overall_score=0.85,
        class_score=1.0,
        hu_moments_score=0.8,
        color_histogram_score=0.9,
        spatial_continuity_score=0.7,
        match_method="full_matching",
        confidence=0.85
    )
    print(f"Good match: {match.is_good_match()}")
    
    # 测试相机帧
    print("\nTesting CameraFrame...")
    fake_image = np.zeros((480, 640, 3), dtype=np.uint8)
    frame = CameraFrame(
        timestamp=time.time(),
        color_image=fake_image
    )
    print(f"Frame valid: {frame.is_valid()}")
    print(f"Image shape: {frame.get_image_shape()}")
    
    print("\n✅ All data structures test completed")