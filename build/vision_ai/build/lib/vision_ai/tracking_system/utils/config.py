#!/usr/bin/env python3

import os
import numpy as np
from dataclasses import dataclass
from typing import Dict, Tuple, List

@dataclass
class CameraConfig:
    """相机配置"""
    fx: float = 912.7
    fy: float = 910.3  
    cx: float = 640
    cy: float = 360
    depth_min: float = 0.16  # 最小深度160mm
    depth_max: float = 3.0   # 最大深度3000mm
    depth_accuracy: float = 0.002  # 1-2mm@1m

@dataclass
class DetectionConfig:
    """检测配置"""
    yolo_model_path: str = "/home/qi/下载/best2.pt"
    yolo_confidence: float = 0.5
    sam2_checkpoint: str = "~/ros2_ws/src/vision_ai/models/sam2/sam2_hiera_large.pt"
    sam2_config: str = "sam2_hiera_l.yaml"
    device: str = "cuda"
    
    # YOLO类别映射
    class_names: Dict[int, str] = None
    
    def __post_init__(self):
        if self.class_names is None:
            self.class_names = {
                1: 'banana',
                2: 'carrot', 
                3: 'corn',
                4: 'lemon',
                5: 'greenlemon',
                6: 'strawberry',
                7: 'tomato',
                8: 'potato',
                9: 'redpepper'
            }

@dataclass
class TrackingConfig:
    """追踪配置"""
    # 简化的距离阶段控制
    height_phases: Dict[str, float] = None
    
    # ID匹配阈值
    color_hist_threshold: float = 0.4
    hu_moment_threshold: float = 0.3
    position_continuity_threshold: float = 50.0  # pixels
    
    # 特征权重
    feature_weights: Dict[str, float] = None
    
    # 控制参数
    proportional_factor: float = 0.1
    movement_speed: float = 0.5  # 统一移动速度
    
    # 对齐阈值（新增）
    alignment_thresholds: Dict[str, float] = None
    
    # 状态机参数
    lost_frame_threshold: int = 10
    lost_frame_threshold_approaching: int = 5  # 下降中更敏感
    
    def __post_init__(self):
        if self.height_phases is None:
            self.height_phases = {
                'TRACKING': 350,        # 固定追踪高度
                'APPROACHING_START': 350,  # 开始下降高度
                'APPROACHING_END': 270,    # 结束下降高度  
                'GRASPING': 270         # 抓取高度
            }
        
        if self.feature_weights is None:
            self.feature_weights = {
                'color_hist': 0.4,
                'position_continuity': 0.3,
                'shape_moments': 0.3
            }
        
        if self.alignment_thresholds is None:
            self.alignment_thresholds = {
                'xy_tolerance': 10.0,      # mm - xy对齐容差
                'yaw_tolerance': 5.0,      # 度 - yaw对齐容差
                'descent_step': 5.0,       # mm - 每步下降距离
                'approach_timeout': 30.0,  # 秒 - 接近超时
                'tracking_timeout': 60.0   # 秒 - 追踪超时
            }

@dataclass
class WorkspaceConfig:
    """工作空间配置"""
    x_limits: Tuple[float, float] = (-800, 800)
    y_limits: Tuple[float, float] = (-800, 800)
    z_limits: Tuple[float, float] = (100, 800)
    min_height: float = 250.0  # 最小安全高度

@dataclass
class GripperConfig:
    """夹爪配置"""
    open_position: int = 850
    closed_position: int = 0
    partial_open: int = 70
    width_offset: float = 50.0  # 夹爪宽度偏移量
    
    # 基于高度的pitch角度
    pitch_rules: Dict[str, float] = None
    
    def __post_init__(self):
        if self.pitch_rules is None:
            self.pitch_rules = {
                'low': (80, 0),      # height <= 80mm: pitch = 0
                'medium': (150, -20), # 80 < height <= 150mm: pitch = -20
                'high': (float('inf'), -40)  # height > 150mm: pitch = -40
            }

@dataclass
class CoordinateTransformConfig:
    """坐标变换配置"""
    # 相机到世界坐标的偏移
    camera_offset: Tuple[float, float, float] = (65, -30, -100)
    # 旋转调整
    roll_correction: float = -180
    
