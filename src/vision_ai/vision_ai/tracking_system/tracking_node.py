#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
import json
import os
import cv2
import numpy as np
from datetime import datetime
import threading
import time
import math
# 导入Track模块组件
from .enhanced_tracker import EnhancedTracker
from .utils.feedback_collector import FeedbackCollector
from .utils.data_recorder import DataRecorder
from .utils.user_profile_manager import UserProfileManager
from .utils.tracking_visualizer import TrackingVisualizer
from .adaptive_learning.online_learner import OnlineLearner
from ..detection.enhanced_detection_pipeline import EnhancedDetectionPipeline

class TrackingNode(Node):
    def __init__(self):
        super().__init__('tracking_node')
        
        # 🔧 修复：系统状态初始化 - 增加确认等待状态
        self.tracking_active = False
        self.current_target_id = None
        self.current_scan_dir = None
        self.current_user_id = None
        self.movement_complete = True
        self.tracking_count = 0
        self.max_tracking_steps = 20
        
        # 🆕 用户确认状态管理
        self.waiting_for_user_confirmation = False
        self.current_tracking_result = None
        self.user_feedback_received = False
        self.command_input_thread = None
        
        # 🆕 姿态控制
        self.initial_yaw = None  # 记录初始yaw角度
        self.max_yaw_change = 90.0  # 最大yaw变化限制（度）
        
        # 🆕 追踪参数记录
        self.tracking_parameters_history = []
        
        # 图像数据缓存
        self.latest_rgb_image = None
        self.latest_depth_image = None
        self.latest_camera_info = None
        
        # 核心组件（初始化时都为None）
        self.tracker = None
        self.feedback_collector = None
        self.data_recorder = None
        self.user_profile_manager = None
        self.visualizer = None
        self.online_learner = None
        self.detection_pipeline = None
        
        # 线程锁和TCP位姿
        self.tracking_lock = threading.Lock()
        self.current_tcp_pose = None
        self.previous_yaw = None  # 🆕 用于yaw角度连续性处理
        # 系统状态标志
        self.system_initialized = False
        self.waiting_for_detection_complete = True
        
        # 初始化基础组件
        from cv_bridge import CvBridge
        self.bridge = CvBridge()
        
        # 订阅机械臂状态获取TCP位姿
        self.tcp_pose_sub = self.create_subscription(
            PoseStamped, '/xarm/current_pose', self.tcp_pose_callback, 10
        )
        
        # ROS接口设置
        self._setup_ros_interfaces()
        
        # 系统启动检查
        self._perform_startup_checks()
        
        self.get_logger().info('🎯 Track节点启动完成 - 等待检测完成信号')
    
    def _setup_ros_interfaces(self):
        """设置ROS接口"""
        # 订阅检测完成信号
        self.detection_complete_sub = self.create_subscription(
            String, '/detection_complete', self.detection_complete_callback, 10
        )
        
        # 订阅相机数据
        self.rgb_image_sub = self.create_subscription(
            Image, '/camera/color/image_raw', self.rgb_image_callback, 10
        )
        self.depth_image_sub = self.create_subscription(
            Image, '/camera/depth/image_raw', self.depth_image_callback, 10
        )
        
        # 订阅机械臂移动完成信号
        self.movement_complete_sub = self.create_subscription(
            String, '/xarm/movement_complete', self.movement_complete_callback, 10
        )
        
        # 发布追踪结果给机械臂
        self.tracking_result_pub = self.create_publisher(
            PoseStamped, '/xarm/target_pose', 10
        )
        self.tracking_status_pub = self.create_publisher(
            String, '/tracking_status', 10
        )
        
        # 发布追踪完成信号
        self.tracking_complete_pub = self.create_publisher(
            String, '/tracking_complete', 10
        )
        # 🆕 发布抓取触发信号
        self.grasp_trigger_pub = self.create_publisher(
            String, '/grasp_trigger', 10
        )
    def _perform_startup_checks(self):
        """执行启动检查"""
        try:
            self.get_logger().info('🔧 执行系统启动检查...')
            
            # 检查关键文件路径
            key_files = [
                '/home/qi/下载/best2.pt',
                '/home/qi/ros2_ws/src/vision_ai/models/sam2/sam2_hiera_large.pt',
                '/home/qi/ros2_ws/src/vision_ai/vision_ai/detection/config/enhanced_detection_config.json'
            ]
            
            all_files_exist = True
            for file_path in key_files:
                if os.path.exists(file_path):
                    self.get_logger().info(f'  ✅ {os.path.basename(file_path)}')
                else:
                    self.get_logger().warn(f'  ❌ {file_path} (不存在)')
                    all_files_exist = False
            
            # 检查ROS话题连接
            self.get_logger().info('🔧 检查ROS话题连接...')
            self.get_logger().info('  - 等待检测完成信号: /detection_complete')
            self.get_logger().info('  - 等待相机数据: /camera/color/image_raw, /camera/depth/image_raw')
            self.get_logger().info('  - 等待机械臂位姿: /xarm/current_pose')
            
            if all_files_exist:
                self.get_logger().info('✅ 启动检查完成 - 所有必需文件存在')
            else:
                self.get_logger().warn('⚠️ 启动检查完成 - 部分文件缺失，可能影响功能')
            
            self.get_logger().info('🔔 系统就绪，等待检测完成信号开始追踪...')
            
        except Exception as e:
            self.get_logger().error(f'启动检查失败: {e}')
    
    def _extract_user_id(self, scan_dir_path: str) -> str:
        """从扫描目录路径提取用户ID"""
        try:
            # /home/qi/ros2_ws/scan_output_20250728_214915 -> qi
            path_parts = scan_dir_path.split('/')
            for i, part in enumerate(path_parts):
                if part == 'home' and i + 1 < len(path_parts):
                    return path_parts[i + 1]
            
            # 如果提取失败，使用默认值
            return 'default_user'
            
        except Exception as e:
            self.get_logger().error(f'提取用户ID失败: {e}')
            return 'default_user'
    
    def detection_complete_callback(self, msg):
        """检测完成回调 - 初始化追踪系统"""
        try:
            data = json.loads(msg.data)
            
            self.get_logger().info('🔔 收到检测完成信号，开始初始化追踪系统...')
            
            # 检查是否是增强检测结果
            if not data.get('enhanced_detection', False):
                self.get_logger().info('📍 接收到普通检测结果，跳过增强追踪')
                return
            
            self.current_scan_dir = data.get('scan_directory')
            if not self.current_scan_dir:
                self.get_logger().error('❌ 无法获取扫描目录')
                return
            
            self.get_logger().info(f'📁 扫描目录: {self.current_scan_dir}')
            
            # 提取用户ID
            self.current_user_id = self._extract_user_id(self.current_scan_dir)
            self.get_logger().info(f'👤 用户ID: {self.current_user_id}')
            
            # 🔧 标记不再等待检测完成信号
            self.waiting_for_detection_complete = False
            
            # 初始化追踪系统
            success = self._initialize_tracking_system(data)
            
            if success:
                # 🔧 只有在系统完全初始化成功后才激活追踪
                self.system_initialized = True
                self.tracking_active = True
                self.get_logger().info('✅ 追踪系统初始化成功，开始追踪')
            else:
                self.get_logger().error('❌ 追踪系统初始化失败')
                
        except Exception as e:
            self.get_logger().error(f'处理检测完成信号失败: {e}')
            import traceback
            traceback.print_exc()

    def _publish_grasp_trigger(self, filename: str, coordinate: dict):
        """发布抓取触发信号"""
        try:
            grasp_data = {
                'filename': filename,
                'coordinate': coordinate,
                'timestamp': datetime.now().isoformat(),
                'target_id': self.current_target_id,
                'trigger_reason': 'conditions_met'
            }
            
            trigger_msg = String()
            trigger_msg.data = json.dumps(grasp_data)
            self.grasp_trigger_pub.publish(trigger_msg)
            
            self.get_logger().info(f'📤 已发布抓取触发信号: {filename}')
            self.get_logger().info(f'📍 抓取坐标: ({coordinate["x"]:.1f}, {coordinate["y"]:.1f}, {coordinate["z"]:.1f}mm)')
            
        except Exception as e:
            self.get_logger().error(f'发布抓取触发信号失败: {e}')

    def _initialize_tracking_system(self, detection_data: dict) -> bool:
        """初始化追踪系统 - 完全使用参考库数据"""
        try:
            self.get_logger().info('🔧 开始初始化追踪系统...')
            
            # 1. 检查参考特征库文件
            reference_library_file = detection_data.get('reference_library_file')
            if not reference_library_file or not os.path.exists(reference_library_file):
                self.get_logger().error(f'❌ 参考特征库文件不存在: {reference_library_file}')
                return False
            
            self.get_logger().info(f'✅ 参考特征库文件: {reference_library_file}')
            
            # 2. 🔧 配置文件路径处理（保持不变）
            possible_config_paths = [
                '/home/qi/ros2_ws/src/vision_ai/vision_ai/tracking_system/config/tracking_config.json',
                os.path.join(os.path.dirname(__file__), 'config', 'tracking_config.json'),
                os.path.join(os.path.expanduser('~'), 'ros2_ws', 'src', 'vision_ai', 'vision_ai', 'tracking_system', 'config', 'tracking_config.json')
            ]
            
            config_path = None
            for path in possible_config_paths:
                if os.path.exists(path):
                    config_path = path
                    self.get_logger().info(f'✅ 找到追踪配置文件: {config_path}')
                    break

            
            # 3. 初始化追踪器
            self.tracker = EnhancedTracker(config_path)
            self.get_logger().info('✅ 追踪器初始化完成')
            
            # 4. 加载参考特征库
            if not self.tracker.load_reference_features(reference_library_file):
                self.get_logger().error('❌ 加载参考特征库失败')
                return False
            
            self.get_logger().info('✅ 参考特征库加载完成')
            
            # 5. 读取用户选择的追踪目标
            target_id = self._load_tracking_target()
            if not target_id:
                self.get_logger().error('❌ 无法加载追踪目标')
                return False
            
            self.current_target_id = target_id
            self.get_logger().info(f'🎯 追踪目标: {target_id}')
            
            # 6. 🔧 验证参考库中的高度数据（不需要缓存）
            if target_id in self.tracker.reference_library:
                ref_entry = self.tracker.reference_library[target_id]
                spatial_features = ref_entry.get('features', {}).get('spatial', {})
                
                height_mm = spatial_features.get('height_mm')
                background_z = spatial_features.get('background_world_z')
                
                if height_mm is not None and background_z is not None:
                    self.get_logger().info(f'✅ 参考库高度数据验证:')
                    self.get_logger().info(f'   高度: {height_mm:.1f}mm')
                    self.get_logger().info(f'   背景: {background_z:.1f}mm')
                else:
                    self.get_logger().warn(f'⚠️ 参考库中缺少高度数据')
            else:
                self.get_logger().error(f'❌ 目标 {target_id} 不在参考库中')
                return False
            
            # 7. 选择追踪目标
            if not self.tracker.select_tracking_target(target_id):
                self.get_logger().error(f'❌ 选择追踪目标失败: {target_id}')
                return False
            
            self.get_logger().info('✅ 追踪目标选择完成')
            
            # 8. 初始化其他组件
            self._initialize_auxiliary_components()
            
            # 9. 初始化检测管道
            self._initialize_detection_pipeline_fixed()
            
            # 10. 🔧 修复：简化组件验证，不检查缓存
            if not self._verify_system_components_no_cache():
                self.get_logger().error('❌ 系统组件验证失败')
                return False
            
            self.get_logger().info('🎉 追踪系统初始化完成，所有组件就绪')
            return True
            
        except Exception as e:
            self.get_logger().error(f'❌ 初始化追踪系统失败: {e}')
            import traceback
            traceback.print_exc()
            return False
    def _verify_system_components_no_cache(self) -> bool:
        """验证系统组件是否正常 - 不检查缓存"""
        try:
            self.get_logger().info('🔧 验证系统组件...')
            
            # 检查核心组件
            components = [
                ('tracker', self.tracker),
                ('detection_pipeline', self.detection_pipeline),
                ('data_recorder', self.data_recorder),
            ]
            
            all_ok = True
            for name, component in components:
                if component is not None:
                    self.get_logger().info(f'  ✅ {name}: 已初始化')
                else:
                    self.get_logger().error(f'  ❌ {name}: 未初始化')
                    all_ok = False
            
            # 检查追踪目标
            if self.current_target_id:
                self.get_logger().info(f'  ✅ 追踪目标: {self.current_target_id}')
            else:
                self.get_logger().error('  ❌ 追踪目标: 未设置')
                all_ok = False
            
            # 🔧 验证参考库数据而不是缓存
            if (hasattr(self.tracker, 'reference_library') and 
                self.current_target_id in self.tracker.reference_library):
                ref_entry = self.tracker.reference_library[self.current_target_id]
                spatial_data = ref_entry.get('features', {}).get('spatial', {})
                if 'height_mm' in spatial_data and 'background_world_z' in spatial_data:
                    self.get_logger().info(f'  ✅ 参考库数据: 高度和背景数据可用')
                else:
                    self.get_logger().warn(f'  ⚠️ 参考库数据: 缺少高度或背景数据')
            else:
                self.get_logger().error('  ❌ 参考库数据: 不可用')
                all_ok = False
            
            # 检查图像数据
            if self.latest_rgb_image is not None:
                self.get_logger().info(f'  ✅ RGB图像: {self.latest_rgb_image.shape}')
            else:
                self.get_logger().warn('  ⚠️ RGB图像: 暂无数据')
            
            if self.latest_depth_image is not None:
                self.get_logger().info(f'  ✅ 深度图像: {self.latest_depth_image.shape}')
            else:
                self.get_logger().warn('  ⚠️ 深度图像: 暂无数据')
            
            return all_ok
            
        except Exception as e:
            self.get_logger().error(f'系统组件验证失败: {e}')
            return False
    
    def _initialize_detection_pipeline_fixed(self):
        """初始化检测管道 - 修复YOLO参数问题"""
        try:
            # 找到正确的配置文件
            possible_config_paths = [
                '/home/qi/ros2_ws/src/vision_ai/vision_ai/detection/config/enhanced_detection_config.json',
                os.path.join(os.path.dirname(__file__), '..', 'detection', 'config', 'enhanced_detection_config.json'),
                os.path.join(os.path.expanduser('~'), 'ros2_ws', 'src', 'vision_ai', 'vision_ai', 'detection', 'config', 'enhanced_detection_config.json')
            ]
            
            config_file = None
            for path in possible_config_paths:
                if os.path.exists(path):
                    config_file = path
                    self.get_logger().info(f'✅ 找到检测配置文件: {config_file}')
                    break
            
            # if config_file is None:
            #     # 🔧 创建兼容的检测配置文件
            #     config_file = possible_config_paths[0]
            #     config_dir = os.path.dirname(config_file)
            #     os.makedirs(config_dir, exist_ok=True)
                
            #     # 🔧 修复：创建不包含iou_threshold的配置
            #     compatible_config = {
            #         "models": {
            #             "yolo": {
            #                 "model_path": "/home/qi/下载/best2.pt",
            #                 "confidence_threshold": 0.7,
            #                 "device": "cuda"
            #                 # 🔧 移除iou_threshold参数
            #             },
            #             "sam2": {
            #                 "model_config": "sam2_hiera_l.yaml",
            #                 "checkpoint_path": "/home/qi/ros2_ws/src/vision_ai/models/sam2/sam2_hiera_large.pt",
            #                 "device": "cuda"
            #             }
            #         },
            #         "features": {
            #             "color": {
            #                 "histogram_bins": 32
            #             },
            #             "shape": {
            #                 "enable_moments": True,
            #                 "enable_contour": True
            #             },
            #             "spatial": {
            #                 "enable_3d": True
            #             }
            #         },
            #         "camera": {
            #             "intrinsics": {
            #                 "fx": 912.694580078125,
            #                 "fy": 910.309814453125,
            #                 "cx": 640,
            #                 "cy": 360
            #             }
            #         },
            #         "processing": {
            #             "max_objects": 50,
            #             "min_area": 100
            #         }
            #     }
                
            #     with open(config_file, 'w', encoding='utf-8') as f:
            #         import json
            #         json.dump(compatible_config, f, indent=4, ensure_ascii=False)
                
            #     self.get_logger().info(f'✅ 已创建兼容的检测配置: {config_file}')
            
            # 🔧 在创建管道前，先验证并修复配置文件
            self._fix_detection_config_if_needed(config_file)
            
            # 创建增强检测管道
            from ..detection.enhanced_detection_pipeline import EnhancedDetectionPipeline
            
            self.detection_pipeline = EnhancedDetectionPipeline(
                config_file=config_file,
                output_dir=None
            )
            
            # 禁用3D后处理
            self.detection_pipeline.enable_3d_post_processing = False
            
            self.get_logger().info('✅ 增强检测管道初始化成功')
            
        except Exception as e:
            self.get_logger().error(f'❌ 初始化检测管道失败: {e}')

    def _fix_detection_config_if_needed(self, config_file: str):
        """修复检测配置文件中的问题参数"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 🔧 检查并移除有问题的YOLO参数
            yolo_config = config.get('models', {}).get('yolo', {})
            problematic_params = ['iou_threshold', 'nms_threshold', 'max_detections']
            
            config_changed = False
            for param in problematic_params:
                if param in yolo_config:
                    removed_value = yolo_config.pop(param)
                    self.get_logger().info(f'🔧 移除不支持的YOLO参数: {param}={removed_value}')
                    config_changed = True
            
            # 🔧 确保YOLO配置包含必需参数
            required_params = {
                'model_path': '/home/qi/下载/best2.pt',
                'confidence_threshold': 0.7,
                'device': 'cuda'
            }
            
            for param, default_value in required_params.items():
                if param not in yolo_config:
                    yolo_config[param] = default_value
                    self.get_logger().info(f'🔧 添加缺失的YOLO参数: {param}={default_value}')
                    config_changed = True
            
            # 如果配置有更改，保存文件
            if config_changed:
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=4, ensure_ascii=False)
                self.get_logger().info('✅ 检测配置文件已修复并保存')
            
        except Exception as e:
            self.get_logger().error(f'修复检测配置文件失败: {e}')

    def _verify_system_components(self) -> bool:
        """验证系统组件是否正常"""
        try:
            self.get_logger().info('🔧 验证系统组件...')
            
            # 检查核心组件
            components = [
                ('tracker', self.tracker),
                ('detection_pipeline', self.detection_pipeline),
                ('data_recorder', self.data_recorder),
            ]
            
            all_ok = True
            for name, component in components:
                if component is not None:
                    self.get_logger().info(f'  ✅ {name}: 已初始化')
                else:
                    self.get_logger().error(f'  ❌ {name}: 未初始化')
                    all_ok = False
            
            # 检查追踪目标
            if self.current_target_id:
                self.get_logger().info(f'  ✅ 追踪目标: {self.current_target_id}')
            else:
                self.get_logger().error('  ❌ 追踪目标: 未设置')
                all_ok = False
            
            # 检查图像数据
            if self.latest_rgb_image is not None:
                self.get_logger().info(f'  ✅ RGB图像: {self.latest_rgb_image.shape}')
            else:
                self.get_logger().warn('  ⚠️ RGB图像: 暂无数据')
            
            if self.latest_depth_image is not None:
                self.get_logger().info(f'  ✅ 深度图像: {self.latest_depth_image.shape}')
            else:
                self.get_logger().warn('  ⚠️ 深度图像: 暂无数据')
            
            return all_ok
            
        except Exception as e:
            self.get_logger().error(f'系统组件验证失败: {e}')
            return False

        
    def _initialize_detection_pipeline(self):
        """初始化实时检测管道 - 重定向到修复版本"""
        return self._initialize_detection_pipeline_fixed()

        
    def tcp_pose_callback(self, msg):
        """TCP位姿回调 - 缓存当前机械臂位姿"""
        try:
            # 🔧 修复：xarm_controller发布的位置已经是mm单位，无需再转换
            self.current_tcp_pose = {
                'position': {
                    'x': msg.pose.position.x,  # 已经是mm单位
                    'y': msg.pose.position.y,
                    'z': msg.pose.position.z
                },
                'orientation': {
                    'x': msg.pose.orientation.x,
                    'y': msg.pose.orientation.y,
                    'z': msg.pose.orientation.z,
                    'w': msg.pose.orientation.w
                },
                'timestamp': msg.header.stamp
            }
            
        except Exception as e:
            self.get_logger().error(f'处理TCP位姿失败: {e}')
    
    def _get_candidate_detections(self) -> list:
        """获取候选检测结果 - 使用增强管道版本"""
        try:
            if not self.detection_pipeline:
                self.get_logger().error('检测管道未初始化')
                return []
            
            if self.latest_rgb_image is None or self.latest_depth_image is None:
                self.get_logger().warn('图像数据不完整')
                return []
            
            # 🆕 额外的图像预处理确保格式正确
            rgb_processed = self.latest_rgb_image.copy()
            depth_processed = self.latest_depth_image.copy()
            
            # 确保图像尺寸匹配
            if rgb_processed.shape[:2] != depth_processed.shape:
                self.get_logger().warn('检测前再次调整深度图像尺寸')
                depth_processed = cv2.resize(
                    depth_processed, 
                    (rgb_processed.shape[1], rgb_processed.shape[0]), 
                    interpolation=cv2.INTER_LINEAR
                )
            
            # 确保数据类型正确
            if rgb_processed.dtype != np.uint8:
                rgb_processed = rgb_processed.astype(np.uint8)
            if depth_processed.dtype != np.uint16:
                depth_processed = depth_processed.astype(np.uint16)
            
            self.get_logger().info('🔍 执行实时检测...')
            self.get_logger().info(f'预处理后图像: RGB{rgb_processed.shape}, Depth{depth_processed.shape}')
            
            # 🔧 使用增强管道的process_single_image方法
            detection_result = self.detection_pipeline.process_single_image(
                image_rgb=rgb_processed,
                depth_image=depth_processed,
                camera_pose=self._get_current_camera_pose()
            )
            
            if not detection_result.get('objects'):
                self.get_logger().warn('实时检测未发现任何目标')
                return []
            
            # 🔧 转换为追踪器期望的格式
            candidates = []
            for obj in detection_result['objects']:
                candidate = {
                    'bounding_box': obj['bounding_box'],
                    'confidence': obj['confidence'],
                    'class_id': obj['class_id'],
                    'class_name': obj['class_name'],
                    'mask': obj['mask'],
                    
                    # 🔧 使用增强管道提取的特征（格式可能不同）
                    'geometric_features': obj['features'].get('geometric', {}),
                    'appearance_features': obj['features'].get('appearance', obj['features'].get('color', {})),
                    'shape_features': obj['features'].get('shape', {}),
                    'spatial_features': obj['features'].get('spatial', {})
                }
                candidates.append(candidate)
            
            self.get_logger().info(f'实时检测完成，发现 {len(candidates)} 个候选目标')
            return candidates
            
        except Exception as e:
            self.get_logger().error(f'实时检测失败: {e}')
            import traceback
            traceback.print_exc()
            return []
    
    def _get_current_camera_pose(self) -> dict:
        """获取当前相机位姿（用于detection_pipeline）"""
        try:
            if not self.current_tcp_pose:
                # 使用默认位姿
                return {
                    'world_pos': [0, 0, 350],
                    'roll': 179,
                    'pitch': 0,
                    'yaw': 0
                }
            
            # 从四元数转换为欧拉角
            orientation = self.current_tcp_pose['orientation']
            roll, pitch, yaw = self._quat_to_euler(
                orientation['x'], orientation['y'], 
                orientation['z'], orientation['w']
            )
            self.get_logger().info(f'当前位姿状态 :roll:{roll},pitch: {pitch}, yaw:{yaw} ')
            # 🔧 修复：位置已经是mm单位，直接使用
            return {
                'world_pos': [
                    self.current_tcp_pose['position']['x'],
                    self.current_tcp_pose['position']['y'],
                    self.current_tcp_pose['position']['z']
                ],
                'roll': roll,
                'pitch': pitch,
                'yaw': yaw
            }
            
        except Exception as e:
            self.get_logger().error(f'获取相机位姿失败: {e}')
            return {'world_pos': [0, 0, 350], 'roll': 179, 'pitch': 0, 'yaw': 0}
    
    def _quat_to_euler(self, qx, qy, qz, qw):
        """四元数转欧拉角（度）- 修复版，增强稳定性"""
        import math
        
        # 🔧 使用更稳定的转换算法，避免万向节锁问题
        # 参考ROS tf2和scipy的实现
        
        # 预处理：确保四元数归一化
        norm = math.sqrt(qx*qx + qy*qy + qz*qz + qw*qw)
        if norm > 0:
            qx, qy, qz, qw = qx/norm, qy/norm, qz/norm, qw/norm
        
        # 🔧 使用更稳定的atan2计算，适合xarm坐标系
        # Roll (X轴旋转)
        sinr_cosp = 2 * (qw * qx + qy * qz)
        cosr_cosp = 1 - 2 * (qx * qx + qy * qy)
        roll = math.atan2(sinr_cosp, cosr_cosp)
        
        # Pitch (Y轴旋转) - 使用clamp避免数值误差
        sinp = 2 * (qw * qy - qz * qx)
        sinp = max(-1.0, min(1.0, sinp))  # clamp到[-1,1]
        pitch = math.asin(sinp)
        
        # Yaw (Z轴旋转) - 🔧 关键修复点
        siny_cosp = 2 * (qw * qz + qx * qy)
        cosy_cosp = 1 - 2 * (qy * qy + qz * qz)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        
        # 转换为度
        roll_deg = math.degrees(roll)
        pitch_deg = math.degrees(pitch)
        yaw_deg = math.degrees(yaw)
        
        # 🆕 yaw角度连续性处理，避免-180°到180°的跳跃
        if self.previous_yaw is not None:
            yaw_diff = yaw_deg - self.previous_yaw
            
            # 处理跨越±180°的情况
            if yaw_diff > 180:
                yaw_deg -= 360
            elif yaw_diff < -180:
                yaw_deg += 360
            
            # 🔧 如果角度变化过大（>90°），可能是计算错误，使用上一次的值
            if abs(yaw_deg - self.previous_yaw) > 90:
                self.get_logger().warn(f'yaw角度变化过大: {self.previous_yaw:.1f}° -> {yaw_deg:.1f}°，使用上次值')
                yaw_deg = self.previous_yaw
        
        # 更新previous_yaw
        self.previous_yaw = yaw_deg
        
        # 🔧 角度范围标准化到[-180, 180]
        roll_deg = ((roll_deg + 180) % 360) - 180
        pitch_deg = ((pitch_deg + 180) % 360) - 180  
        yaw_deg = ((yaw_deg + 180) % 360) - 180
        
        return roll_deg, pitch_deg, yaw_deg
    
    def _get_current_waypoint_data(self) -> dict:
        """获取当前waypoint数据 - 基于实际TCP位姿"""
        try:
            if not self.current_tcp_pose:
                self.get_logger().warn('TCP位姿数据不可用，使用默认值')
                return {
                    'world_pos': [0, 0, 350],
                    'roll': 179,
                    'pitch': 0,
                    'yaw': 0
                }
            
            # 从缓存的TCP位姿构建waypoint数据
            camera_pose = self._get_current_camera_pose()
            
            waypoint_data = {
                'world_pos': camera_pose['world_pos'],
                'roll': camera_pose['roll'],
                'pitch': camera_pose['pitch'],
                'yaw': camera_pose['yaw'],
                'timestamp': self.current_tcp_pose['timestamp']
            }
            
            return waypoint_data
            
        except Exception as e:
            self.get_logger().error(f'获取waypoint数据失败: {e}')
            return {'world_pos': [0, 0, 350], 'roll': 179, 'pitch': 0, 'yaw': 0}
    
    def _handle_tracking_success(self, tracking_result: dict):
        """处理追踪成功 - 增加循环控制"""
        try:
            self.get_logger().info('✅ 追踪成功')
            
            # 显示详细追踪信息
            self._log_tracking_details(tracking_result)
            
            # 发布追踪结果给机械臂（25%移动策略）
            self._publish_target_pose(tracking_result)
            
            # 记录追踪数据
            self.data_recorder.record_tracking_step(
                self.current_target_id,
                tracking_result,
                self.latest_rgb_image,
                self.latest_depth_image
            )
            
            # 更新追踪计数
            self.tracking_count += 1
            
            # 🆕 检查是否达到最大步数
            if self.tracking_count >= self.max_tracking_steps:
                self.get_logger().info(f'🎯 已完成 {self.tracking_count} 步追踪，达到最大步数')
                self._finish_tracking_session()
                return  # 🔧 重要：立即返回，停止继续处理
            
            # 发布状态
            self._publish_tracking_status('tracking_success', tracking_result)
            
            # 🆕 暂停追踪，等待机械臂移动完成
            self.movement_complete = False
            self.get_logger().info(f'⏳ 等待机械臂移动到目标位置... (步数: {self.tracking_count}/{self.max_tracking_steps})')
            
        except Exception as e:
            self.get_logger().error(f'处理追踪成功失败: {e}')
    
    def _log_tracking_details(self, tracking_result: dict):
        """记录详细追踪信息 - 修复版"""
        try:
            self.get_logger().info(f'🎯 追踪详情:')
            self.get_logger().info(f'  目标ID: {tracking_result["target_id"]}')
            self.get_logger().info(f'  追踪置信度: {tracking_result["tracking_confidence"]:.3f}')
            self.get_logger().info(f'  检测置信度: {tracking_result["detection_confidence"]:.3f}')
            
            grasp_coord = tracking_result['grasp_coordinate']
            self.get_logger().info(f'  目标坐标: ({grasp_coord["x"]:.1f}, {grasp_coord["y"]:.1f}, {grasp_coord["z"]:.1f}mm)')

            object_info = tracking_result['object_info']
            self.get_logger().info(f'  物体高度: {object_info["estimated_height"]:.1f}mm')
            self.get_logger().info(f'  背景高度: {object_info["background_z"]:.1f}mm')
            self.get_logger().info(f'  推荐夹爪宽度: {object_info["recommended_gripper_width"]}')
            
            # 🔧 修复：安全地显示特征相似度分解
            similarity_breakdown = tracking_result.get('similarity_breakdown', {})
            if similarity_breakdown:
                self.get_logger().info('  特征相似度分解:')
                
                for feature_type, similarity_data in similarity_breakdown.items():
                    try:
                        # 🆕 处理不同类型的相似度数据
                        if isinstance(similarity_data, dict):
                            # 如果是字典，查找关键的数值字段
                            if 'contribution' in similarity_data:
                                score = similarity_data['contribution']
                                self.get_logger().info(f'    {feature_type}: {score:.3f} (贡献度)')
                            elif 'average_score' in similarity_data:
                                score = similarity_data['average_score']
                                self.get_logger().info(f'    {feature_type}: {score:.3f} (平均分)')
                            else:
                                # 显示字典内容摘要
                                keys = list(similarity_data.keys())[:3]  # 只显示前3个键
                                self.get_logger().info(f'    {feature_type}: dict包含 {keys}...')
                        
                        elif isinstance(similarity_data, (int, float)):
                            # 如果是数字，直接显示
                            self.get_logger().info(f'    {feature_type}: {similarity_data:.3f}')
                        
                        elif isinstance(similarity_data, list):
                            # 如果是列表，显示长度和均值
                            if len(similarity_data) > 0 and all(isinstance(x, (int, float)) for x in similarity_data):
                                avg_score = sum(similarity_data) / len(similarity_data)
                                self.get_logger().info(f'    {feature_type}: {avg_score:.3f} (均值, 共{len(similarity_data)}项)')
                            else:
                                self.get_logger().info(f'    {feature_type}: list包含{len(similarity_data)}项')
                        
                        else:
                            # 其他类型，显示类型信息
                            self.get_logger().info(f'    {feature_type}: {type(similarity_data).__name__}')
                            
                    except Exception as e:
                        self.get_logger().warn(f'    {feature_type}: 显示失败 ({e})')
            
            # 🆕 显示详细特征分解（如果有）
            detailed_breakdown = tracking_result.get('detailed_similarity_breakdown', {})
            if detailed_breakdown:
                self.get_logger().info('  详细特征分解:')
                
                for feature_category, feature_details in detailed_breakdown.items():
                    try:
                        if isinstance(feature_details, dict) and len(feature_details) > 0:
                            # 计算该类别的平均分数
                            numeric_scores = []
                            for key, value in feature_details.items():
                                if isinstance(value, (int, float)):
                                    numeric_scores.append(value)
                            
                            if numeric_scores:
                                avg_score = sum(numeric_scores) / len(numeric_scores)
                                self.get_logger().info(f'    {feature_category}: {avg_score:.3f} (平均, {len(numeric_scores)}个特征)')
                            else:
                                self.get_logger().info(f'    {feature_category}: {len(feature_details)}个特征')
                                
                    except Exception as e:
                        self.get_logger().warn(f'    {feature_category}: 处理失败 ({e})')
            
            # 🆕 显示最小外接矩形信息（如果有）
            bounding_rect = tracking_result.get('bounding_rect', {})
            if bounding_rect and bounding_rect.get('width', 0) > 0:
                self.get_logger().info(f'  最小外接矩形: {bounding_rect["width"]:.1f}x{bounding_rect["height"]:.1f}像素, 角度{bounding_rect["angle"]:.1f}°')
                        
        except Exception as e:
            self.get_logger().error(f'记录追踪详情失败: {e}')
            import traceback
            traceback.print_exc()
    
    def _load_tracking_target(self) -> str:
        """从tracking_selection.txt加载用户选择的追踪目标 - 简化版"""
        try:
            selection_file = os.path.join(
                self.current_scan_dir, 
                'enhanced_detection_results', 
                'tracking_selection.txt'
            )
            
            if not os.path.exists(selection_file):
                self.get_logger().error(f'追踪选择文件不存在: {selection_file}')
                return None
            
            with open(selection_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析文件内容，提取目标ID
            target_id = None
            lines = content.strip().split('\n')
            for line in lines:
                if 'ID:' in line and ')' in line:
                    # 格式：- Description (ID: target_id)
                    start = line.find('ID:') + 3
                    end = line.find(')', start)
                    if start < end:
                        target_id = line[start:end].strip()
                        self.get_logger().info(f'📌 找到追踪目标: {target_id}')
                        break
            
            if not target_id:
                self.get_logger().error('无法从选择文件中解析目标ID')
                return None
            
            return target_id
            
        except Exception as e:
            self.get_logger().error(f'加载追踪目标失败: {e}')
            return None

    def _initialize_auxiliary_components(self):
        """初始化辅助组件 - 详细版本"""
        try:
            self.get_logger().info('🔧 初始化辅助组件...')
            
            # 用户配置管理器
            self.user_profile_manager = UserProfileManager(self.current_user_id)
            self.get_logger().info('  ✅ 用户配置管理器')
            
            # 数据记录器
            if self._initialize_data_recorder():
                self.get_logger().info('  ✅ 数据记录器')
            else:
                self.get_logger().warn('  ⚠️ 数据记录器: 使用备用模式')
            
            # 反馈收集器
            self.feedback_collector = FeedbackCollector(self.get_logger())
            self.get_logger().info('  ✅ 反馈收集器')
            
            # 追踪可视化器
            self.visualizer = TrackingVisualizer()
            self.get_logger().info('  ✅ 追踪可视化器')
            
            # 在线学习器
            self.online_learner = OnlineLearner(
                self.current_user_id or "default_user",
                self.tracker.similarity_calculator
            )
            self.get_logger().info('  ✅ 在线学习器')
            
            self.get_logger().info('✅ 辅助组件初始化完成')
            
        except Exception as e:
            self.get_logger().error(f'辅助组件初始化失败: {e}')
            self._create_fallback_components()

    def _initialize_data_recorder(self) -> bool:
        """初始化数据记录器"""
        try:
            if self.current_scan_dir and self.current_user_id:
                self.data_recorder = DataRecorder(
                    self.current_user_id, 
                    self.current_scan_dir
                )
                return True
            else:
                # 创建备用数据记录器
                self.data_recorder = self._create_fallback_recorder()
                return False
                
        except Exception as e:
            self.get_logger().error(f'数据记录器初始化失败: {e}')
            self.data_recorder = self._create_fallback_recorder()
            return False

    def _create_fallback_components(self):
        """创建备用组件"""
        try:
            if self.data_recorder is None:
                self.data_recorder = self._create_fallback_recorder()
            
            if self.feedback_collector is None:
                class FallbackFeedbackCollector:
                    def __init__(self, logger):
                        self.logger = logger
                    def collect_feedback(self, prompt):
                        self.logger.info(f'备用反馈收集器: {prompt}')
                        return True  # 默认正确
                
                self.feedback_collector = FallbackFeedbackCollector(self.get_logger())
                
        except Exception as e:
            self.get_logger().error(f'创建备用组件失败: {e}')


    def rgb_image_callback(self, msg):
        """RGB图像回调 - 修复确认等待逻辑"""
        try:
            # 处理RGB图像
            try:
                color_cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
                
                if len(color_cv_image.shape) == 3 and color_cv_image.shape[2] == 3:
                    color_rgb = cv2.cvtColor(color_cv_image, cv2.COLOR_BGR2RGB)
                else:
                    self.get_logger().error(f'不支持的彩色图像格式: {color_cv_image.shape}')
                    return
                    
                self.latest_rgb_image = color_rgb
                self.get_logger().debug(f'RGB图像已更新: {color_rgb.shape}')
                    
            except Exception as color_error:
                self.get_logger().error(f'RGB图像转换失败: {color_error}')
                return
            
            # 🔧 修复：只有在系统完全初始化且不在等待确认状态时才执行追踪
            if (self.system_initialized and 
                self.tracking_active and 
                not self.waiting_for_user_confirmation and  # 🆕 关键修复
                self.latest_depth_image is not None and 
                self.tracking_count < self.max_tracking_steps and
                self.movement_complete):  # 🆕 确保机械臂移动完成
                
                current_time = time.time()
                if not hasattr(self, '_last_tracking_time'):
                    self._last_tracking_time = 0
                
                if current_time - self._last_tracking_time >= 0.5:
                    self._last_tracking_time = current_time
                    self._execute_tracking_step()
            
            # 检查是否达到最大步数
            elif self.tracking_count >= self.max_tracking_steps and self.tracking_active:
                self.get_logger().info('🏁 已达到最大追踪步数，停止追踪')
                self._finish_tracking_session()
            
            # 显示系统状态（仅在等待时）
            elif self.waiting_for_detection_complete:
                current_time = time.time()
                if not hasattr(self, '_last_status_time'):
                    self._last_status_time = current_time
                
                if current_time - self._last_status_time >= 10.0:
                    self._last_status_time = current_time
                    self.get_logger().info('⏳ 系统就绪，等待检测完成信号...')
                    
        except Exception as e:
            self.get_logger().error(f'RGB图像处理失败: {e}')

    def depth_image_callback(self, msg):
        """深度图像回调 - 总是处理深度图像用于系统监控"""
        try:
            # 🔧 完全采用scan_executor的深度处理逻辑
            try:
                self.get_logger().debug(f'接收深度消息编码: {msg.encoding}')
                
                # 直接从原始字节数据重建16位深度图像
                if msg.step == msg.width * 2:  # 正确的16位步长
                    raw_data = np.frombuffer(msg.data, dtype=np.uint16)
                    depth_raw = raw_data.reshape((msg.height, msg.width))
                    self.get_logger().debug('使用直接uint16重建')
                else:
                    raw_data = np.frombuffer(msg.data, dtype=np.uint8)
                    depth_raw = raw_data.view(np.uint16).reshape((msg.height, msg.width))
                    self.get_logger().debug('使用uint8->uint16重新解释')
                
                self.get_logger().debug(f'深度图像: {depth_raw.shape}, dtype: {depth_raw.dtype}')
                self.get_logger().debug(f'深度范围: min={depth_raw.min()}, max={depth_raw.max()}')
                    
            except Exception as depth_error:
                self.get_logger().error(f'直接深度重建失败: {depth_error}')
                try:
                    depth_raw = self.bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
                    if depth_raw.dtype != np.uint16:
                        depth_raw = depth_raw.astype(np.uint16)
                    self.get_logger().debug('降级到cv_bridge转换')
                except Exception as fallback_error:
                    self.get_logger().error(f'所有深度转换方法都失败: {fallback_error}')
                    return
            
            # 检查并修正深度图像分辨率
            expected_width, expected_height = 1280, 720
            if depth_raw.shape != (expected_height, expected_width):
                depth_raw = cv2.resize(
                    depth_raw, 
                    (expected_width, expected_height), 
                    interpolation=cv2.INTER_LINEAR
                )
            
            # 🔧 修复：正确的深度数据合理性验证
            depth_min, depth_max = depth_raw.min(), depth_raw.max()
            
            # 合理的深度范围验证（静默处理）
            if depth_max == 0:
                self.get_logger().debug('深度数据全为0')
            elif depth_max > 10000:
                self.get_logger().debug(f'深度值较大: max={depth_max}mm')
            elif depth_max < 50:
                self.get_logger().debug(f'深度值较小: max={depth_max}mm')
            else:
                self.get_logger().debug(f'深度范围正常: {depth_min}mm - {depth_max}mm')
            
            self.latest_depth_image = depth_raw
            
        except Exception as e:
            self.get_logger().error(f'深度图像处理失败: {e}')
    
    def movement_complete_callback(self, msg):
        """机械臂移动完成回调 - 修复版"""
        try:
            self.get_logger().info('🤖 机械臂移动完成')
            self.movement_complete = True
            
            # 🆕 移动完成后，如果追踪仍然激活，准备下一步
            if self.tracking_active and self.tracking_count < self.max_tracking_steps:
                self.get_logger().info('✅ 准备进行下一步追踪')
            elif self.tracking_count >= self.max_tracking_steps:
                self.get_logger().info('🏁 已完成所有追踪步骤')
                self._finish_tracking_session()
                
        except Exception as e:
            self.get_logger().error(f'处理移动完成信号失败: {e}')
    
    def _execute_tracking_step(self):
        """执行单步追踪 - 修复版：追踪→确认→记录→移动"""
        try:
            self.get_logger().info(f'🔍 执行第 {self.tracking_count + 1} 步追踪')
            
            # 验证图像数据
            if not self._validate_image_data():
                self.get_logger().error('图像数据验证失败，跳过追踪')
                return
            
            # 记录图像信息用于调试
            self.get_logger().info(f'📊 图像信息:')
            self.get_logger().info(f'  RGB: {self.latest_rgb_image.shape}, dtype: {self.latest_rgb_image.dtype}')
            self.get_logger().info(f'  Depth: {self.latest_depth_image.shape}, dtype: {self.latest_depth_image.dtype}')
            self.get_logger().info(f'  Depth range: {self.latest_depth_image.min()}-{self.latest_depth_image.max()}')
            
            # 获取候选检测结果
            candidate_detections = self._get_candidate_detections()
            
            if not candidate_detections:
                self.get_logger().warn('⚠️ 未检测到候选目标')
                self._handle_tracking_failure()
                return
            
            # 使用增强追踪器进行匹配
            waypoint_data = self._get_current_waypoint_data()
            
            # 验证waypoint数据
            self.get_logger().info(f'📍 当前waypoint数据: {waypoint_data}')
            
            tracking_result = self.tracker.track_target(
                self.current_target_id,
                self.latest_rgb_image,
                self.latest_depth_image,
                waypoint_data,
                candidate_detections
            )
            
            if tracking_result:
                # 🆕 修复：等待用户确认，而不是直接移动
                self._handle_tracking_success_with_confirmation(tracking_result)
            else:
                self._handle_tracking_failure()
                
        except Exception as e:
            self.get_logger().error(f'追踪步骤执行失败: {e}')
            import traceback
            traceback.print_exc()

    # tracking_node.py
    def _handle_tracking_success_with_confirmation(self, tracking_result: dict):
        """处理追踪成功 - 添加抓取条件判断"""
        try:
            self.get_logger().info('✅ 追踪成功，分析抓取条件')
            
            # 显示详细追踪信息
            self._log_tracking_details(tracking_result)
            
            # 🆕 计算移动策略（用于抓取条件判断）
            movement_strategy = self._calculate_adaptive_movement_strategy(
                self.current_tcp_pose, 
                tracking_result['grasp_coordinate'], 
                tracking_result['object_info']
            )
            
            # 🆕 评估抓取条件
            grasp_conditions = self._evaluate_grasp_conditions(tracking_result, movement_strategy)
            
            if grasp_conditions['grasp_ready']:
                # 满足抓取条件，生成抓取信息文件
                self.get_logger().info('🎯 满足抓取条件，准备抓取')
                
                bounding_rect = tracking_result.get('bounding_rect', {})
                grasp_filename = self._generate_grasp_info_file(tracking_result, bounding_rect)
                
                if grasp_filename:
                    # 发布抓取触发信号
                    self._publish_grasp_trigger(grasp_filename, tracking_result['grasp_coordinate'])
                    
                    # 🆕 标记追踪完成
                    self.tracking_active = False
                    self._finish_tracking_session()
                    return  # 🔧 抓取触发后结束追踪
            
            # 不满足抓取条件，继续追踪流程
            self.get_logger().info('⏳ 未满足抓取条件，继续追踪')
            
            # 继续原有确认流程
            self.current_tracking_result = tracking_result
            self.waiting_for_user_confirmation = True
            self.user_feedback_received = False
            
            self._start_command_input_thread()
            
        except Exception as e:
            self.get_logger().error(f'处理追踪成功失败: {e}')

    def _generate_grasp_info_file(self, tracking_result: dict, bounding_rect: dict) -> str:
        """生成抓取信息文件"""
        try:
            import time
            
            grasp_info = {
                'target_id': tracking_result['target_id'],
                'object_coordinate': tracking_result['grasp_coordinate'],
                'background_height': tracking_result['object_info']['background_z'],
                'object_height': tracking_result['object_info']['estimated_height'],
                'object_width': tracking_result['object_info'].get('estimated_width', 50),
                'bounding_rect': bounding_rect,
                'recommended_gripper_width': tracking_result['object_info']['recommended_gripper_width'],
                'tracking_confidence': tracking_result['tracking_confidence'],
                'detection_confidence': tracking_result['detection_confidence']
            }
            
            # 保存文件
            filename = f"grasp_info_{tracking_result['target_id']}_{int(time.time())}.json"
            filepath = os.path.join(self.current_scan_dir, 'grasp_commands', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(grasp_info, f, indent=2, ensure_ascii=False)
            
            self.get_logger().info(f'💾 抓取信息文件已生成: {filename}')
            return filename
            
        except Exception as e:
            self.get_logger().error(f'生成抓取信息文件失败: {e}')
            return None
        
    def _extract_tracking_parameters(self, tracking_result: dict) -> dict:
        """提取并记录追踪参数 - 修复版，确保特征数据传递"""
        try:
            grasp_coord = tracking_result['grasp_coordinate']
            object_info = tracking_result['object_info']
            
            # 🆕 正确提取细粒度特征数据
            detailed_features = tracking_result.get('detailed_similarity_breakdown', {})
            similarity_breakdown = tracking_result.get('similarity_breakdown', {})
            feature_weights = tracking_result.get('feature_weights_used', {})
            
            # 🆕 调试输出
            print(f"[TRACKING_PARAMS] 提取特征数据:")
            print(f"  detailed_features keys: {list(detailed_features.keys())}")
            print(f"  similarity_breakdown keys: {list(similarity_breakdown.keys())}")
            print(f"  feature_weights keys: {list(feature_weights.keys())}")
            
            # 计算最小外接矩形
            bbox_info = tracking_result.get('bounding_rect', {})
            
            # 计算当前姿态
            current_pose = self._get_current_camera_pose()
            
            tracking_params = {
                'step': self.tracking_count + 1,
                'timestamp': datetime.now().isoformat(),
                'target_coordinate': {
                    'x': grasp_coord['x'],
                    'y': grasp_coord['y'], 
                    'z': grasp_coord['z']
                },
                'current_tcp_pose': current_pose,
                'object_properties': {
                    'height': object_info.get('estimated_height', 30.0),
                    'recommended_gripper_width': object_info.get('recommended_gripper_width', 150),
                    'class_name': object_info.get('class_name', 'unknown')
                },
                'bounding_rect': bbox_info,
                'tracking_confidence': tracking_result['tracking_confidence'],
                'detection_confidence': tracking_result['detection_confidence'],
                
                # 🆕 确保特征数据正确传递
                'detailed_features': detailed_features,
                'similarity_breakdown': similarity_breakdown,
                'feature_weights_used': feature_weights
            }
            
            print(f"[TRACKING_PARAMS] 最终参数包含 detailed_features: {len(tracking_params['detailed_features'])} 项")
            print(f"[TRACKING_PARAMS] 最终参数包含 similarity_breakdown: {len(tracking_params['similarity_breakdown'])} 项")
            
            return tracking_params
            
        except Exception as e:
            self.get_logger().error(f'提取追踪参数失败: {e}')
            import traceback
            traceback.print_exc()
            return {}

    def _display_tracking_parameters(self, params: dict):
        """显示追踪参数"""
        try:
            self.get_logger().info('📋 当前追踪参数:')
            self.get_logger().info(f'  步骤: {params.get("step", "未知")}')
            
            target_coord = params.get('target_coordinate', {})
            self.get_logger().info(f'  目标坐标: ({target_coord.get("x", 0):.1f}, {target_coord.get("y", 0):.1f}, {target_coord.get("z", 0):.1f}mm)')
            
            obj_props = params.get('object_properties', {})
            self.get_logger().info(f'  物体高度: {obj_props.get("height", 0):.1f}mm')
            self.get_logger().info(f'  推荐夹爪宽度: {obj_props.get("recommended_gripper_width", 0)}')
            
            self.get_logger().info(f'  追踪置信度: {params.get("tracking_confidence", 0):.3f}')
            self.get_logger().info(f'  检测置信度: {params.get("detection_confidence", 0):.3f}')
            
        except Exception as e:
            self.get_logger().error(f'显示追踪参数失败: {e}')

    def _start_command_input_thread(self):
        """启动命令行输入线程"""
        try:
            if self.command_input_thread and self.command_input_thread.is_alive():
                return  # 已有输入线程在运行
            
            self.command_input_thread = threading.Thread(
                target=self._command_input_worker,
                daemon=True
            )
            self.command_input_thread.start()
            
        except Exception as e:
            self.get_logger().error(f'启动命令输入线程失败: {e}')

    def _command_input_worker(self):
        """命令行输入工作线程"""
        try:
            print(f"\n{'='*60}")
            print(f"🎯 追踪步骤 {self.tracking_count + 1} - 请确认追踪结果")
            print(f"{'='*60}")
            print("📋 当前追踪结果:")
            
            if self.current_tracking_result:
                grasp_coord = self.current_tracking_result['grasp_coordinate']
                print(f"  🎯 目标坐标: ({grasp_coord['x']:.1f}, {grasp_coord['y']:.1f}, {grasp_coord['z']:.1f}mm)")
                print(f"  🔍 追踪置信度: {self.current_tracking_result['tracking_confidence']:.3f}")
            
            print(f"\n💬 命令选项:")
            print(f"  's' 或 'success' - 确认追踪成功，继续移动")
            print(f"  'f' 或 'fail'    - 标记追踪失败")
            print(f"  'q' 或 'quit'    - 退出追踪")
            print(f"{'='*60}")
            
            while self.waiting_for_user_confirmation and not self.user_feedback_received:
                try:
                    user_input = input("请输入命令 (s/f/q): ").strip().lower()
                    
                    if user_input in ['s', 'success']:
                        self._handle_user_confirmation(True)
                        break
                    elif user_input in ['f', 'fail']:
                        self._handle_user_confirmation(False)
                        break
                    elif user_input in ['q', 'quit']:
                        self._handle_quit_request()
                        break
                    else:
                        print("❌ 无效输入，请输入 's'(成功), 'f'(失败), 或 'q'(退出)")
                        
                except (EOFError, KeyboardInterrupt):
                    print("\n🛑 用户中断输入")
                    self._handle_quit_request()
                    break
                except Exception as e:
                    print(f"❌ 输入处理错误: {e}")
                    
        except Exception as e:
            self.get_logger().error(f'命令输入工作线程失败: {e}')

    def _handle_user_confirmation(self, success: bool):
        """处理用户确认"""
        try:
            self.user_feedback_received = True
            
            if success:
                self.get_logger().info('✅ 用户确认追踪成功，开始移动')
                
                # 🆕 记录追踪参数到历史
                if self.current_tracking_result:
                    tracking_params = self._extract_tracking_parameters(self.current_tracking_result)
                    tracking_params['user_feedback'] = 'success'
                    self.tracking_parameters_history.append(tracking_params)
                
                # 🆕 保存当前步骤数据
                self._save_tracking_step_data(self.current_tracking_result, success)
                
                # 检查姿态变化并发布移动指令
                if self._validate_pose_change(self.current_tracking_result):
                    self._publish_target_pose(self.current_tracking_result)
                    self.tracking_count += 1
                else:
                    self.get_logger().warn('❌ 姿态变化超过限制，跳过移动')
                    
            else:
                self.get_logger().info('❌ 用户标记追踪失败')
                
                # 记录失败
                if self.current_tracking_result:
                    tracking_params = self._extract_tracking_parameters(self.current_tracking_result)
                    tracking_params['user_feedback'] = 'failure'
                    self.tracking_parameters_history.append(tracking_params)
                
                self._save_tracking_step_data(self.current_tracking_result, success)
                
                # 可以选择重试或继续下一步
                self.tracking_count += 1
            
            # 重置确认状态
            self.waiting_for_user_confirmation = False
            self.current_tracking_result = None
            
            # 检查是否完成所有步骤
            if self.tracking_count >= self.max_tracking_steps:
                self._finish_tracking_session()
                
        except Exception as e:
            self.get_logger().error(f'处理用户确认失败: {e}')

    def _validate_pose_change(self, tracking_result: dict) -> bool:
        """验证姿态变化是否在允许范围内"""
        try:
            current_pose = self._get_current_camera_pose()
            current_yaw = current_pose.get('yaw', 0)
            
            # 🆕 记录初始yaw角度
            if self.initial_yaw is None:
                self.initial_yaw = current_yaw
                self.get_logger().info(f'📐 记录初始yaw角度: {self.initial_yaw:.1f}°')
                return True
            
            # 🆕 检查yaw变化是否超过限制
            yaw_change = abs(current_yaw - self.initial_yaw)
            
            # 处理角度跨越180度的情况
            if yaw_change > 180:
                yaw_change = 360 - yaw_change
            
            if yaw_change > self.max_yaw_change:
                self.get_logger().warn(
                    f'⚠️ yaw角度变化过大: {yaw_change:.1f}° > {self.max_yaw_change}° '
                    f'(初始: {self.initial_yaw:.1f}°, 当前: {current_yaw:.1f}°)'
                )
                return False
            else:
                self.get_logger().info(f'✅ yaw角度变化正常: {yaw_change:.1f}°')
                return True
                
        except Exception as e:
            self.get_logger().error(f'验证姿态变化失败: {e}')
            return True  # 异常时允许移动

    def _save_tracking_step_data(self, tracking_result: dict, success: bool):
        """保存追踪步骤数据 - 修复版，传递详细特征"""
        try:
            if not self.data_recorder:
                self.get_logger().warn('数据记录器未初始化，无法保存数据')
                return
            
            # 🔧 提取详细特征数据
            detailed_features = tracking_result.get('detailed_similarity_breakdown', {})
            
            # 🔧 将user_feedback信息合并到tracking_result中
            enhanced_tracking_result = tracking_result.copy()
            enhanced_tracking_result['user_feedback'] = 'success' if success else 'failure'
            enhanced_tracking_result['feedback_timestamp'] = datetime.now().isoformat()
            
            # 🆕 调用修改后的记录方法，传递详细特征
            self.data_recorder.record_tracking_step(
                self.current_target_id,
                enhanced_tracking_result,
                self.latest_rgb_image,
                self.latest_depth_image,
                detailed_features  # 🆕 传递详细特征
            )
            
            # 保存追踪参数历史到文件
            self._save_parameters_history()
            
        except Exception as e:
            self.get_logger().error(f'保存追踪步骤数据失败: {e}')
            import traceback
            traceback.print_exc()

    def _save_parameters_history(self):
        """保存追踪参数历史到文件"""
        try:
            if not self.current_scan_dir:
                return
            
            output_dir = os.path.join(self.current_scan_dir, 'tracking_results')
            os.makedirs(output_dir, exist_ok=True)
            
            params_file = os.path.join(output_dir, 'tracking_parameters_history.json')
            
            with open(params_file, 'w', encoding='utf-8') as f:
                json.dump(self.tracking_parameters_history, f, indent=2, ensure_ascii=False)
            
            self.get_logger().info(f'💾 追踪参数历史已保存: {params_file}')
            
        except Exception as e:
            self.get_logger().error(f'保存参数历史失败: {e}')

    def _handle_quit_request(self):
        """处理退出请求"""
        try:
            self.get_logger().info('🛑 用户请求退出追踪')
            
            # 保存当前数据
            if self.current_tracking_result:
                tracking_params = self._extract_tracking_parameters(self.current_tracking_result)
                tracking_params['user_feedback'] = 'quit'
                self.tracking_parameters_history.append(tracking_params)
            
            self._save_parameters_history()
            
            # 停止追踪
            self.tracking_active = False
            self.waiting_for_user_confirmation = False
            self.user_feedback_received = True
            
            # 完成会话
            self._finish_tracking_session()
            
        except Exception as e:
            self.get_logger().error(f'处理退出请求失败: {e}')


    def _validate_image_data(self):
        """验证图像数据的完整性和格式 - 增强版"""
        try:
            if self.latest_rgb_image is None:
                self.get_logger().warn('RGB图像数据为空')
                return False
                
            if self.latest_depth_image is None:
                self.get_logger().warn('深度图像数据为空')
                return False
            
            # 检查RGB图像格式
            if len(self.latest_rgb_image.shape) != 3 or self.latest_rgb_image.shape[2] != 3:
                self.get_logger().error(f'RGB图像格式错误: {self.latest_rgb_image.shape}')
                return False
            
            # 检查深度图像格式
            if len(self.latest_depth_image.shape) != 2:
                self.get_logger().error(f'深度图像格式错误: {self.latest_depth_image.shape}')
                return False
            
            # 🔧 严格检查图像尺寸必须匹配
            rgb_height, rgb_width = self.latest_rgb_image.shape[:2]
            depth_height, depth_width = self.latest_depth_image.shape
            
            if (rgb_height, rgb_width) != (depth_height, depth_width):
                self.get_logger().error(f'❌ RGB和深度图像尺寸不匹配: RGB({rgb_height}, {rgb_width}) vs Depth({depth_height}, {depth_width})')
                
                # 🆕 尝试在这里再次调整深度图像分辨率
                try:
                    self.latest_depth_image = cv2.resize(
                        self.latest_depth_image, 
                        (rgb_width, rgb_height), 
                        interpolation=cv2.INTER_LINEAR
                    )
                    self.get_logger().info(f'✅ 深度图像已紧急调整到: {self.latest_depth_image.shape}')
                except Exception as resize_error:
                    self.get_logger().error(f'紧急调整深度图像失败: {resize_error}')
                    return False
            
            # 检查深度数据合理性
            if self.latest_depth_image.max() < 100:
                self.get_logger().warn(f'深度值异常小: max={self.latest_depth_image.max()}')
            
            self.get_logger().debug('✅ 图像数据验证通过')
            return True
            
        except Exception as e:
            self.get_logger().error(f'图像数据验证失败: {e}')
            return False
 
    def _handle_tracking_failure(self):
        """处理追踪失败 - 修复记录错误"""
        try:
            self.get_logger().warn('⚠️ 追踪失败')
            
            # 🔧 确保data_recorder存在
            if self.data_recorder is not None:
                self.data_recorder.record_tracking_failure(
                    self.current_target_id,
                    self.latest_rgb_image,
                    self.latest_depth_image
                )
            else:
                self.get_logger().warn('data_recorder未初始化，跳过失败记录')
            
            # 发布失败状态
            self._publish_tracking_status('tracking_failed', None)
            
            # 重置移动完成标志，等待用户干预
            self.movement_complete = True
            
        except Exception as e:
            self.get_logger().error(f'处理追踪失败失败: {e}')

    
    def _setup_movement_monitoring(self):
        """设置运动监听 - 参考scan_executor的逻辑"""
        try:
            # 🔧 仿照scan_executor的运动监听
            self.movement_start_time = time.time()
            self.movement_completed = False
            
            # 🔧 启动运动完成检查定时器（类似scan_executor）
            if hasattr(self, 'movement_check_timer'):
                self.movement_check_timer.destroy()
            
            self.movement_check_timer = self.create_timer(0.5, self.check_movement_completion)
            
            self.get_logger().info('🤖 开始监听机械臂运动完成...')
            
        except Exception as e:
            self.get_logger().error(f'设置运动监听失败: {e}')   

    def check_movement_completion(self):
        """检查运动完成 - 参考scan_executor的检查逻辑"""
        try:
            # 🔧 超时检查 (50秒，scan_executor的超时时间)
            if time.time() - self.movement_start_time > 50:
                self.get_logger().warn('运动超时，强制继续')
                self._on_movement_completed()
                return
            
            # 🔧 检查是否到达目标位置（scan_executor的检查方式）
            # 这里简化处理，实际中应该检查与目标位置的距离
            if self.current_tcp_pose is not None:
                # 简化版：检查是否有位置更新（表明运动开始了）
                elapsed = time.time() - self.movement_start_time
                
                if elapsed > 2.0:  # 2秒后认为运动完成（简化处理）
                    self.get_logger().info('✅ 运动完成（简化检测）')
                    self._on_movement_completed()
                else:
                    self.get_logger().debug(f'🚀 等待运动完成... 已过时间: {elapsed:.1f}s')
            
        except Exception as e:
            self.get_logger().error(f'运动完成检查失败: {e}')

    def _on_movement_completed(self):
        """运动完成处理 - 参考scan_executor的处理"""
        try:
            # 🔧 停止运动检查定时器（scan_executor风格）
            if hasattr(self, 'movement_check_timer'):
                self.movement_check_timer.destroy()
            
            self.movement_completed = True
            
            self.get_logger().info('✅ 机械臂运动完成，准备下一步追踪')
            
            # 🔧 发布运动完成信号（模拟scan_executor的完成信号）
            movement_complete_msg = String()
            movement_complete_msg.data = "movement_completed"
            
            # 这里应该有一个运动完成发布者，如果没有则创建一个
            if not hasattr(self, 'movement_complete_pub'):
                self.movement_complete_pub = self.create_publisher(String, '/xarm/movement_complete', 10)
            
            self.movement_complete_pub.publish(movement_complete_msg)
            
        except Exception as e:
            self.get_logger().error(f'运动完成处理失败: {e}')

    def _publish_target_pose(self, tracking_result: dict):
        """发布目标位姿给机械臂 - 使用自适应移动策略"""
        try:
            grasp_coord = tracking_result['grasp_coordinate']
            object_info = tracking_result['object_info']
            
            # 获取当前TCP位置
            if not self.current_tcp_pose:
                self.get_logger().error('无法获取当前TCP位置')
                return
            
            current_pos = self.current_tcp_pose['position']
            
            # 计算自适应移动策略
            movement_strategy = self._calculate_adaptive_movement_strategy(
                self.current_tcp_pose, grasp_coord, object_info
            )
            
            # 使用自适应比例而不是固定25%
            target_x = current_pos['x'] + (grasp_coord['x'] - current_pos['x']) * movement_strategy['xy_movement_ratio']
            target_y = current_pos['y'] + (grasp_coord['y'] - current_pos['y']) * movement_strategy['xy_movement_ratio']
            
            # 使用安全移动高度
            target_z = movement_strategy['safe_movement_z']
            
            # 构建位姿消息
            pose_msg = PoseStamped()
            pose_msg.header.stamp = self.get_clock().now().to_msg()
            pose_msg.header.frame_id = "base_link"
            
            # 🔧 关键修复：确保所有位置数据都是float类型
            pose_msg.pose.position.x = float(target_x)
            pose_msg.pose.position.y = float(target_y)
            pose_msg.pose.position.z = float(target_z)
            
            # 姿态保持不变
            if self.current_tcp_pose and 'orientation' in self.current_tcp_pose:
                orientation = self.current_tcp_pose['orientation']
                pose_msg.pose.orientation.x = float(orientation['x'])
                pose_msg.pose.orientation.y = float(orientation['y'])
                pose_msg.pose.orientation.z = float(orientation['z'])
                pose_msg.pose.orientation.w = float(orientation['w'])
            else:
                # 默认姿态
                pose_msg.pose.orientation.x = 0.0
                pose_msg.pose.orientation.y = 1.0
                pose_msg.pose.orientation.z = 0.0
                pose_msg.pose.orientation.w = 0.0
            
            # 发布目标位姿
            self.tracking_result_pub.publish(pose_msg)
            
            self.get_logger().info(f'📤 发布自适应移动目标:')
            self.get_logger().info(f'   目标: ({target_x:.1f}, {target_y:.1f}, {target_z:.1f}mm)')
            self.get_logger().info(f'   当前: ({current_pos["x"]:.1f}, {current_pos["y"]:.1f}, {current_pos["z"]:.1f}mm)')
            self.get_logger().info(f'   最终: ({grasp_coord["x"]:.1f}, {grasp_coord["y"]:.1f}, {grasp_coord["z"]:.1f}mm)')
            self.get_logger().info(f'   策略: XY比例={movement_strategy["xy_movement_ratio"]:.1f}, 距离={movement_strategy["distance_3d"]:.1f}mm')
            
            # 标记为等待移动完成
            self.movement_complete = False
            
        except Exception as e:
            self.get_logger().error(f'发布目标位姿失败: {e}')

    
    def _publish_tracking_status(self, status: str, result: dict):
        """发布追踪状态"""
        try:
            status_data = {
                'status': status,
                'step': self.tracking_count,
                'target_id': self.current_target_id,
                'timestamp': datetime.now().isoformat()
            }
            
            if result:
                status_data['confidence'] = result.get('tracking_confidence', 0.0)
                status_data['position'] = result.get('grasp_coordinate', {})
            
            status_msg = String()
            status_msg.data = json.dumps(status_data)
            self.tracking_status_pub.publish(status_msg)
            
        except Exception as e:
            self.get_logger().error(f'发布追踪状态失败: {e}')
    
    def _finish_tracking_session(self):
        """完成追踪会话 - 修复版"""
        try:
            self.get_logger().info('🏁 追踪会话完成，开始收集反馈')
            
            # 🔧 立即停止追踪，防止继续执行
            self.tracking_active = False
            
            # 🆕 停止图像处理
            if hasattr(self, '_last_tracking_time'):
                del self._last_tracking_time
            
            # 收集用户反馈
            self._collect_user_feedback()
            
            # 发布追踪完成信号
            complete_data = {
                'status': 'completed',
                'total_steps': self.tracking_count,
                'target_id': self.current_target_id,
                'user_id': self.current_user_id
            }
            
            complete_msg = String()
            complete_msg.data = json.dumps(complete_data)
            self.tracking_complete_pub.publish(complete_msg)
            
            self.get_logger().info(f'📊 追踪完成统计: 总步数={self.tracking_count}, 目标={self.current_target_id}')
            
        except Exception as e:
            self.get_logger().error(f'完成追踪会话失败: {e}')
    
    def _collect_user_feedback(self):
        """收集用户反馈 - 修复重复问题"""
        try:
            # 🔧 检查是否已经在实时确认中收集了反馈
            if hasattr(self, 'tracking_parameters_history') and self.tracking_parameters_history:
                # 检查是否所有步骤都已经有反馈
                steps_with_feedback = [step for step in self.tracking_parameters_history if 'user_feedback' in step]
                
                if len(steps_with_feedback) == len(self.tracking_parameters_history):
                    self.get_logger().info('✅ 所有步骤已在实时过程中收集反馈，跳过额外反馈收集')
                    
                    # 保存学习结果
                    if hasattr(self, 'online_learner') and self.online_learner:
                        self.online_learner.save_learning_data()
                    if hasattr(self, 'data_recorder') and self.data_recorder:
                        self.data_recorder.save_session_data()
                    
                    self.get_logger().info('✅ 反馈收集完成，学习数据已更新')
                    return
            
            # 🔧 只有在没有实时反馈时才进行传统反馈收集
            self.get_logger().info('🔧 开始传统反馈收集流程...')
            
            # 显示追踪结果可视化
            if hasattr(self, 'visualizer') and self.visualizer:
                self.visualizer.show_tracking_summary(
                    self.data_recorder.get_tracking_history(),
                    self.current_target_id
                )
            
            # 启动反馈收集线程
            feedback_thread = threading.Thread(
                target=self._feedback_collection_worker
            )
            feedback_thread.daemon = True
            feedback_thread.start()
            
        except Exception as e:
            self.get_logger().error(f'收集用户反馈失败: {e}')

    def _feedback_collection_worker(self):
        """反馈收集工作线程 - 修复重复问题"""
        try:
            # 🔧 检查是否已经有实时反馈
            if hasattr(self, 'tracking_parameters_history') and self.tracking_parameters_history:
                steps_with_feedback = [step for step in self.tracking_parameters_history if 'user_feedback' in step]
                if len(steps_with_feedback) == len(self.tracking_parameters_history):
                    self.get_logger().info('✅ 跳过重复反馈收集')
                    return
            
            tracking_history = self.data_recorder.get_tracking_history()
            
            for i, record in enumerate(tracking_history):
                # 🔧 检查是否已经有反馈
                if 'user_feedback' in record:
                    self.get_logger().info(f'📋 步骤 {i+1}: 已有反馈，跳过')
                    continue
                
                self.get_logger().info(f'📋 步骤 {i+1}: 请确认追踪结果是否正确')
                
                # 显示该步骤的图像和结果
                if hasattr(self, 'visualizer') and self.visualizer:
                    self.visualizer.show_step_result(record, i+1)
                
                # 收集反馈
                feedback = self.feedback_collector.collect_feedback(
                    f"步骤 {i+1} 追踪是否正确？ (y/n): "
                )
                
                # 记录反馈
                record['human_feedback'] = 'correct' if feedback else 'incorrect'
                record['feedback_timestamp'] = datetime.now().isoformat()
                
                # 更新在线学习
                if hasattr(self, 'online_learner') and self.online_learner:
                    self.online_learner.update_with_feedback(
                        self.current_target_id,
                        record,
                        feedback
                    )
            
            # 保存学习结果
            if hasattr(self, 'online_learner') and self.online_learner:
                self.online_learner.save_learning_data()
            if hasattr(self, 'data_recorder') and self.data_recorder:
                self.data_recorder.save_session_data()
            
            self.get_logger().info('✅ 反馈收集完成，学习数据已更新')
            
        except Exception as e:
            self.get_logger().error(f'反馈收集工作线程失败: {e}')

    def _calculate_adaptive_movement_strategy(self, current_tcp_pose: dict, target_coord: dict, 
                                            object_info: dict) -> dict:
        """计算自适应移动策略 - 添加安全高度约束"""
        try:
            import math
            
            # 计算3D距离
            current_pos = current_tcp_pose['position']
            distance_3d = math.sqrt(
                (target_coord['x'] - current_pos['x'])**2 + 
                (target_coord['y'] - current_pos['y'])**2
            )
            z_compensation = 260
            # 距离自适应策略
            if distance_3d > 200:
                xy_ratio = 0.30

            elif distance_3d > 100:
                xy_ratio = 0.50
            elif distance_3d > 50:
                xy_ratio = 0.8
                z_compensation = 250
            else:
                xy_ratio = 1
                z_compensation = 230
            
            # 🆕 安全移动高度计算
            background_z = object_info.get('background_z', 300)
            object_height = object_info.get('estimated_height', 30)
            safe_movement_z = max(320, background_z + object_height + z_compensation)
            
            self.get_logger().info(f'📐 移动策略计算:')
            self.get_logger().info(f'   3D距离: {distance_3d:.1f}mm')
            self.get_logger().info(f'   XY移动比例: {xy_ratio:.1f}')
            self.get_logger().info(f'   背景高度: {background_z:.1f}mm')
            self.get_logger().info(f'   物体高度: {object_height:.1f}mm') 
            self.get_logger().info(f'   Z补偿: {z_compensation}mm')
            self.get_logger().info(f'   安全移动高度: max(320, {background_z:.1f} + {object_height:.1f} + {z_compensation}) = {safe_movement_z:.1f}mm')
            
            return {
                'distance_3d': distance_3d,
                'xy_movement_ratio': xy_ratio,
                'z_compensation': z_compensation,
                'safe_movement_z': safe_movement_z,  # 🆕 使用这个作为移动目标Z
                'strategy': 'adaptive_with_safety'
            }
            
        except Exception as e:
            self.get_logger().error(f'自适应移动策略计算失败: {e}')
            return {
                'distance_3d': 100,
                'xy_movement_ratio': 0.25,
                'z_compensation': 200,
                'safe_movement_z': 300,
                'strategy': 'fallback'
            }

        
    def _evaluate_grasp_conditions(self, tracking_result: dict, movement_strategy: dict) -> dict:
        """评估抓取条件 - 精确版本"""
        try:
            # 获取当前和目标位置
            current_pos = self.current_tcp_pose['position']
            target_coord = tracking_result['grasp_coordinate']
            
            # 计算精确距离
            target_distance_z = target_coord['z']
            xy_distance = math.sqrt(
                (target_coord['x'] - current_pos['x'])**2 + 
                (target_coord['y'] - current_pos['y'])**2
            )
            
            # 精确的抓取条件
            conditions = {
                'camera_min_height': current_pos['z'] >= 300,
                'z_close_enough': 0.0 < target_distance_z < 10.0,  # Z距离小于10mm
                'xy_aligned': xy_distance < 50.0,  # XY距离小于50mm
                'confidence_check': tracking_result['tracking_confidence'] > 0.65,
                'stability_check': self._check_tracking_stability()
            }
            
            # 综合判断
            grasp_ready = conditions['camera_min_height'] and conditions['z_close_enough'] and conditions['xy_aligned'] and conditions['confidence_check'] and conditions['stability_check']
            
            self.get_logger().info(f'🎯 抓取条件评估:')
            self.get_logger().info(f'   Z距离: {target_distance_z:.1f}mm (< 10mm: {conditions["z_close_enough"]})')
            self.get_logger().info(f'   XY距离: {xy_distance:.1f}mm (< 60mm: {conditions["xy_aligned"]})')
            self.get_logger().info(f'   置信度: {tracking_result["tracking_confidence"]:.3f} (> 0.65: {conditions["confidence_check"]})')
            self.get_logger().info(f'   稳定性: {conditions["stability_check"]}')
            self.get_logger().info(f'   🎯 准备抓取: {grasp_ready}')
            
            return {
                'grasp_ready': grasp_ready,
                'conditions': conditions,
                'distances': {
                    'z_distance': target_distance_z,
                    'xy_distance': xy_distance
                },
                'recommendation': 'grasp' if grasp_ready else 'continue_tracking'
            }
            
        except Exception as e:
            self.get_logger().error(f'抓取条件评估失败: {e}')
            return {'grasp_ready': False, 'conditions': {}, 'recommendation': 'continue_tracking'}

    def _check_tracking_stability(self) -> bool:
        """检查追踪稳定性（最近3步位置变化）"""
        if len(self.tracking_parameters_history) < 2:
            return False
        
        recent_positions = [step['target_coordinate'] for step in self.tracking_parameters_history[-2:]]
        max_deviation = 0
        for i in range(1, len(recent_positions)):
            deviation = math.sqrt(
                (recent_positions[i]['x'] - recent_positions[i-1]['x'])**2 +
                (recent_positions[i]['y'] - recent_positions[i-1]['y'])**2
            )
            max_deviation = max(max_deviation, deviation)
        
        return max_deviation < 30  # 15mm以内认为稳定
    def _handle_detection_failure_with_retry(self):
        """处理检测失败 - 增强提示信息"""
        try:
            if not hasattr(self, 'consecutive_failures'):
                self.consecutive_failures = 0
            
            self.consecutive_failures += 1
            
            # 🆕 详细的失败提示
            self.get_logger().warn(f'🔍 检测失败 {self.consecutive_failures}/2')
            self.get_logger().info(f'📊 当前追踪状态:')
            self.get_logger().info(f'   目标ID: {self.current_target_id}')
            self.get_logger().info(f'   当前位置: {self._get_current_position_str()}')
            self.get_logger().info(f'   追踪步数: {self.tracking_count}/{self.max_tracking_steps}')
            self.get_logger().info(f'   追踪置信度历史: {self._get_recent_confidence_str()}')
            
            if self.consecutive_failures < 2:
                self.get_logger().info('⏳ 2秒后进行重试检测...')
                self.get_logger().info('💡 重试期间请确保:')
                self.get_logger().info('   ✓ 目标物体在相机视野内')
                self.get_logger().info('   ✓ 光照条件良好')
                self.get_logger().info('   ✓ 没有遮挡物干扰')
                self.get_logger().info('   ✓ 相机焦距清晰')
                time.sleep(2)
                return False
            
            # 连续失败的详细提示
            self.get_logger().warn('❌ 连续2次检测失败!')
            self.get_logger().warn('🤔 可能的原因分析:')
            self.get_logger().warn('   1. 目标物体已移出相机视野')
            self.get_logger().warn('   2. 光照条件发生显著变化') 
            self.get_logger().warn('   3. 目标物体被其他物体遮挡')
            self.get_logger().warn('   4. 相机角度不适合当前检测')
            self.get_logger().warn('   5. 物体外观发生变化(如形变)')
            
            self.get_logger().info('🔧 系统建议:')
            self.get_logger().info('   → 检查相机视野是否包含目标')
            self.get_logger().info('   → 调整环境光照条件')
            self.get_logger().info('   → 移除可能的遮挡物')
            
            user_confirms_failure = self._request_user_failure_confirmation()
            
            if user_confirms_failure:
                self.get_logger().info('🔄 用户确认检测失败，准备回退到上一个成功位置')
                self.get_logger().info('📍 正在查找最近的成功追踪位置...')
                return self._rollback_to_last_successful_position()
            else:
                self.get_logger().info('✅ 用户认为应该能检测到，重置失败计数继续尝试')
                self.get_logger().info('🔄 系统将继续尝试检测，请确保环境条件合适')
                self.consecutive_failures = 0
                return False
                
        except Exception as e:
            self.get_logger().error(f'检测失败处理异常: {e}')
            return True
        
    def _get_current_position_str(self) -> str:
        """获取当前位置的字符串描述"""
        if self.current_tcp_pose:
            pos = self.current_tcp_pose['position']
            return f"[{pos['x']:.1f}, {pos['y']:.1f}, {pos['z']:.1f}]mm"
        return "位置未知"

    def _get_recent_confidence_str(self) -> str:
        """获取最近置信度历史的字符串"""
        try:
            if hasattr(self, 'tracking_parameters_history') and self.tracking_parameters_history:
                recent_steps = self.tracking_parameters_history[-3:]  # 最近3步
                confidences = [f"{step.get('tracking_confidence', 0):.3f}" for step in recent_steps]
                return f"[{', '.join(confidences)}]"
            return "无历史数据"
        except:
            return "获取失败"


    def _request_user_failure_confirmation(self) -> bool:
        """请求用户确认检测失败"""
        try:
            print(f"\n{'='*60}")
            print(f"🔍 检测失败确认 - 追踪步骤 {self.tracking_count + 1}")
            print(f"{'='*60}")
            print(f"目标ID: {self.current_target_id}")
            print(f"当前位置: {self._get_current_position_str()}")
            print(f"连续失败次数: {self.consecutive_failures}")
            print(f"\n❓ 请确认: 在当前位置是否真的无法看到目标物体?")
            print(f"   'y' - 确认无法看到 (将回退到上一个成功位置)")
            print(f"   'n' - 应该能看到 (继续尝试检测)")
            print(f"{'='*60}")
            
            while True:
                try:
                    user_input = input("请输入选择 (y/n): ").strip().lower()
                    
                    if user_input in ['y', 'yes', '是', '确认']:
                        print("✅ 用户确认: 当前位置无法检测到目标")
                        return True
                    elif user_input in ['n', 'no', '否', '继续']:
                        print("✅ 用户确认: 应该能检测到目标，继续尝试")
                        return False
                    else:
                        print("❌ 无效输入，请输入 'y'(确认失败) 或 'n'(继续尝试)")
                        
                except (EOFError, KeyboardInterrupt):
                    print("\n🛑 用户中断输入，默认为确认失败")
                    return True
                    
        except Exception as e:
            self.get_logger().error(f'请求用户确认失败: {e}')
            return True  # 异常时默认确认失败
    def _rollback_to_last_successful_position(self) -> bool:
        """回退到上一个用户确认成功的位置 - 增强版"""
        try:
            self.get_logger().info('🔄 开始回退流程分析...')
            
            # 找到最后一个用户反馈为success的位置
            rollback_target = None
            for step in reversed(self.tracking_parameters_history):
                if step.get('user_feedback') == 'success':
                    rollback_target = step
                    break
            
            if rollback_target is None:
                self.get_logger().error('❌ 没有找到可回退的成功位置')
                self.get_logger().error('💡 建议: 手动移动到合适位置后重新开始追踪')
                return False
            
            # 显示回退信息
            self.get_logger().info(f'🔄 找到回退目标: 步骤 {rollback_target["step"]}')
            self.get_logger().info(f'📍 回退位置: {rollback_target["target_coordinate"]}')
            self.get_logger().info(f'⭐ 该位置追踪置信度: {rollback_target.get("tracking_confidence", 0):.3f}')
            
            # 发布回退位置
            target_coord = rollback_target['target_coordinate']
            self._publish_rollback_pose(target_coord)
            
            # 重置状态
            self.consecutive_failures = 0
            self.tracking_count = rollback_target['step']  # 重置追踪计数
            self.movement_complete = False  # 等待移动完成
            
            self.get_logger().info(f'✅ 回退指令已发布，等待机械臂移动完成')
            self.get_logger().info(f'🔄 追踪将从步骤 {self.tracking_count} 继续')
            
            return True
            
        except Exception as e:
            self.get_logger().error(f'回退处理失败: {e}')
            return False

    def _publish_rollback_pose(self, target_coord: dict):
        """发布回退位置指令"""
        try:
            pose_msg = PoseStamped()
            pose_msg.header.stamp = self.get_clock().now().to_msg()
            pose_msg.header.frame_id = "base_link"
            
            # 使用回退位置坐标
            pose_msg.pose.position.x = target_coord['x']
            pose_msg.pose.position.y = target_coord['y']  
            pose_msg.pose.position.z = target_coord['z']
            
            # 保持当前姿态
            if self.current_tcp_pose and 'orientation' in self.current_tcp_pose:
                orientation = self.current_tcp_pose['orientation']
                pose_msg.pose.orientation.x = orientation['x']
                pose_msg.pose.orientation.y = orientation['y']
                pose_msg.pose.orientation.z = orientation['z']
                pose_msg.pose.orientation.w = orientation['w']
            else:
                pose_msg.pose.orientation.x = 0.0
                pose_msg.pose.orientation.y = 1.0
                pose_msg.pose.orientation.z = 0.0
                pose_msg.pose.orientation.w = 0.0
            
            self.tracking_result_pub.publish(pose_msg)
            
            self.get_logger().info(f'📤 回退指令已发布: ({target_coord["x"]:.1f}, {target_coord["y"]:.1f}, {target_coord["z"]:.1f}mm)')
            
        except Exception as e:
            self.get_logger().error(f'发布回退位置失败: {e}')         
def main(args=None):
    rclpy.init(args=args)
    
    try:
        tracking_node = TrackingNode()
        tracking_node.get_logger().info('🎯 Track节点运行中...')
        rclpy.spin(tracking_node)
    except KeyboardInterrupt:
        print('🛑 Track节点被用户中断')
    except Exception as e:
        print(f'❌ Track节点运行错误: {e}')
    finally:
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()