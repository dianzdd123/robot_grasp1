#!/usr/bin/env python3
"""
Tracking System Configuration Manager
追踪系统配置管理器
"""

import os
import yaml
from typing import Dict, Any, List, Tuple
from enum import Enum
from dataclasses import dataclass

class TrackingState(Enum):
    """追踪状态枚举"""
    IDLE = "idle"
    INITIALIZING = "initializing"
    SEARCHING = "searching"
    TRACKING = "tracking"
    APPROACHING = "approaching"
    GRASPING = "grasping"
    RETURNING = "returning"
    PLACING = "placing"
    RECOVERY = "recovery"
    ERROR = "error"

class TrackingMode(Enum):
    """追踪模式枚举"""
    FULL_MATCHING = "full_matching"          # 完整特征匹配
    LIGHTWEIGHT_TRACKING = "lightweight"     # 轻量级追踪
    SPATIAL_PREDICTION = "spatial_prediction" # 空间预测

@dataclass
class TrackingConfig:
    """追踪系统配置类"""
    
    def __init__(self, config_file: str = None):
        """初始化配置"""
        self.config_file = config_file
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self.config_file and os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                print(f"[TRACKING_CONFIG] 从文件加载配置: {self.config_file}")
                return config
            except Exception as e:
                print(f"[TRACKING_CONFIG] 配置文件加载失败: {e}")
        
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        home_dir = os.path.expanduser("~")
        model_dir = os.path.join(home_dir, "ros2_ws", "src", "vision_ai", "models")
        
        return {
            # ============ ROS2 话题配置 ============
            'topics': {
                # 输入话题
                'camera_color': '/camera/color/image_raw',
                'camera_depth': '/camera/depth/image_raw',
                'camera_info': '/camera/color/camera_info',
                'xarm_current_pose': '/xarm/current_pose',
                'detection_complete': '/detection_complete',
                
                # 输出话题
                'xarm_target_pose': '/xarm/target_pose',
                'xarm_gripper_target': '/xarm/gripper_target',
                'tracking_status': '/tracking/status',
                'tracking_visualization': '/tracking/visualization',
                'tracking_control': '/tracking/control',
                
                # 内部话题
                'tracking_detection_result': '/tracking/detection_result',
                'tracking_state_change': '/tracking/state_change',
                'tracking_recovery': '/tracking/recovery',
            },
            
            # ============ 追踪控制参数 ============
            'tracking': {
                'proportional_factor': 0.2,      # 比例控制因子
                'move_speed': 60,                # 运动速度 mm/s
                'target_tolerance_xy': 30.0,     # XY平面距离阈值 mm
                'target_tolerance_yaw': 5.0,     # YAW角度阈值 degrees
                'approach_height': 400.0,        # 逼近高度 mm
                'grasp_height_offset': 50.0,     # 抓取高度偏移 mm
                'safe_height': 400.0,            # 安全高度 mm
                'min_z_height': 200.0,           # 最低高度限制 mm
                'max_xy_distance': 1000.0,       # 最大XY距离 mm
                'collision_avoidance': True,     # 启用碰撞避免
            },
            
            # ============ 检测参数 ============
            'detection': {
                'frequency': 10.0,               # 检测频率 Hz
                'max_lost_frames': 10,           # 最大丢失帧数
                'lightweight_continuity_frames': 10,  # 轻量级追踪连续帧数
                'spatial_continuity_threshold': 100.0,  # 空间连续性阈值 pixels
                'confidence_threshold': 0.7,     # 检测置信度阈值
            },
            
            # ============ YOLO配置 ============
            'yolo': {
                'model_path': '/home/qi/下载/best2.pt',
                'confidence_threshold': 0.6,  # 降低阈值用于测试
                'iou_threshold': 0.5,
                'device': 'cuda',
                'imgsz': 640,
            },
            
            # ============ SAM2配置 ============
            'sam2': {
                'checkpoint': os.path.join(model_dir, 'sam2', 'sam2_hiera_large.pt'),
                'config': 'sam2_hiera_l.yaml',
                'device': 'cuda',
            },
            
            # ============ 特征匹配配置 ============
            'features': {
                'match_threshold': 0.6,          # 从0.6改为0.3
                'weights': {
                    'class_id': 1.0,             
                    'hu_moments': 0.5,           # 从0.6改为0.3
                    'color_histogram': 0.5,      # 从0.8改为0.7
                    'spatial_continuity': 0.2    
                },
                'color': {
                    'histogram_bins': 96,        
                },
                'shape': {
                    'hu_moments_count': 4,       
                },
            },
            
            # ============ 相机参数 ============
            'camera': {
                'intrinsics': {
                    'fx': 912.694580078125,
                    'fy': 910.309814453125,
                    'cx': 640.0,
                    'cy': 360.0
                },
                'image_size': {
                    'width': 1280,
                    'height': 720
                },
                'depth_scale': 0.001,            # 深度缩放因子 (mm to m)
            },
            
            # ============ 回退机制配置 ============
            'recovery': {
                'max_attempts': 3,               # 最大回退尝试次数
                'waypoint_search_timeout': 30.0, # waypoint搜索超时 seconds
                'return_to_last_position': True, # 是否返回上一位置
                're_scan_on_failure': True,      # 失败时是否重新扫描
            },
            
            # ============ 夹爪控制配置 ============
            'gripper': {
                'fully_open': 850,              # 完全打开位置
                'closed': 150,                  # 关闭位置
                'default_grasp_width': 300,     # 默认抓取宽度
                'width_safety_margin': 10,      # 宽度安全边距
            },
            
            # ============ 类别名称映射 ============
            'class_names': {
                1: 'banana',
                2: 'carrot', 
                3: 'corn',
                4: 'lemon',
                5: 'greenlemon',
                6: 'strawberry',
                7: 'tomato',
                8: 'potato',
                9: 'redpepper'
            },
            
            # ============ 日志配置 ============
            'logging': {
                'level': 'INFO',
                'save_tracking_history': True,
                'save_motion_records': True,
                'log_detection_results': True,
            },
            
            # ============ 测试配置 ============
            'testing': {
                'independent_mode': False,       # 独立测试模式
                'mock_arm_control': False,       # 模拟机械臂控制
                'visualization_enabled': True,   # 启用可视化
                'auto_start_tracking': False,    # 自动开始追踪
            }
        }
    
    # ============ 获取配置方法 ============
    
    @property
    def topics(self) -> Dict[str, str]:
        """获取话题配置"""
        return self.config.get('topics', {})
    
    @property
    def tracking_params(self) -> Dict[str, Any]:
        """获取追踪参数"""
        return self.config.get('tracking', {})
    
    @property
    def detection_params(self) -> Dict[str, Any]:
        """获取检测参数"""
        return self.config.get('detection', {})
    
    @property
    def yolo_config(self) -> Dict[str, Any]:
        """获取YOLO配置"""
        return self.config.get('yolo', {})
    
    @property
    def sam2_config(self) -> Dict[str, Any]:
        """获取SAM2配置"""
        return self.config.get('sam2', {})
    
    @property
    def feature_config(self) -> Dict[str, Any]:
        """获取特征配置"""
        return self.config.get('features', {})
    
    @property
    def camera_config(self) -> Dict[str, Any]:
        """获取相机配置"""
        return self.config.get('camera', {})
    
    @property
    def recovery_config(self) -> Dict[str, Any]:
        """获取回退配置"""
        return self.config.get('recovery', {})
    
    @property
    def gripper_config(self) -> Dict[str, Any]:
        """获取夹爪配置"""
        return self.config.get('gripper', {})
    
    @property
    def class_names(self) -> Dict[int, str]:
        """获取类别名称"""
        return self.config.get('class_names', {})
    
    @property
    def logging_config(self) -> Dict[str, Any]:
        """获取日志配置"""
        return self.config.get('logging', {})
    
    @property
    def testing_config(self) -> Dict[str, Any]:
        """获取测试配置"""
        return self.config.get('testing', {})
    
    # ============ 便捷访问方法 ============
    
    def get_proportional_factor(self) -> float:
        """获取比例控制因子"""
        return self.tracking_params.get('proportional_factor', 0.2)
    
    def get_target_tolerance_xy(self) -> float:
        """获取XY距离阈值"""
        return self.tracking_params.get('target_tolerance_xy', 30.0)
    
    def get_target_tolerance_yaw(self) -> float:
        """获取YAW角度阈值"""
        return self.tracking_params.get('target_tolerance_yaw', 5.0)
    
    def get_max_lost_frames(self) -> int:
        """获取最大丢失帧数"""
        return self.detection_params.get('max_lost_frames', 10)
    
    def get_lightweight_continuity_frames(self) -> int:
        """获取轻量级追踪连续帧数"""
        return self.detection_params.get('lightweight_continuity_frames', 6)
    
    def get_detection_frequency(self) -> float:
        """获取检测频率"""
        return self.detection_params.get('frequency', 10.0)
    
    def get_feature_match_threshold(self) -> float:
        """获取特征匹配阈值"""
        return self.feature_config.get('match_threshold', 0.6)
    
    def get_feature_weights(self) -> Dict[str, float]:
        """获取特征权重"""
        return self.feature_config.get('weights', {})
    
    def get_camera_intrinsics(self) -> Dict[str, float]:
        """获取相机内参"""
        return self.camera_config.get('intrinsics', {})
    
    def get_safe_height(self) -> float:
        """获取安全高度"""
        return self.tracking_params.get('safe_height', 400.0)
    
    def get_min_z_height(self) -> float:
        """获取最低高度"""
        return self.tracking_params.get('min_z_height', 200.0)
    
    # ============ 验证和保存方法 ============
    
    def validate_config(self) -> bool:
        """验证配置的有效性"""
        try:
            # 检查必要的配置段
            required_sections = ['topics', 'tracking', 'detection', 'yolo', 'sam2', 'camera', 'class_names']
            for section in required_sections:
                if section not in self.config:
                    print(f"[TRACKING_CONFIG] 缺少必要配置段: {section}")
                    return False
            
            # 检查YOLO模型文件
            yolo_model = self.yolo_config.get('model_path', '')
            if not os.path.exists(yolo_model):
                print(f"[TRACKING_CONFIG] YOLO模型文件不存在: {yolo_model}")
                return False
            
            # 检查SAM2模型文件
            sam2_checkpoint = self.sam2_config.get('checkpoint', '')
            if not os.path.exists(sam2_checkpoint):
                print(f"[TRACKING_CONFIG] SAM2模型文件不存在: {sam2_checkpoint}")
                return False
            
            print(f"[TRACKING_CONFIG] 配置验证通过")
            return True
            
        except Exception as e:
            print(f"[TRACKING_CONFIG] 配置验证失败: {e}")
            return False
    
    def save_config(self, output_path: str):
        """保存配置到文件"""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            print(f"[TRACKING_CONFIG] 配置已保存到: {output_path}")
        except Exception as e:
            print(f"[TRACKING_CONFIG] 配置保存失败: {e}")
    
    def update_config(self, updates: Dict[str, Any]):
        """更新配置"""
        def deep_update(base_dict, update_dict):
            for key, value in update_dict.items():
                if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value
        
        deep_update(self.config, updates)
        print(f"[TRACKING_CONFIG] 配置已更新")
    
    def get_file_paths(self) -> Dict[str, str]:
        """获取文件路径配置"""
        return {
            'yolo_model': self.yolo_config.get('model_path', ''),
            'sam2_checkpoint': self.sam2_config.get('checkpoint', ''),
            'sam2_config': self.sam2_config.get('config', ''),
        }
    
    def print_config_summary(self):
        """打印配置摘要"""
        print("\n" + "="*50)
        print("🎯 TRACKING SYSTEM CONFIG SUMMARY")
        print("="*50)
        print(f"📊 比例控制因子: {self.get_proportional_factor()}")
        print(f"📏 XY距离阈值: {self.get_target_tolerance_xy()}mm")
        print(f"🔄 YAW角度阈值: {self.get_target_tolerance_yaw()}°")
        print(f"⏱️  检测频率: {self.get_detection_frequency()}Hz")
        print(f"🔢 最大丢失帧: {self.get_max_lost_frames()}")
        print(f"🔄 轻量级连续帧: {self.get_lightweight_continuity_frames()}")
        print(f"🎯 特征匹配阈值: {self.get_feature_match_threshold()}")
        print(f"⚡ 安全高度: {self.get_safe_height()}mm")
        print(f"⬇️  最低高度: {self.get_min_z_height()}mm")
        print(f"📷 相机内参: fx={self.get_camera_intrinsics().get('fx', 0):.1f}")
        print(f"🤖 YOLO模型: {os.path.basename(self.yolo_config.get('model_path', ''))}")
        print(f"🎭 SAM2模型: {os.path.basename(self.sam2_config.get('checkpoint', ''))}")
        print(f"🏷️  类别数量: {len(self.class_names)}")
        print("="*50)


