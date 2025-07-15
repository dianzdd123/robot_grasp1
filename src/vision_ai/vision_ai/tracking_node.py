import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped, Point, Quaternion
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import json
import os
import threading
import math
import time
import cv2
import numpy as np
from pathlib import Path

# 导入追踪系统组件
from vision_ai.tracking_system.utils.config import TrackingSystemConfig
from vision_ai.tracking_system.core.tracking_core import TrackingCore
from vision_ai.tracking_system.core.state_machine import StateMachine, TrackingState
from vision_ai.tracking_system.vision.visual_tracker import VisualTracker
from vision_ai.tracking_system.vision.feature_manager import FeatureManager
from vision_ai.tracking_system.control.pose_controller import PoseController

from vision_ai.tracking_system.detection.realtime_detector import RealtimeDetector


class TrackingNode(Node):
    def __init__(self):
        super().__init__('tracking_node')
        
        # 初始化配置
        self.config = TrackingSystemConfig()
        
        # 初始化追踪系统组件
        self.tracking_core = TrackingCore(self.config, self.get_logger())
        self.state_machine = StateMachine(self.config, self.get_logger())
        self.visual_tracker = VisualTracker(self.config, self.get_logger())
        self.feature_manager = FeatureManager(self.config, self.get_logger())
        self.pose_controller = PoseController(self.config, self.get_logger())
        
        # ⭐⭐⭐ 初始化实时检测管道 ⭐⭐⭐
        self.realtime_detector = None
        self._initialize_realtime_detector()
        
        # 当前扫描输出目录和参考特征
        self.current_scan_dir = None
        self.reference_features_db = {}  # 存储检测阶段的参考特征
        
        # 订阅者
        self.current_pose_sub = self.create_subscription(
            PoseStamped,
            self.config.topics['xarm_current_pose'],
            self.current_pose_callback,
            10
        )
        
        # ⭐⭐⭐ 订阅实时相机图像 ⭐⭐⭐
        self.color_image_sub = self.create_subscription(
            Image,
            self.config.topics['camera_color'],
            self.realtime_image_callback,
            10
        )
        
        self.depth_image_sub = self.create_subscription(
            Image,
            self.config.topics['camera_depth'],
            self.depth_image_callback,
            10
        )
        
        # 检测完成信号订阅
        self.detection_complete_sub = self.create_subscription(
            String,
            '/detection_complete',
            self.detection_complete_callback,
            10
        )
        
        # 发布者
        self.target_pose_pub = self.create_publisher(
            PoseStamped,
            self.config.topics['xarm_target_pose'],
            10
        )
        
        self.gripper_target_pub = self.create_publisher(
            String,
            self.config.topics['xarm_gripper_target'],
            10
        )
        
        self.status_pub = self.create_publisher(
            String,
            self.config.topics['tracking_status'],
            10
        )
        
        self.visualization_pub = self.create_publisher(
            Image,
            self.config.topics['tracking_visualization'],
            10
        )
        
        # 状态定时器
        self.status_timer = self.create_timer(0.1, self.publish_status)  # 10Hz
        
        # 实时检测定时器 (当tracking激活时)
        self.realtime_detection_timer = None
        
        # 状态变量
        self.current_arm_pose = None
        self.current_color_image = None
        self.current_depth_image = None
        self.last_detection_time = None
        
        # 线程锁
        self.data_lock = threading.Lock()
        
        self.get_logger().info('🎯 Enhanced Tracking Node with Real-time Detection initialized')

    def _initialize_realtime_detector(self):
        """初始化独立的实时检测器"""
        try:
            self.realtime_detector = RealtimeDetector(self.config, self.get_logger())
            self.get_logger().info('✅ Independent realtime detector initialized')
        except Exception as e:
            self.get_logger().error(f'❌ Failed to initialize realtime detector: {e}')
            self.realtime_detector = None

    def detection_complete_callback(self, msg):
        """检测完成回调，解析扫描目录并加载参考特征"""
        try:
            data = json.loads(msg.data)
            self.current_scan_dir = data.get('scan_directory', '')
            
            if not self.current_scan_dir:
                self.get_logger().error('No scan directory in detection complete message')
                return
            
            # 更新配置中的路径
            self.config.paths['tracking_selection'] = os.path.join(
                self.current_scan_dir, 'detection_results', 'tracking_selection.txt'
            )
            self.config.paths['detection_results_dir'] = os.path.join(
                self.current_scan_dir, 'detection_results'
            )
            
            self.get_logger().info(f'📁 Scan directory updated: {self.current_scan_dir}')
            
            # ⭐⭐⭐ 加载参考特征数据库 ⭐⭐⭐
            self._load_reference_features_db()
            
            # 检查tracking_selection文件
            selection_file = self.config.paths['tracking_selection']
            if os.path.exists(selection_file):
                self.get_logger().info(f'✅ Found tracking selection file: {selection_file}')
                # 自动启动追踪
                self.start_tracking_from_selection()
            else:
                self.get_logger().warn(f'⚠️ Tracking selection file not found: {selection_file}')
                
        except json.JSONDecodeError as e:
            self.get_logger().error(f'Failed to parse detection complete JSON: {e}')
        except Exception as e:
            self.get_logger().error(f'Error in detection complete callback: {e}')

    def _load_reference_features_db(self):
        """加载检测阶段的参考特征数据库"""
        try:
            results_dir = self.config.paths['detection_results_dir']
            
            # 查找检测结果JSON文件
            json_files = []
            for file in os.listdir(results_dir):
                if file.endswith('_detection_results.json'):
                    json_files.append(file)
            
            if not json_files:
                self.get_logger().warn('No detection results JSON found')
                return
            
            # 加载最新的检测结果
            latest_json = sorted(json_files)[-1]
            json_path = os.path.join(results_dir, latest_json)
            
            with open(json_path, 'r') as f:
                detection_results = json.load(f)
            
            # 构建参考特征数据库
            for obj in detection_results.get('objects', []):
                object_id = obj.get('object_id')
                if object_id:
                    self.reference_features_db[object_id] = {
                        'class_id': obj.get('class_id'),
                        'class_name': obj.get('class_name'),
                        'features': obj.get('features', {}),
                        'description': obj.get('description', '')
                    }
            
            self.get_logger().info(f'📚 Loaded {len(self.reference_features_db)} reference features')
            
        except Exception as e:
            self.get_logger().error(f'Failed to load reference features: {e}')

    def realtime_image_callback(self, msg):
        """实时彩色图像回调"""
        try:
            with self.data_lock:
                # 手动转换避免cv_bridge冲突
                self.current_color_image = self._manual_imgmsg_to_cv2(msg, "bgr8")
                
                # 如果正在追踪且有深度图像，触发实时检测
                if (self.tracking_core.current_state != TrackingState.IDLE and 
                    self.current_depth_image is not None):
                    self._trigger_realtime_detection()
                    
        except Exception as e:
            self.get_logger().error(f'Error in color image callback: {e}')

    def depth_image_callback(self, msg):
        """实时深度图像回调"""
        try:
            with self.data_lock:
                # 手动转换避免cv_bridge冲突
                self.current_depth_image = self._manual_imgmsg_to_cv2(msg, "16UC1")
                    
        except Exception as e:
            self.get_logger().error(f'Error in depth image callback: {e}')

    def _manual_imgmsg_to_cv2(self, msg, encoding):
        """手动转换ROS图像消息避免cv_bridge冲突"""
        try:
            import numpy as np
            
            # 从ROS消息提取图像数据
            if encoding == "bgr8":
                # 彩色图像 8UC3
                image_array = np.frombuffer(msg.data, dtype=np.uint8)
                image = image_array.reshape((msg.height, msg.width, 3))
            elif encoding == "16UC1":
                # 深度图像 16UC1
                image_array = np.frombuffer(msg.data, dtype=np.uint16)
                image = image_array.reshape((msg.height, msg.width))
            else:
                raise ValueError(f"Unsupported encoding: {encoding}")
            
            return image
            
        except Exception as e:
            self.get_logger().error(f'Manual image conversion failed: {e}')
            return None

    def _trigger_realtime_detection(self):
        """触发实时检测（修改后的版本）"""
        try:
            if not self.realtime_detector:
                return
            
            # 复制当前图像
            color_img = self.current_color_image.copy()
            
            # 转换为RGB
            rgb_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2RGB)
            
            # ⭐⭐⭐ 使用独立检测器 ⭐⭐⭐
            detected_objects = self.realtime_detector.detect_and_segment(rgb_img)
            
            if detected_objects:
                self.get_logger().debug(f'🔍 Realtime detection: {len(detected_objects)} objects')
                
                # ID匹配
                matched_objects = self._perform_id_matching(detected_objects)
                
                # 构建检测数据
                detection_data = {
                    'detection_count': len(matched_objects),
                    'objects': matched_objects,
                    'timestamp': self.get_clock().now().nanoseconds
                }
                
                # 处理追踪
                control_command = self.tracking_core.process_detection_result(detection_data)
                
                if control_command:
                    enhanced_command = self._enhance_control_command(control_command, detection_data)
                    self._execute_control_command(enhanced_command)
                    self._publish_tracking_visualization(detection_data, enhanced_command)
                
                self.last_detection_time = self.get_clock().now()
            
        except Exception as e:
            self.get_logger().error(f'Real-time detection failed: {e}')

    def _perform_realtime_detection(self, color_img, depth_img):
        """执行实时YOLO+SAM2检测"""
        try:
            # 转换为RGB
            rgb_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2RGB)
            
            # 使用detection_pipeline进行检测
            result = self.detection_pipeline.process_reference_image(
                rgb_img, 
                depth_img,
                generate_visualization=False,
                auto_display=False
            )
            
            if result['success']:
                self.get_logger().debug(f'🔍 Real-time detection: {result["detection_count"]} objects')
                return result
            else:
                return None
                
        except Exception as e:
            self.get_logger().error(f'YOLO+SAM2 detection failed: {e}')
            return None

    def _perform_id_matching(self, detection_result):
        """⭐⭐⭐ 执行ID匹配：class_id + hu_moments + color_histogram ⭐⭐⭐"""
        matched_objects = []
        
        try:
            for detected_obj in detection_result.get('objects', []):
                best_match = self._find_best_match(detected_obj)
                
                if best_match:
                    # 为匹配的对象分配object_id
                    matched_obj = detected_obj.copy()
                    matched_obj['object_id'] = best_match['object_id']
                    matched_obj['match_confidence'] = best_match['confidence']
                    matched_obj['match_method'] = best_match['method']
                    
                    matched_objects.append(matched_obj)
                    
                    self.get_logger().debug(
                        f'✅ ID Match: {best_match["object_id"]} '
                        f'(conf: {best_match["confidence"]:.3f}, method: {best_match["method"]})'
                    )
                else:
                    # 未匹配的对象，分配临时ID
                    detected_obj['object_id'] = f"unknown_{detected_obj.get('class_name', 'obj')}"
                    detected_obj['match_confidence'] = 0.0
                    matched_objects.append(detected_obj)
            
            return matched_objects
            
        except Exception as e:
            self.get_logger().error(f'ID matching failed: {e}')
            return []

    def _find_best_match(self, detected_obj):
        """找到最佳匹配的参考对象"""
        try:
            detected_class_id = detected_obj.get('class_id')
            detected_features = detected_obj.get('features', {})
            
            best_match = None
            best_score = 0.0
            
            for ref_id, ref_data in self.reference_features_db.items():
                # 1. 类别ID必须匹配
                if ref_data['class_id'] != detected_class_id:
                    continue
                
                # 2. 计算特征相似度
                similarity_score = self._calculate_feature_similarity(
                    detected_features, 
                    ref_data['features']
                )
                
                # 3. 空间连续性检查（如果有历史位置）
                spatial_bonus = self._calculate_spatial_continuity_bonus(detected_obj, ref_id)
                
                # 4. 综合评分
                total_score = similarity_score * 0.8 + spatial_bonus * 0.2
                
                if total_score > best_score and total_score > 0.6:  # 阈值
                    best_score = total_score
                    best_match = {
                        'object_id': ref_id,
                        'confidence': total_score,
                        'method': 'class+features+spatial'
                    }
            
            return best_match
            
        except Exception as e:
            self.get_logger().error(f'Best match search failed: {e}')
            return None

    def _calculate_feature_similarity(self, detected_features, reference_features):
        """计算检测特征与参考特征的相似度"""
        try:
            total_score = 0.0
            weight_sum = 0.0
            
            # Hu矩相似度
            detected_hu = detected_features.get('shape', {}).get('hu_moments', [])
            reference_hu = reference_features.get('shape', {}).get('hu_moments', [])
            
            if detected_hu and reference_hu and len(detected_hu) >= 3 and len(reference_hu) >= 3:
                hu_similarity = self._compare_hu_moments(detected_hu[:3], reference_hu[:3])
                total_score += 0.4 * hu_similarity
                weight_sum += 0.4
            
            # 颜色直方图相似度
            detected_hist = detected_features.get('color', {}).get('histogram', [])
            reference_hist = reference_features.get('color', {}).get('histogram', [])
            
            if detected_hist and reference_hist:
                hist_similarity = self._compare_histograms(detected_hist, reference_hist)
                total_score += 0.4 * hist_similarity
                weight_sum += 0.4
            
            # 形状几何特征相似度
            shape_similarity = self._compare_shape_geometry(
                detected_features.get('shape', {}),
                reference_features.get('shape', {})
            )
            total_score += 0.2 * shape_similarity
            weight_sum += 0.2
            
            return total_score / weight_sum if weight_sum > 0 else 0.0
            
        except Exception as e:
            self.get_logger().error(f'Feature similarity calculation failed: {e}')
            return 0.0

    def _compare_hu_moments(self, hu1, hu2):
        """比较Hu矩"""
        try:
            if len(hu1) != len(hu2):
                return 0.0
            
            # 对数变换
            log_hu1 = [-np.sign(h) * np.log10(abs(h) + 1e-10) for h in hu1]
            log_hu2 = [-np.sign(h) * np.log10(abs(h) + 1e-10) for h in hu2]
            
            # 欧氏距离
            distance = np.linalg.norm(np.array(log_hu1) - np.array(log_hu2))
            similarity = max(0, 1 - distance / 10)
            
            return similarity
            
        except Exception:
            return 0.0

    def _compare_histograms(self, hist1, hist2):
        """比较颜色直方图"""
        try:
            if len(hist1) != len(hist2):
                return 0.0
            
            h1 = np.array(hist1, dtype=np.float64)
            h2 = np.array(hist2, dtype=np.float64)
            
            # 归一化
            h1 = h1 / (np.sum(h1) + 1e-10)
            h2 = h2 / (np.sum(h2) + 1e-10)
            
            # Chi-square距离
            chi_square = np.sum((h1 - h2) ** 2 / (h1 + h2 + 1e-10))
            similarity = max(0, 1 - chi_square / 2)
            
            return similarity
            
        except Exception:
            return 0.0

    def _compare_shape_geometry(self, shape1, shape2):
        """比较形状几何特征"""
        try:
            features = ['area', 'aspect_ratio', 'circularity', 'eccentricity']
            similarities = []
            
            for feature in features:
                val1 = shape1.get(feature, 0)
                val2 = shape2.get(feature, 0)
                
                if val1 > 0 and val2 > 0:
                    ratio = min(val1, val2) / max(val1, val2)
                    similarities.append(ratio)
            
            return np.mean(similarities) if similarities else 0.0
            
        except Exception:
            return 0.0

    def _calculate_spatial_continuity_bonus(self, detected_obj, ref_id):
        """计算空间连续性奖励"""
        try:
            # 如果当前正在追踪这个ID，给予空间连续性奖励
            if self.tracking_core.target_object_id == ref_id:
                detected_centroid = detected_obj.get('features', {}).get('spatial', {}).get('centroid_2d', (0, 0))
                
                # 与历史位置比较
                if hasattr(self.tracking_core, 'target_features') and self.tracking_core.target_features:
                    ref_centroid = self.tracking_core.target_features.get('centroid', (0, 0))
                    
                    if detected_centroid and ref_centroid:
                        distance = np.sqrt(
                            (detected_centroid[0] - ref_centroid[0])**2 + 
                            (detected_centroid[1] - ref_centroid[1])**2
                        )
                        
                        # 距离越近，奖励越高
                        max_distance = 100  # pixels
                        bonus = max(0, 1 - distance / max_distance)
                        return bonus
            
            return 0.0
            
        except Exception:
            return 0.0

    def detection_complete_callback(self, msg):
        """检测完成回调，解析扫描目录"""
        try:
            # 解析JSON数据
            data = json.loads(msg.data)
            self.current_scan_dir = data.get('scan_directory', '')
            
            if not self.current_scan_dir:
                self.get_logger().error('No scan directory in detection complete message')
                return
            
            # 更新配置中的路径
            self.config.paths['tracking_selection'] = os.path.join(
                self.current_scan_dir, 'detection_results', 'tracking_selection.txt'
            )
            self.config.paths['detection_results_dir'] = os.path.join(
                self.current_scan_dir, 'detection_results'
            )
            
            self.get_logger().info(f'📁 Scan directory updated: {self.current_scan_dir}')
            
            # 检查tracking_selection文件是否存在
            selection_file = self.config.paths['tracking_selection']
            if os.path.exists(selection_file):
                self.get_logger().info(f'✅ Found tracking selection file: {selection_file}')
            else:
                self.get_logger().warn(f'⚠️ Tracking selection file not found: {selection_file}')
                
        except json.JSONDecodeError as e:
            self.get_logger().error(f'Failed to parse detection complete JSON: {e}')
        except Exception as e:
            self.get_logger().error(f'Error in detection complete callback: {e}')

    def detection_result_callback(self, msg):
        """检测结果回调"""
        try:
            # 解析JSON检测结果
            detection_data = json.loads(msg.data)
            
            self.get_logger().info(f"🔍 Received detection: {detection_data.get('detection_count', 0)} objects")
            
            with self.data_lock:
                self.last_detection_time = self.get_clock().now()
                
                # 更新视觉追踪器
                self._update_visual_tracker(detection_data)
                
                # 处理检测结果
                control_command = self.tracking_core.process_detection_result(detection_data)
                
                if control_command:
                    # 使用位姿控制器计算精确目标
                    enhanced_command = self._enhance_control_command(control_command, detection_data)
                    self._execute_control_command(enhanced_command)
                    
                    # 尝试发布可视化
                    self._publish_tracking_visualization(detection_data, enhanced_command)
                else:
                    self.get_logger().warn("❌ No control command generated")
                    
        except json.JSONDecodeError as e:
            self.get_logger().error(f'Failed to parse detection JSON: {e}')
        except Exception as e:
            self.get_logger().error(f'Error in detection callback: {e}')
            import traceback
            traceback.print_exc()
    
    def _publish_tracking_visualization(self, detection_data, command):
        """发布追踪可视化"""
        try:
            # 简单的可视化信息（JSON格式）
            viz_data = {
                'target_id': self.tracking_core.target_object_id,
                'detection_count': detection_data.get('detection_count', 0),
                'command_phase': command.get('phase', 'UNKNOWN'),
                'distance_mm': command.get('distance_mm', 0),
                'timestamp': self.get_clock().now().nanoseconds
            }
            
            # 找到目标对象的信息
            for obj in detection_data.get('objects', []):
                if obj.get('object_id') == self.tracking_core.target_object_id:
                    viz_data['target_bbox'] = obj.get('bounding_box', [])
                    viz_data['target_confidence'] = obj.get('confidence', 0)
                    break
            
            # 创建简单的可视化消息（使用String暂时代替Image）
            viz_msg = String()
            viz_msg.data = json.dumps(viz_data, indent=2)
            
            # 发布到tracking_status话题（临时）
            self.get_logger().info(f"📸 Publishing visualization: phase={viz_data.get('command_phase')}, dist={viz_data.get('distance_mm'):.1f}mm")
            
        except Exception as e:
            self.get_logger().error(f'Error publishing visualization: {e}')

    def current_pose_callback(self, msg):
        """当前机械臂位姿回调"""
        with self.data_lock:
            # 更新内部位姿表示
            self.current_arm_pose = {
                'position': [
                    msg.pose.position.x,
                    msg.pose.position.y, 
                    msg.pose.position.z
                ],
                'orientation': [
                    msg.pose.orientation.x,
                    msg.pose.orientation.y,
                    msg.pose.orientation.z,
                    msg.pose.orientation.w
                ]
            }
            
            # 更新追踪核心和位姿控制器
            pose_dict = {
                'position': {
                    'x': msg.pose.position.x,
                    'y': msg.pose.position.y,
                    'z': msg.pose.position.z
                },
                'orientation': {
                    'x': msg.pose.orientation.x,
                    'y': msg.pose.orientation.y,
                    'z': msg.pose.orientation.z,
                    'w': msg.pose.orientation.w
                }
            }
            self.pose_controller.update_current_pose(pose_dict)
            self.tracking_core.update_current_pose(pose_dict)

    def _enhance_control_command(self, command, detection_data):
        """使用位姿控制器增强控制命令"""
        try:
            # 查找目标检测
            target_detection = None
            objects = detection_data.get('objects', [])
            
            if not objects:
                self.get_logger().warn("No objects in detection data")
                return command
            
            for obj in objects:
                if obj.get('object_id') == self.tracking_core.target_object_id:
                    target_detection = obj
                    break
            
            if not target_detection:
                self.get_logger().warn(f"Target {self.tracking_core.target_object_id} not found in {len(objects)} objects")
                return command
            
            # 使用位姿控制器计算精确位姿
            phase = command.get('phase', 'TRACKING')
            calculated_pose = self.pose_controller.calculate_target_pose(target_detection, phase)
            
            # 安全限制：所有z坐标最小350mm
            if calculated_pose and 'position' in calculated_pose:
                calculated_pose['position']['z'] = max(350, calculated_pose['position']['z'])
                
                self.get_logger().debug(
                    f"Enhanced pose: x={calculated_pose['position']['x']:.1f}, "
                    f"y={calculated_pose['position']['y']:.1f}, "
                    f"z={calculated_pose['position']['z']:.1f}, "
                    f"yaw={calculated_pose.get('orientation', {}).get('yaw', 0):.1f}"
                )
            
            # 更新命令
            enhanced_command = command.copy()
            if calculated_pose:
                enhanced_command['pose'] = calculated_pose
            
            return enhanced_command
            
        except Exception as e:
            self.get_logger().error(f'Failed to enhance control command: {e}')
            import traceback
            traceback.print_exc()
            return command

    def _execute_control_command(self, command):
        """执行控制命令"""
        try:
            # 发布位姿命令
            if 'pose' in command:
                self._publish_pose_command(command['pose'])
            
            # 发布夹爪命令
            if 'gripper' in command:
                self._publish_gripper_command(command['gripper'])
                
            # 记录执行状态
            phase = command.get('phase', 'UNKNOWN')
            distance = command.get('distance_mm', 0)
            state = command.get('state', 'UNKNOWN')
            
            self.get_logger().debug(
                f'📋 Executed: {state}→{phase}, dist={distance:.1f}mm'
            )
            
        except Exception as e:
            self.get_logger().error(f'Failed to execute control command: {e}')

    def _publish_pose_command(self, pose_cmd):
        """发布位姿命令"""
        pose_msg = PoseStamped()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = "base_link"
        
        # 位置
        position = pose_cmd.get('position', {})
        pose_msg.pose.position.x = float(position.get('x', 0))
        pose_msg.pose.position.y = float(position.get('y', 0))
        # 安全限制：最小高度350mm
        pose_msg.pose.position.z = max(350.0, float(position.get('z', 350)))
        
        # 姿态（欧拉角转四元数）
        orientation = pose_cmd.get('orientation', {})
        roll = math.radians(orientation.get('roll', 179))
        pitch = math.radians(orientation.get('pitch', 0))
        yaw = math.radians(orientation.get('yaw', 0))
        
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        
        pose_msg.pose.orientation.x = qx
        pose_msg.pose.orientation.y = qy
        pose_msg.pose.orientation.z = qz
        pose_msg.pose.orientation.w = qw
        
        self.target_pose_pub.publish(pose_msg)

    def _publish_gripper_command(self, gripper_cmd):
        """发布夹爪命令"""
        gripper_msg = String()
        
        # 构建JSON格式的夹爪命令
        gripper_data = {
            'position': gripper_cmd.get('position', 850),
            'action': gripper_cmd.get('action', 'open'),
            'timestamp': self.get_clock().now().nanoseconds
        }
        
        gripper_msg.data = json.dumps(gripper_data)
        self.gripper_target_pub.publish(gripper_msg)

    def _publish_tracking_visualization(self, detection_data, command):
        """发布追踪可视化"""
        try:
            if self.current_color_image is None:
                return
            
            # 创建可视化图像
            viz_img = self.current_color_image.copy()
            
            # 绘制检测结果
            for obj in detection_data.get('objects', []):
                self._draw_detection_on_image(viz_img, obj)
            
            # 绘制追踪状态信息
            self._draw_tracking_status(viz_img, command)
            
            # 手动创建ROS图像消息避免cv_bridge冲突
            viz_msg = Image()
            viz_msg.header.stamp = self.get_clock().now().to_msg()
            viz_msg.header.frame_id = "camera_color_optical_frame"
            viz_msg.height = viz_img.shape[0]
            viz_msg.width = viz_img.shape[1]
            viz_msg.encoding = "bgr8"
            viz_msg.is_bigendian = False
            viz_msg.step = viz_img.shape[1] * 3
            viz_msg.data = viz_img.tobytes()
            
            self.visualization_pub.publish(viz_msg)
            
        except Exception as e:
            self.get_logger().error(f'Error publishing visualization: {e}')

    def _draw_detection_on_image(self, img, obj):
        """在图像上绘制检测结果"""
        try:
            bbox = obj.get('bounding_box', [0, 0, 0, 0])
            object_id = obj.get('object_id', 'unknown')
            confidence = obj.get('match_confidence', 0.0)
            
            x1, y1, x2, y2 = map(int, bbox)
            
            # 绘制边界框
            color = (0, 255, 0) if object_id == self.tracking_core.target_object_id else (255, 0, 0)
            thickness = 3 if object_id == self.tracking_core.target_object_id else 2
            
            cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
            
            # 绘制标签
            label = f"{object_id} ({confidence:.2f})"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(img, (x1, y1 - label_size[1] - 10), (x1 + label_size[0], y1), color, -1)
            cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
        except Exception as e:
            self.get_logger().error(f'Error drawing detection: {e}')

    def _draw_tracking_status(self, img, command):
        """在图像上绘制追踪状态"""
        try:
            h, w = img.shape[:2]
            
            # 状态信息
            state = command.get('state', 'UNKNOWN')
            phase = command.get('phase', 'UNKNOWN')
            distance = command.get('distance_mm', 0)
            
            # 绘制状态栏
            cv2.rectangle(img, (10, 10), (w - 10, 100), (0, 0, 0), -1)
            cv2.rectangle(img, (10, 10), (w - 10, 100), (255, 255, 255), 2)
            
            # 状态文本
            status_text = f"State: {state} | Phase: {phase}"
            cv2.putText(img, status_text, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            target_text = f"Target: {self.tracking_core.target_object_id} | Distance: {distance:.1f}mm"
            cv2.putText(img, target_text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # 追踪时间
            if hasattr(self.tracking_core, 'tracking_start_time') and self.tracking_core.tracking_start_time:
                tracking_time = time.time() - self.tracking_core.tracking_start_time
                time_text = f"Tracking Time: {tracking_time:.1f}s"
                cv2.putText(img, time_text, (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
        except Exception as e:
            self.get_logger().error(f'Error drawing status: {e}')

    def publish_status(self):
        """发布追踪状态"""
        try:
            # 获取各组件状态
            tracking_status = self.tracking_core.get_status()
            state_status = self.state_machine.get_status()
            
            # 检查pose_controller状态
            try:
                control_status = self.pose_controller.get_control_status()
            except Exception as e:
                self.get_logger().error(f'Error getting control status: {e}')
                control_status = {'error': str(e)}
            
            # 综合状态
            status = {
                'tracking': tracking_status,
                'state_machine': state_status,
                'pose_control': control_status,
                'scan_directory': self.current_scan_dir,
                'reference_features_count': len(self.reference_features_db),
                'last_detection': self.last_detection_time.nanoseconds if self.last_detection_time else None,
                'arm_pose_available': self.current_arm_pose is not None,
                'realtime_detection_active': self.realtime_detection_timer is not None
            }
            
            status_msg = String()
            status_msg.data = json.dumps(status, indent=2)
            self.status_pub.publish(status_msg)
            
            # 每10秒记录一次状态摘要
            if hasattr(self, '_last_status_log'):
                if time.time() - self._last_status_log > 10:
                    self._log_status_summary(status)
                    self._last_status_log = time.time()
            else:
                self._last_status_log = time.time()
            
        except Exception as e:
            self.get_logger().error(f'Error publishing status: {e}')
            import traceback
            traceback.print_exc()
    
    def _log_status_summary(self, status):
        """记录状态摘要"""
        tracking_state = status.get('tracking', {}).get('state', 'UNKNOWN')
        target_id = status.get('tracking', {}).get('target_id', 'None')
        lost_frames = status.get('tracking', {}).get('lost_frames', 0)
        features_count = status.get('reference_features_count', 0)
        
        self.get_logger().info(
            f"📊 Status: {tracking_state}, Target: {target_id}, "
            f"Lost: {lost_frames}, Features: {features_count}"
        )

    def start_tracking_from_selection(self):
        """从选择文件启动追踪"""
        if not self.current_scan_dir:
            self.get_logger().error('No scan directory available')
            return False
        
        if not self.reference_features_db:
            self.get_logger().error('No reference features database loaded')
            return False
        
        # 启动追踪核心
        success = self.tracking_core.start_tracking()
        
        if success:
            # 状态机转换到SEARCHING
            self.state_machine.transition_to(TrackingState.SEARCHING)
            self.get_logger().info('🚀 Real-time tracking started successfully')
            
            # 开始实时检测（如果还没开始的话）
            self._start_realtime_detection_loop()
        else:
            self.get_logger().error('❌ Failed to start tracking')
        
        return success

    def _start_realtime_detection_loop(self):
        """启动实时检测循环"""
        if self.realtime_detection_timer is None:
            # 创建实时检测定时器 (10Hz)
            self.realtime_detection_timer = self.create_timer(0.1, self._realtime_detection_timer_callback)
            self.get_logger().info('🔄 Real-time detection loop started')

    def _realtime_detection_timer_callback(self):
        """实时检测定时器回调"""
        # 检查是否需要继续实时检测
        if self.tracking_core.current_state == TrackingState.IDLE:
            self._stop_realtime_detection_loop()
            return
        
        # 实时检测已在图像回调中处理，这里只做状态检查
        pass

    def _stop_realtime_detection_loop(self):
        """停止实时检测循环"""
        if self.realtime_detection_timer:
            self.realtime_detection_timer.cancel()
            self.realtime_detection_timer = None
            self.get_logger().info('⏹️ Real-time detection loop stopped')

    def stop_tracking(self):
        """停止追踪"""
        success = self.tracking_core.stop_tracking()
        
        if success:
            # 重置所有组件
            self.state_machine.reset()
            self.visual_tracker.reset()
            self.pose_controller.reset()
            
            # 停止实时检测
            self._stop_realtime_detection_loop()
            
            self.get_logger().info('⏹️ Enhanced tracking stopped')
        else:
            self.get_logger().error('❌ Failed to stop tracking')
        
        return success

    def emergency_stop(self):
        """紧急停止"""
        self.get_logger().warn('🚨 Emergency stop triggered')
        
        # 强制状态机转换
        self.state_machine.force_transition(
            TrackingState.IDLE, 
            "Emergency Stop"
        )
        
        return self.stop_tracking()


def main(args=None):
    rclpy.init(args=args)
    
    try:
        tracking_node = TrackingNode()
        
        # 启动时等待检测完成信号
        tracking_node.get_logger().info('Waiting for detection complete signal...')
        tracking_node.get_logger().info('Real-time YOLO+SAM2+ID matching ready!')
        
        rclpy.spin(tracking_node)
        
    except KeyboardInterrupt:
        tracking_node.get_logger().info('Tracking node interrupted')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if 'tracking_node' in locals():
            tracking_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()