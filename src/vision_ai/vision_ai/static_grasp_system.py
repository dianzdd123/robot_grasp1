import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String, Int32
from sensor_msgs.msg import Image
from std_srvs.srv import Trigger
import cv2
import numpy as np
import json
import os
import time
import threading
from cv_bridge import CvBridge
from typing import Dict, List, Optional
import re

#  Import new gripper service interfaces
try:
    from vision_ai_interfaces.srv import SetGripperPosition, SetGripperClose
    GRIPPER_SERVICES_AVAILABLE = True
except ImportError:
    print("Warning: vision_ai_interfaces.srv not found. Using fallback mode.")
    GRIPPER_SERVICES_AVAILABLE = False

#  Temporarily disable new services, force topic mode
GRIPPER_SERVICES_AVAILABLE = False  # Force topic mode for testing

class AutomatedStaticGraspSystem(Node):
    """Fully automated static grasp system with enhanced gripper control"""
    
    def __init__(self):
        super().__init__('automated_static_grasp')
        
        # System state
        self.detection_targets = []
        self.selected_object_ids = []
        self.current_target_idx = 0
        self.system_state = "WAITING_FOR_DETECTION"
        self.detection_output_dir = None
        
        # Camera and visualization
        self.bridge = CvBridge()
        self.current_image = None
        self.display_image = None
        
        # ROS2 Publishers
        self.target_pose_pub = self.create_publisher(PoseStamped, '/xarm/target_pose', 10)
        self.gripper_control_pub = self.create_publisher(Int32, '/xarm/gripper_target', 10)
        
        # ROS2 Subscribers
        self.detection_complete_sub = self.create_subscription(
            String, '/detection_complete', self.detection_complete_callback, 10)
        self.color_image_sub = self.create_subscription(
            Image, '/camera/color/image_raw', self.image_callback, 10)
        
        #  Update: ROS2 Service Clients - supporting new gripper services
        self.gripper_open_client = self.create_client(Trigger, '/xarm/gripper_open')
        self.gripper_close_client = self.create_client(Trigger, '/xarm/gripper_close')
        self.go_home_client = self.create_client(Trigger, '/xarm/go_home')
        
        #  Check if services are actually available
        self.enhanced_gripper_available = False
        if GRIPPER_SERVICES_AVAILABLE:
            self.gripper_set_position_client = self.create_client(
                SetGripperPosition, '/xarm/set_gripper_position')
            self.gripper_close_with_pos_client = self.create_client(
                SetGripperClose, '/xarm/gripper_close_with_position')
            
            #  Check if services truly exist
            self.create_timer(1.0, self.check_enhanced_services)
        
        # Timer for display update
        self.display_timer = self.create_timer(0.1, self.update_display)
        
        self.get_logger().info('🤖 Automated Static Grasp System initialized with enhanced gripper support')
        self.get_logger().info(f'Gripper services imported: {GRIPPER_SERVICES_AVAILABLE}')
        self.get_logger().info('⏳ Waiting for detection complete signal...')

    
    def check_enhanced_services(self):
        if not self.enhanced_gripper_available:
            service_names = self.get_service_names_and_types()
            has_set_position = any('/xarm/set_gripper_position' in name for name, _ in service_names)
            has_close_with_pos = any('/xarm/gripper_close_with_position' in name for name, _ in service_names)
            
            if has_set_position and has_close_with_pos:
                self.enhanced_gripper_available = True
                self.get_logger().info(' Enhanced gripper services are available')
            else:
                self.get_logger().warn(' Enhanced gripper services not found, using basic mode')
                self.destroy_timer(self.get_timer_by_callback(self.check_enhanced_services))
    
    def get_timer_by_callback(self, callback):
        for timer in self._timers:
            if timer.callback == callback:
                return timer
        return None
    
    def call_gripper_set_position(self, position: int, timeout=5.0) -> bool:
        try:
            self.get_logger().info(f'Using topic mode for gripper position: {position}')
            position_msg = Int32()
            position_msg.data = max(0, min(850, position))
            self.gripper_control_pub.publish(position_msg)
            time.sleep(2)
            return True
        except Exception as e:
            self.get_logger().error(f'Error calling gripper set position: {e}')
            return False
    
    def call_gripper_close(self, position: int = None, timeout=5.0) -> bool:
        try:
            if position is None:
                return self.call_service(self.gripper_close_client, timeout)
            self.get_logger().info(f'Using topic mode for gripper close: {position}')
            position_msg = Int32()
            position_msg.data = max(0, min(850, position))
            self.gripper_control_pub.publish(position_msg)
            time.sleep(2) 
            return True
        except Exception as e:
            self.get_logger().error(f'Error calling gripper close: {e}')
            return False
    
    def call_gripper_open(self, timeout=5.0) -> bool:
        """open gripper"""
        return self.call_service(self.gripper_open_client, timeout)
    
    def detection_complete_callback(self, msg):
        """Detection complete callback - start automated grasping"""
        try:
            detection_data = json.loads(msg.data)
            self.detection_output_dir = detection_data.get('scan_directory')
            
            self.get_logger().info(f' Detection complete signal received: {self.detection_output_dir}')
            
            if self.load_detection_results_and_selection():
                self.get_logger().info(f' Loaded {len(self.detection_targets)} targets, {len(self.selected_object_ids)} selected')
                if self.detection_targets:
                    self.start_automated_grasping()
                else:
                    self.get_logger().warn('No selected targets found or loaded.')
            else:
                self.get_logger().error(' Failed to load detection results or selection.')
                
        except Exception as e:
            self.get_logger().error(f'Error processing detection signal: {e}')
    
    def load_detection_results_and_selection(self) -> bool:
        """Load detection results and filter based on tracking_selection.txt"""
        try:
            if not self.detection_output_dir:
                return False
            
            detection_results_dir = os.path.join(self.detection_output_dir, "detection_results")
            results_file = os.path.join(detection_results_dir, "detection_results.json")
            selection_file = os.path.join(detection_results_dir, "tracking_selection.txt")
            
            if not os.path.exists(results_file):
                self.get_logger().error(f'Detection results file not found: {results_file}')
                return False
            
            # Load selected object IDs
            self.selected_object_ids = self.load_selected_object_ids(selection_file)
            if not self.selected_object_ids:
                self.get_logger().warn(f'No object IDs found in {selection_file}. Aborting grasping sequence as no specific objects are selected.')
                return False 
            
            with open(results_file, 'r', encoding='utf-8') as f:
                detection_data = json.load(f)
            
            all_detected_objects = []
            for obj in detection_data.get('objects', []):
                world_coords = obj.get('features', {}).get('spatial', {}).get('world_coordinates')
                scan_angle = obj.get('features', {}).get('spatial', {}).get('scan_info', {})
                if not world_coords:
                    self.get_logger().warn(f'Object {obj["object_id"]} missing world coordinates, skipping in full list.')
                    continue
                
                mask_data = self.load_object_mask(obj, detection_results_dir)
                
                target = {
                    'object_id': str(obj['object_id']),
                    'class_name': obj['class_name'],
                    'confidence': obj['confidence'],
                    'world_coordinates': world_coords,
                    'scan_detail': scan_angle,
                    'bounding_box': obj['bounding_box'],
                    'features': obj['features'],
                    'description': obj['description'],
                    'mask': mask_data,
                    'original_position': world_coords.copy()
                }
                all_detected_objects.append(target)
            
            # Filter detection_targets based on selected_object_ids
            self.detection_targets = [
                obj for obj in all_detected_objects if obj['object_id'] in self.selected_object_ids
            ]
            
            if not self.detection_targets:
                self.get_logger().warn('No matching objects found from detection results for the selected IDs.')
                return False
            
            return True
            
        except Exception as e:
            self.get_logger().error(f'Failed to load detection results and selection: {e}')
            return False

    def load_selected_object_ids(self, selection_file_path: str) -> List[str]:
        """Load object IDs from tracking_selection.txt, extracting only the ID part."""
        selected_ids = []
        try:
            if not os.path.exists(selection_file_path):
                self.get_logger().warn(f'Tracking selection file not found: {selection_file_path}')
                return selected_ids
            
            with open(selection_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    match = re.search(r'\(ID:\s*([^)]+)\)', line)
                    if match:
                        object_id = match.group(1).strip()
                        if object_id:
                            selected_ids.append(object_id)
            self.get_logger().info(f'Loaded selected object IDs: {selected_ids}')
        except Exception as e:
            self.get_logger().error(f'Failed to load selected object IDs from {selection_file_path}: {e}')
        return selected_ids
    
    def load_object_mask(self, obj, detection_dir) -> Optional[np.ndarray]:
        """Load object mask from detection results - improved version"""
        try:
            mask_info = obj.get('mask_info')
            if mask_info and mask_info.get('contour_points'):
                contour_points = mask_info['contour_points']
                mask_shape = mask_info.get('mask_shape', (720, 1280))
                
                mask = np.zeros(mask_shape[:2], dtype=np.uint8)
                
                if contour_points:
                    contour = np.array(contour_points, dtype=np.int32).reshape((-1, 1, 2))
                    cv2.fillPoly(mask, [contour], 255)
                    
                    self.get_logger().info(f' Reconstructed mask from contour points for {obj["object_id"]}')
                    return mask
            
            bbox = obj['bounding_box']
            mask = np.zeros((720, 1280), dtype=np.uint8) 
            x1, y1, x2, y2 = map(int, bbox)
            mask[y1:y2, x1:x2] = 255
            
            self.get_logger().warn(f' Using bbox-based mask for {obj["object_id"]}')
            return mask
            
        except Exception as e:
            self.get_logger().error(f'Could not load mask for {obj["object_id"]}: {e}')
            return None
    
    def calculate_yaw_from_mask(self, mask: np.ndarray, scan_angles) -> tuple:
        """Calculate optimal yaw angle from object mask with scan compensation"""
        try:
            if mask is None:
                return 0.0, 300
            
            #  Correction: Safely get scan_yaw
            scan_yaw = 0.0
            if scan_angles and isinstance(scan_angles, (list, tuple)) and len(scan_angles) > 2:
                scan_yaw = scan_angles[2]
            elif scan_angles and isinstance(scan_angles, dict):
                scan_yaw = scan_angles.get('yaw', 0.0)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                return scan_yaw, 300
            
            largest_contour = max(contours, key=cv2.contourArea)
            rect = cv2.minAreaRect(largest_contour)
            _, (width, height), angle = rect
            
            self.get_logger().info(f"🔧 Rect: w={width:.1f}, h={height:.1f}, angle={angle:.1f}°, scan_yaw={scan_yaw:.1f}°")
            
            # Calculate yaw angle and gripper width
            if width < height:
                dis = max(150, min(500, int(height * 2 - 50)))  # Calculate gripper width based on shorter one
                yaw_angle = -angle + 90 + scan_yaw
            else:
                yaw_angle = -angle + scan_yaw
                dis = max(150, min(500, int(width * 2 - 50)))   # Calculate gripper width based on shorter one
            
            # Normalize yaw angle to [-180, 180]
            while yaw_angle > 180:
                yaw_angle -= 360
            while yaw_angle < -180:
                yaw_angle += 360
            
            # Continuity optimization
            if hasattr(self, 'last_yaw'):
                current_yaw = self.last_yaw
                options = [yaw_angle, yaw_angle + 180, yaw_angle - 180]
                options = [(opt + 180) % 360 - 180 for opt in options]
                best_yaw = min(options, key=lambda opt: abs(opt - current_yaw))
                self.get_logger().info(f"🔄 Best yaw: {best_yaw:.1f}° (gripper width: {dis})")
                yaw_angle = best_yaw
            else:
                self.get_logger().info(f" First yaw: {yaw_angle:.1f}° (gripper width: {dis})")
            
            self.last_yaw = yaw_angle
            return yaw_angle, dis
            
        except Exception as e:
            self.get_logger().error(f'Yaw calculation failed: {e}')
            return getattr(self, 'last_yaw', 0.0), 300
    
    def start_automated_grasping(self):
        """Start automated grasping sequence"""
        if not self.detection_targets:
            self.get_logger().warn('No selected targets to grasp')
            self.system_state = "COMPLETED"
            return
        
        self.system_state = "GRASPING"
        self.current_target_idx = 0
        
        self.get_logger().info(f'🤖 Starting automated grasping of {len(self.detection_targets)} selected objects')
        
        threading.Thread(target=self.automated_grasp_sequence, daemon=True).start()
    
    def automated_grasp_sequence(self):
        """Execute automated grasping sequence for all targets"""
        try:
            self.get_logger().info(' Going to home position before starting sequence...')

            for i, target in enumerate(self.detection_targets):
                self.current_target_idx = i
                self.get_logger().info(f' Grasping object {i+1}/{len(self.detection_targets)}: {target["description"]} (ID: {target["object_id"]})')
                
                if self.execute_single_grasp_and_place(target):
                    self.get_logger().info(f' Successfully processed {target["description"]}')
                else:
                    self.get_logger().error(f' Failed to process {target["description"]}')
                
                time.sleep(2)
            
            self.system_state = "COMPLETED"
            self.get_logger().info(' All objects processed successfully!')
            
        except Exception as e:
            self.get_logger().error(f'Automated sequence failed: {e}')
            self.system_state = "ERROR"
    
    def calculate_pitch_compensation(self, target_x, target_y, target_z, pitch_deg, yaw_deg, gripper_length=120.0):
        """Calculate pitch angle compensation"""
        import math
        
        pitch_rad = math.radians(pitch_deg)
        yaw_rad = math.radians(yaw_deg)
        
        offset_forward = gripper_length * math.sin(-pitch_rad)
        offset_down = gripper_length * (1 - math.cos(-pitch_rad))
        
        offset_x = offset_forward * math.cos(yaw_rad)
        offset_y = offset_forward * math.sin(yaw_rad)
        offset_z = offset_down
        
        compensated_x = target_x - offset_x
        compensated_y = target_y - offset_y*0.8
        compensated_z = target_z + offset_z
        
        self.get_logger().info(f'🔧 Pitch compensation: pitch={pitch_deg}°, yaw={yaw_deg}°')
        self.get_logger().info(f'   Offset: dx={offset_x:.1f}, dy={offset_y:.1f}, dz={offset_z:.1f}')
        self.get_logger().info(f'   Original coordinates: [{target_x:.1f}, {target_y:.1f}, {target_z:.1f}]')
        self.get_logger().info(f'   Compensated: [{compensated_x:.1f}, {compensated_y:.1f}, {compensated_z:.1f}]')
        
        return compensated_x, compensated_y, compensated_z

    def execute_single_grasp_and_place(self, target: Dict) -> bool:
        """执行抓取和放置序列 - 使用正确的补偿公式"""
        try:
            self.get_logger().info(f' 开始抓取序列: {target["description"]}')
            
            # 获取增强信息
            depth_info = target.get('features', {}).get('depth_info', {})
            spatial_features = target.get('features', {}).get('spatial', {})
            gripper_info = spatial_features.get('gripper_width_info', {})
            
            # 基础位置信息
            target_x, target_y, target_z = target['world_coordinates'][:3]
            
            # 🆕 使用正确的背景Z补偿公式
            background_world_z = depth_info.get('background_world_z', target_z)
            background_depth_m = depth_info.get('background_depth_m', 0.3)
            object_height_mm = depth_info.get('height_mm', 30.0)
            
            # 🆕 计算真实的背景补偿高度
            background_z_compensated = background_world_z - (background_depth_m * 1000)
            
            self.get_logger().info(f'📏 深度信息分析:')
            self.get_logger().info(f'   背景世界Z: {background_world_z:.1f}mm')
            self.get_logger().info(f'   背景深度: {background_depth_m:.3f}m ({background_depth_m*1000:.1f}mm)')
            self.get_logger().info(f'   补偿后背景Z: {background_z_compensated:.1f}mm')
            self.get_logger().info(f'   物体高度: {object_height_mm:.1f}mm')
            
            # 🆕 使用正确的抓夹宽度计算公式
            if gripper_info and 'real_width_mm' in gripper_info:
                real_width_mm = gripper_info['real_width_mm']
                
                # 你的公式：
                # 预抓取宽度 = real_width_mm * 10 + 50
                # 最终抓取宽度 = real_width_mm * 10 - 100
                pre_grasp_width = int(real_width_mm * 10 + 50)
                final_grasp_width = int(real_width_mm * 10 - 150)
                
                # 确保在合理范围内
                pre_grasp_width = max(400, min(850, pre_grasp_width))
                final_grasp_width = max(50, min(800, final_grasp_width))
                
                self.get_logger().info(f'🤏 抓夹宽度计算:')
                self.get_logger().info(f'   实际宽度: {real_width_mm:.1f}mm')
                self.get_logger().info(f'   预抓取宽度: {real_width_mm:.1f} * 10 + 50 = {pre_grasp_width}')
                self.get_logger().info(f'   最终抓取宽度: {real_width_mm:.1f} * 10 - 100 = {final_grasp_width}')
                
            else:
                # 回退到原有计算方法
                yaw, backup_width = self.calculate_yaw_from_mask(target['mask'], spatial_features.get('scan_detail'))
                pre_grasp_width = max(backup_width + 100, 600)
                final_grasp_width = backup_width
                self.get_logger().warn('⚠️ 未找到real_width_mm，使用备用抓夹宽度计算')
            
            # 计算yaw角度
            yaw, _ = self.calculate_yaw_from_mask(target['mask'], spatial_features.get('scan_detail'))
            
            self.get_logger().info(f' 抓取参数总结:')
            self.get_logger().info(f'   yaw角度: {yaw:.1f}°')
            self.get_logger().info(f'   预抓取宽度: {pre_grasp_width}')
            self.get_logger().info(f'   最终抓取宽度: {final_grasp_width}')
            
            # 🆕 基于补偿后的背景高度计算抓取策略
            strategy = self.plan_grasp_strategy_with_compensation(
                object_height_mm, background_z_compensated, yaw
            )
            
            # 🆕 计算实际抓取位置（基于补偿后的背景高度）
            actual_grasp_z = background_z_compensated + strategy['z_offset_above_background']
            
            self.get_logger().info(f'🎯 抓取高度计算:')
            self.get_logger().info(f'   补偿背景Z: {background_z_compensated:.1f}mm')
            self.get_logger().info(f'   Z偏移: {strategy["z_offset_above_background"]:.1f}mm')
            self.get_logger().info(f'   最终抓取Z: {actual_grasp_z:.1f}mm')
            
            # 计算pitch补偿
            compensated_x, compensated_y, compensated_z = self.calculate_pitch_compensation(
                target_x, target_y, actual_grasp_z, 
                strategy['pitch'], yaw
            )
            
            self.get_logger().info(f'🔧 Pitch补偿后坐标: [{compensated_x:.1f}, {compensated_y:.1f}, {compensated_z:.1f}]')
            
            # 执行抓取序列
            success = self._execute_enhanced_grasp_sequence(
                compensated_x, compensated_y, compensated_z,
                strategy, yaw, pre_grasp_width, final_grasp_width, 
                background_z_compensated, target
            )
            
            if success:
                self.get_logger().info(f'✅ 完整抓取序列成功: {target["description"]}')
            else:
                self.get_logger().error(f'❌ 抓取序列失败: {target["description"]}')
            
            return success
            
        except Exception as e:
            self.get_logger().error(f'单个抓取序列失败 {target.get("description", "unknown")}: {e}')
            import traceback
            traceback.print_exc()
            return False

    def plan_grasp_strategy_with_compensation(self, object_height_mm: float, background_z_compensated: float, yaw: float) -> Dict:
        """基于补偿后背景高度的抓取策略规划"""
        try:
            # 基础策略（基于物体高度）
            if object_height_mm < 20:
                base_pitch = 0.0
                height_offset = object_height_mm * 0.6  # 薄物体，稍微偏下抓取
            elif object_height_mm < 40:
                base_pitch = -5.0
                height_offset = object_height_mm * 0.8  # 中等薄度，中间偏上
            elif object_height_mm < 80:
                base_pitch = -15.0
                height_offset = object_height_mm * 1  # 中等物体
            elif object_height_mm < 120:
                base_pitch = -25.0
                height_offset = object_height_mm * 1  # 较高物体
            else:
                base_pitch = -35.0
                height_offset = min(object_height_mm * 0.8, 100)  # 高物体，但限制最大偏移
            
            # 🆕 根据补偿后的背景高度调整策略
            if background_z_compensated < 0:
                # 背景在基准面以下，需要更保守的策略
                pitch_adjustment = 5.0  # 减少倾斜
                height_adjustment = 10.0  # 增加高度偏移
                self.get_logger().info('⚠️ 背景低于基准面，使用保守策略')
            elif background_z_compensated > 200:
                # 背景较高，可以更积极
                pitch_adjustment = -5.0  # 增加倾斜
                height_adjustment = -5.0  # 减少高度偏移
                self.get_logger().info('📈 背景较高，使用积极策略')
            else:
                pitch_adjustment = 0.0
                height_adjustment = 20.0
            
            final_pitch = base_pitch + pitch_adjustment
            
            # 🆕 添加安全余量（相对于物体高度动态调整）
            if object_height_mm < 30:
                safety_margin = 110.0  # 薄物体需要更多安全余量
            else:
                safety_margin = 120.0
            
            z_offset_above_background = height_offset + height_adjustment + safety_margin
            
            self.get_logger().info(f'📋 抓取策略详情:')
            self.get_logger().info(f'   物体高度: {object_height_mm:.1f}mm')
            self.get_logger().info(f'   补偿背景Z: {background_z_compensated:.1f}mm')
            self.get_logger().info(f'   基础pitch: {base_pitch:.1f}° → 最终pitch: {final_pitch:.1f}°')
            self.get_logger().info(f'   高度偏移: {height_offset:.1f} + 调整{height_adjustment:.1f} + 安全{safety_margin:.1f} = {z_offset_above_background:.1f}mm')
            
            return {
                'pitch': final_pitch,
                'yaw': yaw,
                'z_offset_above_background': z_offset_above_background,
                'object_height': object_height_mm,
                'background_z_compensated': background_z_compensated,
                'safety_margin': safety_margin,
                'height_offset': height_offset
            }
            
        except Exception as e:
            self.get_logger().error(f'抓取策略规划失败: {e}')
            return {
                'pitch': 0.0,
                'yaw': yaw,
                'z_offset_above_background': 50.0,
                'object_height': 30.0,
                'background_z_compensated': background_z_compensated,
                'safety_margin': 15.0,
                'height_offset': 20.0
            }

    def _execute_enhanced_grasp_sequence(self, x, y, z, strategy, yaw, pre_width, final_width, background_z_compensated, target):
        """执行增强的抓取序列，使用补偿后的背景高度"""
        try:
            target_desc = target.get("description", "unknown object")
            
            # 1. 设置预抓取宽度
            self.get_logger().info(f'📐 步骤1: 设置预抓取宽度: {pre_width}')
            if not self.call_gripper_close(pre_width):
                self.get_logger().warn(' 预抓取宽度设置可能失败，继续执行')
            time.sleep(2)
            
            # 2. 🆕 计算多层安全高度（基于补偿后的背景）
            # 高安全位置：补偿背景 + 物体高度 + 大余量
            safe_z_high = max(background_z_compensated + strategy['object_height'] + 200,350)
            safe_comp_x, safe_comp_y, safe_comp_z = self.calculate_pitch_compensation(
                x, y, safe_z_high, 0, yaw
            )
            if yaw < -135 or -45 < y < 0:
                y = y - 20
                safe_comp_y = safe_comp_y - 20
            self.get_logger().info(f'🔝 步骤2: 移动到高安全位置')
            self.get_logger().info(f'   计算: {background_z_compensated:.1f} + {strategy["object_height"]:.1f} + 200 = {safe_z_high:.1f}mm')
            self.get_logger().info(f'   坐标: [{safe_comp_x:.1f}, {safe_comp_y:.1f}, {safe_comp_z:.1f}]')
            
            if not self.move_to_pose(safe_comp_x, safe_comp_y, safe_comp_z, 180, 0, yaw):
                self.get_logger().error(' 步骤2失败')
                return False
            time.sleep(1)
            
            # 3. 中等安全高度
            mid_safe_z = max(background_z_compensated + strategy['object_height'] + 100,z + 50)
            mid_pitch = strategy['pitch'] * 0.5
            mid_comp_x, mid_comp_y, mid_comp_z = self.calculate_pitch_compensation(
                x, y, mid_safe_z, mid_pitch, yaw
            )
            if yaw < -135 or -45 < y < 0:
                mid_comp_y = mid_comp_y - 20
            self.get_logger().info(f'🔄 步骤3: 移动到中等安全位置')
            self.get_logger().info(f'   高度: {background_z_compensated:.1f} + {strategy["object_height"]:.1f} + 100 = {mid_safe_z:.1f}mm')
            self.get_logger().info(f'   坐标: [{mid_comp_x:.1f}, {mid_comp_y:.1f}, {mid_comp_z:.1f}], pitch: {mid_pitch:.1f}°')
            
            if not self.move_to_pose(mid_comp_x, mid_comp_y, mid_comp_z, 180, mid_pitch, yaw):
                self.get_logger().error(' 步骤3失败')
                return False
            time.sleep(1)
            
            # 4. 下降到最终抓取位置
            self.get_logger().info(f'⬇️ 步骤4: 下降到最终抓取位置')
            self.get_logger().info(f'   目标坐标: [{x:.1f}, {y:.1f}, {z:.1f}]')
            self.get_logger().info(f'   pitch: {strategy["pitch"]:.1f}°, yaw: {yaw:.1f}°')
            
            if not self.move_to_pose(x, y, z, 180, strategy['pitch'], yaw):
                self.get_logger().error(' 步骤4失败')
                return False
            time.sleep(2)

            # 5. 🆕 执行最终抓取（使用计算出的宽度）
            self.get_logger().info(f'🤏 步骤5: 执行最终抓取')
            self.get_logger().info(f'   抓取宽度: {final_width} (来自公式: real_width * 10 - 100)')
            
            grasp_success = False
            
            # 尝试标准抓取
            if self.call_gripper_close(final_width):
                time.sleep(3)  # 给更多时间确保抓取稳定
                grasp_success = True
                self.get_logger().info('✅ 标准抓取成功')
            else:
                # 备用尝试：稍微松一点
                backup_width = final_width + 30
                self.get_logger().warn(f'⚠️ 标准抓取可能失败，尝试备用宽度: {backup_width}')
                if self.call_gripper_close(backup_width):
                    time.sleep(3)
                    grasp_success = True
                    self.get_logger().info('✅ 备用抓取成功')
            
            if not grasp_success:
                self.get_logger().error('❌ 步骤5: 所有抓取尝试都失败')
                return False
            
            # 6. 智能提升检查
            self.get_logger().info('🔍 步骤6: 轻微提升检查抓取效果')
            
            # 轻微提升检查是否抓住
            check_z = z + 100
            check_comp_x, check_comp_y, check_comp_z = self.calculate_pitch_compensation(
                x, y, check_z, strategy['pitch'], yaw
            )
            
            if not self.move_to_pose(check_comp_x, check_comp_y, check_comp_z, 180, strategy['pitch'], yaw):
                self.get_logger().error(' 步骤6失败')
                return False
            time.sleep(2)
            safe_com_z = max(check_comp_z + 50, 300)
            # 继续提升到安全高度
            self.get_logger().info('⬆️ 继续提升到安全高度')
            if not self.move_to_pose(safe_comp_x, safe_comp_y, safe_com_z, 180, 0, yaw):
                self.get_logger().error(' 提升到安全高度失败')
                return False
            time.sleep(1)
            
            # 7-10. 🆕 放置序列（使用补偿后的背景高度）
            placement_x, placement_y, placement_z_safe = 300, 0, 350
            
            self.get_logger().info(f'📦 步骤7: 移动到放置区域: [{placement_x}, {placement_y}, {placement_z_safe}]')
            if not self.move_to_pose(placement_x, placement_y, placement_z_safe, 180, 0, 0):
                self.get_logger().error(' 步骤7失败')
                return False
            time.sleep(1)
            
            # 🆕 使用补偿背景高度计算放置高度
            # 假设放置区域的背景高度与抓取区域类似
            placement_z_release = max(background_z_compensated + 40, 200)  # 至少50mm高度
            
            self.get_logger().info(f'⬇️ 步骤8: 下降到放置高度')
            self.get_logger().info(f'   放置高度: max({background_z_compensated:.1f} + 40, 50) = {placement_z_release:.1f}mm')
            
            if not self.move_to_pose(placement_x, placement_y, placement_z_release, 180, 0, 0):
                self.get_logger().error(' 步骤8失败')
                return False
            time.sleep(1)
            
            # 9. 释放物体
            self.get_logger().info('🔓 步骤9: 释放物体')
            if not self.call_gripper_close(800):
                self.get_logger().error(' 步骤9失败')
                return False
            time.sleep(3)
            
            # 11. 回到初始位置
            self.get_logger().info('🏠 步骤11: 返回初始位置')
            if not self.call_service(self.go_home_client):
                self.get_logger().error(' 步骤11失败')
                return False
            
            self.get_logger().info(f'🎉 完整增强抓取序列成功: {target_desc}')
            
            # 🆕 记录成功的参数用于后续优化
            self._log_successful_grasp_params(target, final_width, background_z_compensated, strategy)
            
            return True
            
        except Exception as e:
            self.get_logger().error(f'增强抓取序列执行失败: {e}')
            import traceback
            traceback.print_exc()
            return False

    def _log_successful_grasp_params(self, target, final_width, background_z_compensated, strategy):
        """记录成功的抓取参数，用于后续优化"""
        try:
            success_data = {
                'object_id': target.get('object_id'),
                'class_name': target.get('class_name'),
                'final_grasp_width': final_width,
                'background_z_compensated': background_z_compensated,
                'pitch_used': strategy['pitch'],
                'z_offset_used': strategy['z_offset_above_background'],
                'object_height': strategy['object_height']
            }
            
            self.get_logger().info('📝 成功参数记录:')
            for key, value in success_data.items():
                self.get_logger().info(f'   {key}: {value}')
                
        except Exception as e:
            self.get_logger().error(f'参数记录失败: {e}')    
    def move_to_pose(self, x, y, z, roll, pitch, yaw, timeout=10.0) -> bool:
        """Move to specified pose"""
        try:
            pose_msg = PoseStamped()
            pose_msg.header.stamp = self.get_clock().now().to_msg()
            pose_msg.header.frame_id = "link_base" 
            
            pose_msg.pose.position.x = float(x) 
            pose_msg.pose.position.y = float(y) 
            pose_msg.pose.position.z = float(z)
            
            # Euler to Quaternion
            roll_rad = np.deg2rad(roll)
            pitch_rad = np.deg2rad(pitch)
            yaw_rad = np.deg2rad(yaw)
            
            cy = np.cos(yaw_rad * 0.5)
            sy = np.sin(yaw_rad * 0.5)
            cp = np.cos(pitch_rad * 0.5)
            sp = np.sin(pitch_rad * 0.5)
            cr = np.cos(roll_rad * 0.5)
            sr = np.sin(roll_rad * 0.5)

            pose_msg.pose.orientation.w = cr * cp * cy + sr * sp * sy
            pose_msg.pose.orientation.x = sr * cp * cy - cr * sp * sy
            pose_msg.pose.orientation.y = cr * sp * cy + sr * cp * sy
            pose_msg.pose.orientation.z = cr * cp * sy - sr * sp * cy
            
            self.target_pose_pub.publish(pose_msg)
            
            time.sleep(3) 
            return True
            
        except Exception as e:
            self.get_logger().error(f'Move to pose failed: {e}')
            return False

    def plan_grasp_strategy(self, height_mm: float, yaw: float) -> Dict:
        """Plan grasp strategy based on object height"""
        pitch = 0.0 
        grasp_offset_from_target_z = 0.0
        if height_mm < 40:
            pitch = 0.0
            grasp_offset_from_target_z = 140            
        elif height_mm < 80:
            pitch = 0.0
            grasp_offset_from_target_z = 120
        elif height_mm < 120:
            pitch = -15.0
            grasp_offset_from_target_z = 0.5 * height_mm + 90
        elif height_mm < 160:
            pitch = -30.0
            grasp_offset_from_target_z = 0.5 * height_mm + 80
        else:
            pitch = -45.0
            grasp_offset_from_target_z = 0.5 * height_mm + 60

        self.get_logger().info(f'Grasp strategy: height={height_mm:.1f}mm, pitch: {pitch}°, yaw: {yaw:.1f}°')
        return {
            'pitch': pitch,
            'yaw': yaw,
            'z_offset_grasp': grasp_offset_from_target_z, 
            'height': height_mm
        }
    
    def call_service(self, client, timeout=5.0) -> bool:
        """Call a service and wait for response"""
        try:
            if not client.wait_for_service(timeout_sec=timeout):
                self.get_logger().error(f'Service not available: {client.srv_name}')
                return False
            
            request = Trigger.Request()
            future = client.call_async(request)
            
            time.sleep(1) 
            return True
            
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
            return False
    
    def image_callback(self, msg):
        """Camera image callback"""
        try:
            self.current_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f'Image conversion failed: {e}')
    
    def update_display(self):
        """Update live camera display with system status"""
        if self.current_image is None:
            return
        
        display = self.current_image.copy()
        h, w = display.shape[:2]
        
    def update_display(self):
        """Update live camera display with system status"""
        if self.current_image is None:
            return
        
        display = self.current_image.copy()
        h, w = display.shape[:2]
        
        # Draw system status
        status_text = f"System State: {self.system_state}"
        cv2.putText(display, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        #  显示夹爪服务状态
        gripper_status = "Enhanced" if GRIPPER_SERVICES_AVAILABLE else "Basic"
        cv2.putText(display, f"Gripper Mode: {gripper_status}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if self.system_state == "GRASPING" and self.detection_targets:
            if self.current_target_idx < len(self.detection_targets):
                current_target = self.detection_targets[self.current_target_idx]
                target_text = f"Processing: {current_target['description']} (ID: {current_target['object_id']}) ({self.current_target_idx+1}/{len(self.detection_targets)})"
                cv2.putText(display, target_text, (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                
                # Draw target bounding box
                bbox = current_target['bounding_box']
                x1, y1, x2, y2 = map(int, bbox)
                cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.putText(display, current_target['class_name'], (x1, y1-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.putText(display, "Processing last object or task nearing completion.", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        elif self.system_state == "WAITING_FOR_DETECTION":
            wait_text = "Waiting for detection complete signal..."
            cv2.putText(display, wait_text, (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        elif self.system_state == "COMPLETED":
            complete_text = "All selected objects processed successfully!"
            cv2.putText(display, complete_text, (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        cv2.imshow('Automated Static Grasp System', display)
        cv2.waitKey(1)
    
    def destroy_node(self):
        """Cleanup when node is destroyed"""
        cv2.destroyAllWindows()
        super().destroy_node()


def main(args=None):
    """Main function"""
    rclpy.init(args=args)
    
    try:
        node = AutomatedStaticGraspSystem()
        cv2.namedWindow('Automated Static Grasp System', cv2.WINDOW_AUTOSIZE)
        rclpy.spin(node)
    except KeyboardInterrupt:
        print(' System interrupted by user')
    except Exception as e:
        print(f' System error: {e}')
    finally:
        if 'node' in locals():
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()