# ============ 全局配置实例 ============
def create_tracking_config(config_file: str = None) -> TrackingConfig:
    """创建追踪配置实例"""
    return TrackingConfig(config_file)


# ============ 数据结构定义 ============
@dataclass
class DetectionResult:
    """检测结果数据结构"""
    object_id: str
    class_id: int
    class_name: str
    bounding_box: List[float]
    mask: Any  # np.ndarray
    centroid_2d: Tuple[float, float]
    centroid_3d: Tuple[float, float, float]
    confidence: float
    features: Dict[str, Any]
    match_confidence: float = 0.0
    match_method: str = "unknown"

@dataclass
class TrackingCommand:
    """追踪命令数据结构"""
    state: TrackingState
    mode: TrackingMode
    target_pose: Dict[str, Any]
    gripper_command: Dict[str, Any] = None
    movement_type: str = "proportional"  # "proportional", "approach", "grasp", "return"
    distance_mm: float = 0.0
    yaw_adjustment: float = 0.0
    success: bool = False

@dataclass
class MotionRecord:
    """运动记录数据结构"""
    timestamp: float
    from_pose: List[float]
    to_pose: List[float]
    command_type: str
    success: bool
    target_position: Tuple[float, float]
    distance_to_target: float
    state: TrackingState
    mode: TrackingMode


if __name__ == "__main__":
    # 测试配置
    config = create_tracking_config()
    config.print_config_summary()
    
    # 验证配置
    if config.validate_config():
        print("✅ 配置验证通过")
    else:
        print("❌ 配置验证失败")