class TrackingSystemConfig:
    """追踪系统总配置"""
    
    def __init__(self, config_file: str = None):
        self.camera = CameraConfig()
        self.detection = DetectionConfig()
        self.tracking = TrackingConfig()
        self.workspace = WorkspaceConfig()
        self.gripper = GripperConfig()
        self.coordinate_transform = CoordinateTransformConfig()
        
        # ROS话题配置
        self.topics = {
            'detection_result': '/detection_result',
            'camera_color': '/camera/color/image_raw',
            'camera_depth': '/camera/depth/image_raw',
            'xarm_current_pose': '/xarm/current_pose',
            'tracking_status': '/tracking/status',
            'xarm_target_pose': '/xarm/target_pose',
            'xarm_gripper_target': '/xarm/gripper_target',
            'tracking_visualization': '/tracking/visualization'
        }
        
        # 服务配置
        self.services = {
            'start_tracking': '/tracking/start_tracking',
            'stop_tracking': '/tracking/stop_tracking',
            'emergency_stop': '/tracking/emergency_stop'
        }
        
        # 文件路径配置
        self.paths = {
            'tracking_selection': '/tmp/tracking_selection.txt',
            'detection_results_dir': '/tmp/detection_results',
            'logs_dir': '/tmp/tracking_logs'
        }
        
        if config_file:
            self.load_from_file(config_file)
    
    def load_from_file(self, config_file: str):
        """从文件加载配置"""
        # TODO: 实现YAML配置文件加载
        pass
    
    def get_current_height(self, state: str) -> float:
        """根据状态获取当前应该的高度"""
        return self.tracking.height_phases.get(state, 350)
    
    def check_xy_alignment(self, current_pos: Tuple, target_pos: Tuple) -> bool:
        """检查xy是否对齐"""
        if not current_pos or not target_pos:
            return False
        
        error_x = abs(current_pos[0] - target_pos[0])
        error_y = abs(current_pos[1] - target_pos[1])
        
        tolerance = self.tracking.alignment_thresholds['xy_tolerance']
        return error_x <= tolerance and error_y <= tolerance
    
    def check_yaw_alignment(self, current_yaw: float, target_yaw: float) -> bool:
        """检查yaw是否对齐"""
        yaw_error = abs(current_yaw - target_yaw)
        # 处理角度跨越180/-180的情况
        if yaw_error > 180:
            yaw_error = 360 - yaw_error
        
        tolerance = self.tracking.alignment_thresholds['yaw_tolerance']
        return yaw_error <= tolerance
    
    def calculate_descent_height(self, progress_ratio: float) -> float:
        """计算渐进下降的高度"""
        start_height = self.tracking.height_phases['APPROACHING_START']
        end_height = self.tracking.height_phases['APPROACHING_END']
        
        # 线性插值
        current_height = start_height - (start_height - end_height) * progress_ratio
        return max(end_height, current_height)
    
    def get_gripper_pitch(self, height_mm: float) -> float:
        """根据物体高度计算pitch角"""
        for rule, (threshold, pitch) in self.gripper.pitch_rules.items():
            if height_mm <= threshold:
                return pitch
        return -40  # 默认值
    
    def calculate_gripper_width(self, object_width_mm: float) -> int:
        """计算夹爪开口宽度"""
        width = int(object_width_mm + self.gripper.width_offset)
        return max(0, min(width, self.gripper.open_position))
    
    def is_position_safe(self, x: float, y: float, z: float) -> bool:
        """检查位置是否在安全工作空间内"""
        return (self.workspace.x_limits[0] <= x <= self.workspace.x_limits[1] and
                self.workspace.y_limits[0] <= y <= self.workspace.y_limits[1] and
                self.workspace.z_limits[0] <= z <= self.workspace.z_limits[1] and
                z >= self.workspace.min_height)
    
    def apply_coordinate_transform(self, camera_point: Tuple[float, float, float], 
                                 arm_pose: List[float]) -> Tuple[float, float, float]:
        """应用坐标转换"""
        x_c, y_c, z_c = camera_point
        
        # 坐标轴重排 + 偏移
        reordered = np.array([
            (y_c + self.coordinate_transform.camera_offset[0]),
            (x_c + self.coordinate_transform.camera_offset[1]), 
            -(z_c + self.coordinate_transform.camera_offset[2])
        ])
        
        # 旋转矩阵
        roll_corrected = abs(arm_pose[3]) + self.coordinate_transform.roll_correction
        from scipy.spatial.transform import Rotation as R
        R_matrix = R.from_euler('XYZ', [roll_corrected, arm_pose[4], arm_pose[5]], 
                               degrees=True).as_matrix()
        
        # 应用变换
        world_point = R_matrix @ reordered + np.array(arm_pose[:3])
        
        return tuple(world_point)

# 全局配置实例
TRACKING_CONFIG = TrackingSystemConfig()