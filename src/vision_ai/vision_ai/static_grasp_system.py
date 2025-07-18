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
            if width > height:
                dis = max(150, min(500, int(height * 2 - 10)))  # Calculate gripper width based on shorter one
                yaw_angle = -angle + 90 + scan_yaw
            else:
                yaw_angle = -angle + scan_yaw
                dis = max(150, min(500, int(width * 2 - 10)))   # Calculate gripper width based on shorter one
            
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
        compensated_y = target_y - offset_y
        compensated_z = target_z + offset_z
        
        self.get_logger().info(f'🔧 Pitch compensation: pitch={pitch_deg}°, yaw={yaw_deg}°')
        self.get_logger().info(f'   Offset: dx={offset_x:.1f}, dy={offset_y:.1f}, dz={offset_z:.1f}')
        self.get_logger().info(f'   Original coordinates: [{target_x:.1f}, {target_y:.1f}, {target_z:.1f}]')
        self.get_logger().info(f'   Compensated: [{compensated_x:.1f}, {compensated_y:.1f}, {compensated_z:.1f}]')
        
        return compensated_x, compensated_y, compensated_z

    def execute_single_grasp_and_place(self, target: Dict) -> bool:
        """Execute grasp and place sequence for a single target - using new gripper control"""
        try:
            self.get_logger().info(f' Starting grasp sequence for: {target["description"]}')
            
            target_x, target_y, target_z = target['world_coordinates'][:3]
            
            yaw, wid = self.calculate_yaw_from_mask(target['mask'], target.get('scan_detail'))
            height_mm = target['features'].get('depth_info', {}).get('height_mm', 30.0)
            
            self.get_logger().info(f' Grasp parameters: yaw={yaw:.1f}°, wid={wid}, height={height_mm:.1f}mm')
            
            strategy = self.plan_grasp_strategy(height_mm, yaw)
            
            # Calculate actual grasp position
            actual_grasp_z = target_z + strategy['z_offset_grasp']
            
            # Calculate pitch compensation
            compensated_x, compensated_y, compensated_z = self.calculate_pitch_compensation(
                target_x, target_y, actual_grasp_z, 
                strategy['pitch'], yaw
            )
            
            # # 1.  Open gripper to suitable pre-grasp position
            # pre_grasp_width = max(wid + 100, 600)  # 100mm wider than target
            # self.get_logger().info(f' Step 1: Setting gripper to pre-grasp width: {pre_grasp_width}')
            # if not self.call_gripper_set_position(pre_grasp_width):
            #     self.get_logger().warn(' Gripper set might have failed, but continuing execution')
            # time.sleep(2)  #  Add wait time
            self.get_logger().info(' Step 1 complete')
            
            # 2. Move to safe pre-grasp position
            safe_z_approach = max(actual_grasp_z + 100, 350)
            pre_comp_x, pre_comp_y, pre_comp_z = self.calculate_pitch_compensation(
                target_x, target_y, safe_z_approach, 0, yaw
            )
            
            self.get_logger().info(f' Step 2: Moving to safe pre-grasp position: [{pre_comp_x:.1f}, {pre_comp_y:.1f}, {pre_comp_z:.1f}]')
            if not self.move_to_pose(pre_comp_x, pre_comp_y, pre_comp_z, 180, 0, yaw):
                self.get_logger().error(' Step 2 failed')
                return False
            time.sleep(1)
            self.get_logger().info(' Step 2 complete')
            
            # 3. Descend to grasp position
            self.get_logger().info(f' Step 3: Descending to grasp position: [{compensated_x:.1f}, {compensated_y:.1f}, {compensated_z:.1f}] pitch={strategy["pitch"]:.1f}°')
            if not self.move_to_pose(compensated_x, compensated_y, compensated_z, 180, strategy['pitch'], yaw):
                self.get_logger().error(' Step 3 failed')
                return False
            time.sleep(1)
            self.get_logger().info(' Step 3 complete')
            
            # 4.  Close gripper to calculated width
            self.get_logger().info(f' Step 4: Closing gripper to width: {wid}')
            if not self.call_gripper_close(wid):
                self.get_logger().warn(' Gripper close might have failed, but continuing execution')
            time.sleep(2)  #  Add wait time
            self.get_logger().info(' Step 4 complete')
            
            # 5. Lift to safe height
            self.get_logger().info(' Step 5: Lifting to safe height...')
            if not self.move_to_pose(pre_comp_x, pre_comp_y, pre_comp_z, 180, 0, yaw):
                self.get_logger().error(' Step 5 failed')
                return False
            time.sleep(1)
            self.get_logger().info(' Step 5 complete')
            
            # 6-10. Placement steps
            placement_x, placement_y, placement_z_safe = 300, 0, 350
            self.get_logger().info(f' Step 6: Moving to placement area: [{placement_x}, {placement_y}, {placement_z_safe}]')
            if not self.move_to_pose(placement_x, placement_y, placement_z_safe, 180, 0, 0):
                self.get_logger().error(' Step 6 failed')
                return False
            time.sleep(1)
            self.get_logger().info(' Step 6 complete')
            
            # Descend to release position
            placement_z_release = compensated_z + 20
            self.get_logger().info(f'⬇ Step 7: Descending to release position: [{placement_x}, {placement_y}, {placement_z_release}]')
            if not self.move_to_pose(placement_x, placement_y, placement_z_release, 180, 0, 0):
                self.get_logger().error(' Step 7 failed')
                return False
            time.sleep(1)
            self.get_logger().info(' Step 7 complete')
            
            # Release gripper
            self.get_logger().info(' Step 8: Releasing object...')
            if not self.call_gripper_open():
                self.get_logger().error(' Step 8 failed')
                return False
            time.sleep(1)
            self.get_logger().info(' Step 8 complete')
            
            # Lift up
            self.get_logger().info(' Step 9: Lifting up...')
            if not self.move_to_pose(placement_x, placement_y, placement_z_safe, 180, 0, 0):
                self.get_logger().error(' Step 9 failed')
                return False
            time.sleep(1)
            self.get_logger().info(' Step 9 complete')
            
            # Return to initial position
            self.get_logger().info(' Step 10: Returning to initial position...')
            if not self.call_service(self.go_home_client):
                self.get_logger().error(' Step 10 failed')
                return False
            
            self.get_logger().info(f' Full grasp sequence successful: {target["description"]}')
            return True
            
        except Exception as e:
            self.get_logger().error(f'Single grasp sequence failed for {target.get("description", "unknown object")}: {e}')
            return False
    
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
        
        if height_mm < 80:
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