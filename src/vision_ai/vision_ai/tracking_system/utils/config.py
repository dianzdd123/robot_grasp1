#!/usr/bin/env python3
"""
追踪系统配置管理
配置所有追踪参数和系统设置
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum

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

class TrackingConfig:
    """追踪系统配置类"""
    
    def __init__(self):
        # ================== 核心追踪参数 ==================
        self.proportional_factor = 0.2
        self.move_speed = 60
        self.target_tolerance_xy = 30.0  # mm
        self.target_tolerance_yaw = 5.0  # degrees
        self.approach_height = 400.0     # mm
        self.grasp_height_offset = 50.0  # mm
        self.safe_height = 500.0         # mm
        
        # ================== 检测参数 ==================
        self.detection_frequency = 10.0  # Hz
        self.max_lost_frames = 10
        self.feature_match_threshold = 0.6
        self.spatial_continuity_threshold = 100.0  # pixels
        
        # ================== 轻量级追踪参数 ==================
        self.lightweight_enable = True
        self.lightweight_continuity_frames = 5
        self.spatial_prediction_enable = True
        
        # ================== 特征匹配权重 ==================
        self.feature_weights = {
            'class_id': 1.0,
            'hu_moments': 0.4,
            'color_histogram': 0.4,
            'spatial_continuity': 0.2
        }
        
        # ================== 安全限制 ==================
        self.min_z_height = 350.0  # mm
        self.max_xy_distance = 1000.0  # mm
        self.collision_avoidance = True
        
        # ================== ROS话题配置 ==================
        self.topics = {
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
        }
        
        # ================== 文件路径配置 ==================
        self.paths = {
            'detection_results_dir': '',  # 由检测完成信号动态设置
            'tracking_selection': '',     # 由检测完成信号动态设置
            'reference_features_db': '',  # 参考特征数据库
            'tracking_logs': '',          # 追踪日志
            'motion_history': '',         # 运动历史
        }
        
        # ================== YOLO配置 ==================
        self.yolo_config = {
            'model_path': '/path/to/yolo/model',
            'confidence_threshold': 0.5,
            'nms_threshold': 0.4,
            'input_size': 640,
            'class_names': {
                0: 'apple',
                1: 'orange', 
                2: 'carrot',
                3: 'corn',
                4: 'lemon',
                5: 'greenlemon'
            }
        }
        
        # ================== SAM2配置 ==================
        self.sam2_config = {
            'model_path': '/path/to/sam2/model',
            'model_cfg': 'sam2_hiera_b_plus.yaml',
            'device': 'cuda',
            'batch_size': 1
        }
        
        # ================== 相机内参 ==================
        self.camera_intrinsics = {
            'fx': 651.01251,
            'fy': 651.01251,
            'cx': 640.0,
            'cy': 360.0,
            'depth_scale': 0.001  # RealSense深度比例
        }
        
        # ================== 回退配置 ==================
        self.recovery_config = {
            'max_attempts': 3,
            'waypoint_search_timeout': 30.0,  # seconds
            'return_to_last_pose': True,
            'search_waypoints': True
        }
        
        # ================== 日志配置 ==================
        self.logging_config = {
            'level': 'INFO',
            'format': '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
            'file_logging': True,
            'console_logging': True
        }
    
    def update_paths(self, scan_directory: str) -> None:
        """更新文件路径配置"""
        self.paths['detection_results_dir'] = os.path.join(scan_directory, 'detection_results')
        self.paths['tracking_selection'] = os.path.join(scan_directory, 'detection_results', 'tracking_selection.txt')
        self.paths['reference_features_db'] = os.path.join(scan_directory, 'detection_results', 'detection_results.json')
        self.paths['tracking_logs'] = os.path.join(scan_directory, 'tracking_logs')
        self.paths['motion_history'] = os.path.join(scan_directory, 'motion_history.json')
    
    def get_class_name(self, class_id: int) -> str:
        """获取类别名称"""
        return self.yolo_config['class_names'].get(class_id, f'class_{class_id}')
    
    def validate_config(self) -> bool:
        """验证配置有效性"""
        # 检查必要参数
        required_params = [
            'proportional_factor', 'move_speed', 'target_tolerance_xy',
            'detection_frequency', 'max_lost_frames', 'feature_match_threshold'
        ]
        
        for param in required_params:
            if not hasattr(self, param):
                print(f"[ERROR] Missing required parameter: {param}")
                return False
        
        # 检查数值范围
        if not (0 < self.proportional_factor <= 1.0):
            print(f"[ERROR] proportional_factor must be in (0, 1], got {self.proportional_factor}")
            return False
        
        if not (0 < self.detection_frequency <= 30.0):
            print(f"[ERROR] detection_frequency must be in (0, 30], got {self.detection_frequency}")
            return False
        
        if not (0 < self.feature_match_threshold <= 1.0):
            print(f"[ERROR] feature_match_threshold must be in (0, 1], got {self.feature_match_threshold}")
            return False
        
        return True
    
    def print_config(self) -> None:
        """打印配置信息"""
        print("=" * 50)
        print("TRACKING SYSTEM CONFIGURATION")
        print("=" * 50)
        print(f"Proportional Factor: {self.proportional_factor}")
        print(f"Move Speed: {self.move_speed}")
        print(f"Target Tolerance XY: {self.target_tolerance_xy} mm")
        print(f"Detection Frequency: {self.detection_frequency} Hz")
        print(f"Max Lost Frames: {self.max_lost_frames}")
        print(f"Feature Match Threshold: {self.feature_match_threshold}")
        print(f"Lightweight Tracking: {'Enabled' if self.lightweight_enable else 'Disabled'}")
        print(f"Spatial Prediction: {'Enabled' if self.spatial_prediction_enable else 'Disabled'}")
        print("=" * 50)

# 全局配置实例
_config_instance = None

def get_config() -> TrackingConfig:
    """获取配置实例（单例模式）"""
    global _config_instance
    if _config_instance is None:
        _config_instance = TrackingConfig()
    return _config_instance

def set_config(config: TrackingConfig) -> None:
    """设置配置实例"""
    global _config_instance
    _config_instance = config

# 测试配置
if __name__ == "__main__":
    config = get_config()
    config.print_config()
    
    # 验证配置
    if config.validate_config():
        print("✅ Configuration validation passed")
    else:
        print("❌ Configuration validation failed")