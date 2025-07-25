#!/usr/bin/env python3
"""
Pose Controller for Tracking System
位姿控制器 - 比例控制、YAW计算、坐标转换
"""

import numpy as np
import cv2
import math
import time
import pyrealsense2 as rs
from scipy.spatial.transform import Rotation as R
from typing import Dict, Any, List, Tuple, Optional

from ..utils.config import TrackingConfig, DetectionResult, TrackingCommand, MotionRecord, TrackingState


class PoseController:
    """位姿控制器"""
    
    def __init__(self, config: TrackingConfig, logger=None):
        """
        初始化位姿控制器
        
        Args:
            config: 追踪配置
            logger: 日志记录器
        """
        self.config = config
        self.logger = logger
        
        # 控制参数
        self.tracking_params = config.tracking_params
        self.proportional_factor = config.get_proportional_factor()
        self.target_tolerance_xy = config.get_target_tolerance_xy()
        self.target_tolerance_yaw = config.get_target_tolerance_yaw()
        self.safe_height = config.get_safe_height()
        self.min_z_height = config.get_min_z_height()
        
        # 相机参数
        self.camera_config = config.camera_config
        
        # 当前状态
        self.current_arm_pose = None
        self.current_arm_pose_list = None  # 添加这个属性
        self.last_successful_pose = None
        self.motion_history = []
        
        # YAW计算历史
        self.last_yaw = None
        
        # 工作空间限制
        self.workspace_limits = {
            'x': (-800, 800),    # mm
            'y': (-800, 800),   # mm  
            'z': (100, 800)     # mm
        }
        
        self._log_info("🎮 位姿控制器初始化完成")
    
    def update_current_pose(self, arm_pose: Dict[str, Any]):
        """
        更新当前机械臂位姿
        
        Args:
            arm_pose: 机械臂位姿 {'position': {'x', 'y', 'z'}, 'orientation': {'x', 'y', 'z', 'w'}}
        """
        try:
            self.current_arm_pose = arm_pose
            
            # 转换为列表格式以兼容原始代码
            position = arm_pose['position']
            orientation = arm_pose['orientation']
            
            # 四元数转欧拉角
            qx, qy, qz, qw = orientation['x'], orientation['y'], orientation['z'], orientation['w']
            roll, pitch, yaw = self._quat_to_euler(qx, qy, qz, qw)
            
            self.current_arm_pose_list = [
                position['x'], position['y'], position['z'],
                roll, pitch, yaw
            ]
            
        except Exception as e:
            self._log_error(f"❌ 更新机械臂位姿失败: {e}")
    
    def calculate_target_pose(self, detection: DetectionResult, 
                            current_state: TrackingState) -> Optional[TrackingCommand]:
        """
        计算目标位姿
        
        Args:
            detection: 检测结果
            current_state: 当前追踪状态
        
        Returns:
            追踪命令
        """
        try:
            if not self.current_arm_pose:
                self._log_error("❌ 机械臂位姿未初始化")
                return None
            
            # 计算目标的世界坐标
            target_world_coords = self._calculate_world_coordinates(detection)
            if target_world_coords is None:
                return None
            
            target_x, target_y, target_z = target_world_coords
            
            # 获取当前位置
            current_x = self.current_arm_pose_list[0]
            current_y = self.current_arm_pose_list[1] 
            current_z = self.current_arm_pose_list[2]
            
            # 计算距离和YAW
            distance_xy = math.sqrt((target_x - current_x)**2 + (target_y - current_y)**2)
            target_yaw = self._calculate_target_yaw(detection)
            current_yaw = self.current_arm_pose_list[5]
            yaw_error = self._normalize_angle(target_yaw - current_yaw)
            
            # 根据状态决定控制策略
            if current_state == TrackingState.TRACKING:
                return self._calculate_proportional_move(
                    target_world_coords, target_yaw, distance_xy, yaw_error
                )
            elif current_state == TrackingState.APPROACHING:
                return self._calculate_approach_move(
                    target_world_coords, target_yaw, distance_xy, yaw_error
                )
            elif current_state == TrackingState.GRASPING:
                return self._calculate_grasp_move(
                    target_world_coords, target_yaw, detection
                )
            else:
                self._log_warn(f"⚠️ 不支持的状态: {current_state}")
                return None
                
        except Exception as e:
            self._log_error(f"❌ 计算目标位姿失败: {e}")
            return None
    
    def _calculate_world_coordinates(self, detection: DetectionResult) -> Optional[Tuple[float, float, float]]:
        """
        计算世界坐标 - 使用RealSense API
        
        Args:
            detection: 检测结果
        
        Returns:
            世界坐标 (x, y, z) 或 None
        """
        try:
            # 使用检测结果中的3D坐标（如果已经计算过）
            if detection.centroid_3d and detection.centroid_3d != (0.0, 0.0, 0.0):
                camera_coords = detection.centroid_3d
            else:
                # 如果没有3D坐标，则使用2D坐标估算
                # 这里需要深度图，暂时使用估算值
                estimated_depth = 300.0  # mm
                pixel_x, pixel_y = detection.centroid_2d
                camera_coords = self._pixel_to_camera_coords(pixel_x, pixel_y, estimated_depth)
            
            # 相机坐标转世界坐标
            world_coords = self._camera_to_world(camera_coords)
            
            return world_coords
            
        except Exception as e:
            self._log_error(f"❌ 计算世界坐标失败: {e}")
            return None
    
    def _pixel_to_camera_coords(self, pixel_x: float, pixel_y: float, depth_mm: float) -> Tuple[float, float, float]:
        """
        像素坐标转相机坐标（当无法使用RealSense API时的备用方法）
        
        Args:
            pixel_x: 像素X坐标
            pixel_y: 像素Y坐标
            depth_mm: 深度（毫米）
        
        Returns:
            相机坐标 (x, y, z)
        """
        try:
            intrinsics = self.camera_config.get('intrinsics', {})
            fx = intrinsics.get('fx', 912.694580078125)
            fy = intrinsics.get('fy', 910.309814453125)
            cx = intrinsics.get('cx', 640.0)
            cy = intrinsics.get('cy', 360.0)
            
            # 相机坐标系计算
            z_camera = depth_mm / 1000.0  # 转换为米
            x_camera = (pixel_x - cx) * z_camera / fx
            y_camera = (pixel_y - cy) * z_camera / fy
            
            return (x_camera * 1000, y_camera * 1000, z_camera * 1000)  # 返回毫米
            
        except Exception as e:
            self._log_error(f"❌ 像素坐标转换失败: {e}")
            return (0.0, 0.0, 300.0)
    
    def _camera_to_world(self, camera_point: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """
        相机坐标转世界坐标 - 基于你提供的算法
        
        Args:
            camera_point: 相机坐标 (x, y, z) 单位：毫米
        
        Returns:
            世界坐标 (x, y, z) 单位：毫米
        """
        try:
            if not self.current_arm_pose_list:
                self._log_error("❌ 机械臂位姿未设置")
                return camera_point
            
            # Step 1: 坐标轴重排（基于你的算法）
            x_c, y_c, z_c = camera_point
            camera_point_reordered = np.array([
                (y_c + 70),     # Y偏移
                (x_c - 50),     # X偏移  
                -(z_c - 180)    # Z偏移并反向
            ])
            
            # Step 2: 生成旋转矩阵
            curr_x, curr_y, curr_z, curr_roll, curr_pitch, curr_yaw = self.current_arm_pose_list
            
            # 相机姿态调整（基于你的算法）
            cam_orientation = [abs(curr_roll) - 180, curr_pitch, curr_yaw]
            roll, pitch, yaw = cam_orientation
            
            rotation = R.from_euler('XYZ', [roll, pitch, yaw], degrees=True)
            R_wc = rotation.as_matrix()
            
            # Step 3: 平移
            T_wc = np.array([curr_x, curr_y, curr_z])
            
            # Step 4: 应用旋转 + 平移
            world_point = R_wc @ camera_point_reordered + T_wc
            
            self._log_debug(f"🔄 坐标转换: 相机{camera_point} → 世界{world_point}")
            
            return tuple(world_point)
            
        except Exception as e:
            self._log_error(f"❌ 相机到世界坐标转换失败: {e}")
            return camera_point
    
    def _calculate_target_yaw(self, detection: DetectionResult) -> float:
        """
        计算目标YAW角度 - 基于最小外接矩形
        
        Args:
            detection: 检测结果
        
        Returns:
            目标YAW角度（度）
        """
        try:
            # 从特征中获取最小外接矩形信息
            shape_features = detection.features.get('shape', {})
            min_area_rect = shape_features.get('min_area_rect', {})
            
            if not min_area_rect:
                # 如果没有预计算的矩形，使用mask计算
                if detection.mask is not None:
                    return self._calculate_yaw_from_mask(detection.mask)
                else:
                    return self.last_yaw if self.last_yaw is not None else 0.0
            
            # 获取矩形参数
            size = min_area_rect.get('size', [0, 0])
            angle = min_area_rect.get('angle', 0)
            width, height = size
            
            # 计算YAW角度（基于静态抓取算法）
            if width > height:
                yaw_angle = -angle + 90
            else:
                yaw_angle = -angle
            
            # 归一化角度到 [-180, 180]
            yaw_angle = self._normalize_angle(yaw_angle)
            
            # 连续性优化
            if self.last_yaw is not None:
                current_yaw = self.last_yaw
                options = [yaw_angle, yaw_angle + 180, yaw_angle - 180]
                options = [self._normalize_angle(opt) for opt in options]
                best_yaw = min(options, key=lambda opt: abs(opt - current_yaw))
                yaw_angle = best_yaw
            
            self.last_yaw = yaw_angle
            
            self._log_debug(f"🔄 计算YAW: width={width:.1f}, height={height:.1f}, angle={angle:.1f}° → yaw={yaw_angle:.1f}°")
            
            return yaw_angle
            
        except Exception as e:
            self._log_error(f"❌ 计算目标YAW失败: {e}")
            return self.last_yaw if self.last_yaw is not None else 0.0
    
    def _calculate_yaw_from_mask(self, mask: np.ndarray) -> float:
        """
        从mask计算YAW角度
        
        Args:
            mask: 对象mask
        
        Returns:
            YAW角度（度）
        """
        try:
            # 找到轮廓
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                return self.last_yaw if self.last_yaw is not None else 0.0
            
            # 选择最大轮廓
            largest_contour = max(contours, key=cv2.contourArea)
            
            if len(largest_contour) < 5:
                return self.last_yaw if self.last_yaw is not None else 0.0
            
            # 计算最小外接矩形
            rect = cv2.minAreaRect(largest_contour)
            _, (width, height), angle = rect
            
            # 计算YAW角度
            if width > height:
                yaw_angle = -angle + 90
            else:
                yaw_angle = -angle
            
            return self._normalize_angle(yaw_angle)
            
        except Exception as e:
            self._log_error(f"❌ 从mask计算YAW失败: {e}")
            return self.last_yaw if self.last_yaw is not None else 0.0
    
    def _calculate_proportional_move(self, target_world_coords: Tuple[float, float, float],
                                   target_yaw: float, distance_xy: float, 
                                   yaw_error: float) -> TrackingCommand:
        """
        计算比例移动
        
        Args:
            target_world_coords: 目标世界坐标
            target_yaw: 目标YAW角度
            distance_xy: XY距离
            yaw_error: YAW误差
        
        Returns:
            追踪命令
        """
        try:
            target_x, target_y, target_z = target_world_coords
            current_x, current_y, current_z = self.current_arm_pose_list[:3]
            current_yaw = self.current_arm_pose_list[5]
            
            # 计算比例移动距离
            delta_x = (target_x - current_x) * self.proportional_factor
            delta_y = (target_y - current_y) * self.proportional_factor
            delta_yaw = yaw_error * self.proportional_factor  # 增量YAW调整
            
            # 计算新位置
            new_x = current_x + delta_x
            new_y = current_y + delta_y
            new_z = max(self.safe_height, self.min_z_height)  # 保持安全高度
            new_yaw = current_yaw + delta_yaw  # 基于当前角度的增量调整
            
            # 归一化YAW角度
            new_yaw = self._normalize_angle(new_yaw)
            
            # 工作空间检查
            if not self._is_in_workspace(new_x, new_y, new_z):
                self._log_warn(f"⚠️ 目标位置超出工作空间: ({new_x:.1f}, {new_y:.1f}, {new_z:.1f})")
                return TrackingCommand(
                    state=TrackingState.TRACKING,
                    mode=None,
                    target_pose={},
                    movement_type="proportional",
                    distance_mm=distance_xy,
                    yaw_adjustment=abs(yaw_error),
                    success=False
                )
            
            # 构建目标位姿
            target_pose = {
                'position': {'x': new_x, 'y': new_y, 'z': new_z},
                'orientation': {'roll': 180, 'pitch': 0, 'yaw': new_yaw}
            }
            
            # 记录运动
            self._record_motion(
                from_pose=self.current_arm_pose_list,
                to_pose=[new_x, new_y, new_z, 180, 0, new_yaw],
                command_type="proportional",
                target_position=(target_x, target_y),
                distance_to_target=distance_xy
            )
            
            self._log_info(f"🎯 比例移动: Δ=({delta_x:.1f},{delta_y:.1f}) → ({new_x:.1f},{new_y:.1f},{new_z:.1f}) yaw={new_yaw:.1f}°")
            
            return TrackingCommand(
                state=TrackingState.TRACKING,
                mode=None,
                target_pose=target_pose,
                movement_type="proportional",
                distance_mm=distance_xy,
                yaw_adjustment=abs(yaw_error),
                success=True
            )
            
        except Exception as e:
            self._log_error(f"❌ 计算比例移动失败: {e}")
            return TrackingCommand(
                state=TrackingState.TRACKING,
                mode=None,
                target_pose={},
                success=False
            )
    
    def _calculate_approach_move(self, target_world_coords: Tuple[float, float, float],
                               target_yaw: float, distance_xy: float, 
                               yaw_error: float) -> TrackingCommand:
        """
        计算逼近移动
        
        Args:
            target_world_coords: 目标世界坐标
            target_yaw: 目标YAW角度
            distance_xy: XY距离
            yaw_error: YAW误差
        
        Returns:
            追踪命令
        """
        try:
            target_x, target_y, target_z = target_world_coords
            
            # 逼近阶段：移动到目标正上方，使用增量YAW调整
            approach_height = max(target_z + 100, self.min_z_height + 50)  # 目标上方100mm
            
            # 计算YAW调整
            current_yaw = self.current_arm_pose_list[5]
            yaw_adjustment = yaw_error * 0.3  # 较小的调整因子
            new_yaw = current_yaw + yaw_adjustment
            new_yaw = self._normalize_angle(new_yaw)
            
            target_pose = {
                'position': {'x': target_x, 'y': target_y, 'z': approach_height},
                'orientation': {'roll': 180, 'pitch': 0, 'yaw': new_yaw}  # 使用调整后的yaw
            }
            
            # 工作空间检查
            if not self._is_in_workspace(target_x, target_y, approach_height):
                self._log_warn(f"⚠️ 逼近位置超出工作空间")
                return TrackingCommand(
                    state=TrackingState.APPROACHING,
                    mode=None,
                    target_pose={},
                    success=False
                )
            
            # 记录运动
            self._record_motion(
                from_pose=self.current_arm_pose_list,
                to_pose=[target_x, target_y, approach_height, 180, 0, target_yaw],
                command_type="approach",
                target_position=(target_x, target_y),
                distance_to_target=distance_xy
            )
            
            self._log_info(f"🎯 逼近移动: → ({target_x:.1f},{target_y:.1f},{approach_height:.1f}) yaw={target_yaw:.1f}°")
            
            return TrackingCommand(
                state=TrackingState.APPROACHING,
                mode=None,
                target_pose=target_pose,
                movement_type="approach",
                distance_mm=distance_xy,
                yaw_adjustment=abs(yaw_error),
                success=True
            )
            
        except Exception as e:
            self._log_error(f"❌ 计算逼近移动失败: {e}")
            return TrackingCommand(
                state=TrackingState.APPROACHING,
                mode=None,
                target_pose={},
                success=False
            )
    
    def _calculate_grasp_move(self, target_world_coords: Tuple[float, float, float],
                            target_yaw: float, detection: DetectionResult) -> TrackingCommand:
        """
        计算抓取移动
        
        Args:
            target_world_coords: 目标世界坐标
            target_yaw: 目标YAW角度
            detection: 检测结果
        
        Returns:
            追踪命令
        """
        try:
            target_x, target_y, target_z = target_world_coords
            
            # 获取对象高度
            height_info = detection.features.get('depth_info', {})
            object_height = height_info.get('height_mm', 30.0)
            
            # 计算抓取策略
            grasp_strategy = self._plan_grasp_strategy(object_height, target_yaw)
            
            # 计算抓取位置
            grasp_z = target_z + grasp_strategy['z_offset']
            grasp_pitch = grasp_strategy['pitch']
            
            # 位移补偿（基于pitch角度）
            compensated_x, compensated_y, compensated_z = self._calculate_pitch_compensation(
                target_x, target_y, grasp_z, grasp_pitch, target_yaw
            )
            
            target_pose = {
                'position': {'x': compensated_x, 'y': compensated_y, 'z': compensated_z},
                'orientation': {'roll': 180, 'pitch': grasp_pitch, 'yaw': target_yaw}
            }
            
            # 夹爪命令
            gripper_width = self._calculate_gripper_width(detection)
            gripper_command = {
                'action': 'close',
                'position': gripper_width
            }
            
            self._log_info(f"🤖 抓取移动: → ({compensated_x:.1f},{compensated_y:.1f},{compensated_z:.1f}) pitch={grasp_pitch:.1f}° width={gripper_width}")
            
            return TrackingCommand(
                state=TrackingState.GRASPING,
                mode=None,
                target_pose=target_pose,
                gripper_command=gripper_command,
                movement_type="grasp",
                distance_mm=0.0,
                yaw_adjustment=0.0,
                success=True
            )
            
        except Exception as e:
            self._log_error(f"❌ 计算抓取移动失败: {e}")
            return TrackingCommand(
                state=TrackingState.GRASPING,
                mode=None,
                target_pose={},
                success=False
            )
    
    def _plan_grasp_strategy(self, height_mm: float, yaw: float) -> Dict[str, float]:
        """
        规划抓取策略 - 基于静态抓取算法
        
        Args:
            height_mm: 对象高度
            yaw: YAW角度
        
        Returns:
            抓取策略
        """
        try:
            # 基于高度确定pitch和Z偏移
            if height_mm < 80:
                pitch = 0.0
                z_offset = 120
            elif height_mm < 120:
                pitch = -15.0
                z_offset = 0.5 * height_mm + 90
            elif height_mm < 160:
                pitch = -30.0
                z_offset = 0.5 * height_mm + 80
            else:
                pitch = -45.0
                z_offset = 0.5 * height_mm + 60
            
            return {
                'pitch': pitch,
                'yaw': yaw,
                'z_offset': z_offset,
                'height': height_mm
            }
            
        except Exception as e:
            self._log_error(f"❌ 规划抓取策略失败: {e}")
            return {'pitch': 0.0, 'yaw': 0.0, 'z_offset': 100.0, 'height': 30.0}
    
    def _calculate_pitch_compensation(self, target_x: float, target_y: float, target_z: float,
                                    pitch_deg: float, yaw_deg: float, 
                                    gripper_length: float = 120.0) -> Tuple[float, float, float]:
        """
        计算pitch角度补偿 - 基于静态抓取算法
        
        Args:
            target_x, target_y, target_z: 目标坐标
            pitch_deg: pitch角度（度）
            yaw_deg: yaw角度（度）
            gripper_length: 夹爪长度（毫米）
        
        Returns:
            补偿后的坐标 (x, y, z)
        """
        try:
            pitch_rad = math.radians(pitch_deg)
            yaw_rad = math.radians(yaw_deg)
            
            # 计算偏移
            offset_forward = gripper_length * math.sin(-pitch_rad)
            offset_down = gripper_length * (1 - math.cos(-pitch_rad))
            
            # 在XY平面上的投影
            offset_x = offset_forward * math.cos(yaw_rad)
            offset_y = offset_forward * math.sin(yaw_rad)
            offset_z = offset_down
            
            # 应用补偿
            compensated_x = target_x - offset_x
            compensated_y = target_y - offset_y
            compensated_z = target_z + offset_z
            
            self._log_debug(f"🔧 Pitch补偿: pitch={pitch_deg}°, yaw={yaw_deg}°")
            self._log_debug(f"   偏移: dx={offset_x:.1f}, dy={offset_y:.1f}, dz={offset_z:.1f}")
            self._log_debug(f"   原始: ({target_x:.1f},{target_y:.1f},{target_z:.1f})")
            self._log_debug(f"   补偿: ({compensated_x:.1f},{compensated_y:.1f},{compensated_z:.1f})")
            
            return (compensated_x, compensated_y, compensated_z)
            
        except Exception as e:
            self._log_error(f"❌ Pitch补偿计算失败: {e}")
            return (target_x, target_y, target_z)
    
    def _calculate_gripper_width(self, detection: DetectionResult) -> int:
        """
        计算夹爪宽度 - 基于对象尺寸
        
        Args:
            detection: 检测结果
        
        Returns:
            夹爪宽度（0-850）
        """
        try:
            # 从shape特征获取最小外接矩形
            shape_features = detection.features.get('shape', {})
            min_area_rect = shape_features.get('min_area_rect', {})
            
            if min_area_rect:
                size = min_area_rect.get('size', [0, 0])
                width, height = size
                
                # 选择较短的一边作为抓取宽度
                short_side = min(width, height)
                
                # 转换为夹爪宽度（添加安全边距）
                gripper_width = max(150, min(500, int(short_side * 2 - 10)))
            else:
                # 默认宽度
                gripper_width = 300
            
            self._log_debug(f"🤏 计算夹爪宽度: {gripper_width}")
            return gripper_width
            
        except Exception as e:
            self._log_error(f"❌ 计算夹爪宽度失败: {e}")
            return 300
    
    def _is_in_workspace(self, x: float, y: float, z: float) -> bool:
        """检查位置是否在工作空间内"""
        try:
            x_ok = self.workspace_limits['x'][0] <= x <= self.workspace_limits['x'][1]
            y_ok = self.workspace_limits['y'][0] <= y <= self.workspace_limits['y'][1]
            z_ok = self.workspace_limits['z'][0] <= z <= self.workspace_limits['z'][1]
            
            return x_ok and y_ok and z_ok
            
        except Exception as e:
            self._log_error(f"❌ 工作空间检查失败: {e}")
            return False
    
    def _normalize_angle(self, angle: float) -> float:
        """归一化角度到 [-180, 180]"""
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle
    
    def _quat_to_euler(self, qx: float, qy: float, qz: float, qw: float) -> Tuple[float, float, float]:
        """四元数转欧拉角（度）"""
        try:
            # Roll (x-axis rotation)
            sinr_cosp = 2 * (qw * qx + qy * qz)
            cosr_cosp = 1 - 2 * (qx * qx + qy * qy)
            roll = math.atan2(sinr_cosp, cosr_cosp)
            
            # Pitch (y-axis rotation)
            sinp = 2 * (qw * qy - qz * qx)
            if abs(sinp) >= 1:
                pitch = math.copysign(math.pi / 2, sinp)
            else:
                pitch = math.asin(sinp)
            
            # Yaw (z-axis rotation)
            siny_cosp = 2 * (qw * qz + qx * qy)
            cosy_cosp = 1 - 2 * (qy * qy + qz * qz)
            yaw = math.atan2(siny_cosp, cosy_cosp)
            
            return (math.degrees(roll), math.degrees(pitch), math.degrees(yaw))
            
        except Exception as e:
            self._log_error(f"❌ 四元数转换失败: {e}")
            return (0.0, 0.0, 0.0)
    
    def _record_motion(self, from_pose: List[float], to_pose: List[float], 
                      command_type: str, target_position: Tuple[float, float],
                      distance_to_target: float):
        """记录运动历史"""
        try:
            motion_record = MotionRecord(
                timestamp=time.time(),
                from_pose=from_pose.copy(),
                to_pose=to_pose.copy(),
                command_type=command_type,
                success=True,  # 实际执行时更新
                target_position=target_position,
                distance_to_target=distance_to_target,
                state=TrackingState.TRACKING,  # 根据实际状态设置
                mode=None
            )
            
            self.motion_history.append(motion_record)
            
            # 保持历史长度
            max_history = 100
            if len(self.motion_history) > max_history:
                self.motion_history = self.motion_history[-max_history:]
                
        except Exception as e:
            self._log_error(f"❌ 记录运动历史失败: {e}")
    
    def get_last_successful_pose(self) -> Optional[List[float]]:
        """获取最后成功的位姿"""
        return self.last_successful_pose.copy() if self.last_successful_pose else None
    
    def update_motion_success(self, success: bool):
        """更新最后一次运动的成功状态"""
        try:
            if self.motion_history:
                self.motion_history[-1].success = success
                
                if success:
                    # 更新最后成功位姿
                    self.last_successful_pose = self.motion_history[-1].to_pose.copy()
                    
        except Exception as e:
            self._log_error(f"❌ 更新运动成功状态失败: {e}")
    
    def get_motion_history(self, count: int = 10) -> List[MotionRecord]:
        """获取运动历史"""
        try:
            return self.motion_history[-count:] if self.motion_history else []
        except Exception as e:
            self._log_error(f"❌ 获取运动历史失败: {e}")
            return []
    
    def check_target_reached(self, detection: DetectionResult) -> Tuple[bool, float, float]:
        """
        检查是否到达目标
        
        Args:
            detection: 检测结果
        
        Returns:
            (是否到达, XY距离, YAW误差)
        """
        try:
            if not self.current_arm_pose:
                return False, float('inf'), float('inf')
            
            # 计算目标世界坐标
            target_world_coords = self._calculate_world_coordinates(detection)
            if not target_world_coords:
                return False, float('inf'), float('inf')
            
            target_x, target_y, target_z = target_world_coords
            current_x, current_y = self.current_arm_pose_list[:2]
            
            # 计算XY距离
            distance_xy = math.sqrt((target_x - current_x)**2 + (target_y - current_y)**2)
            
            # 计算YAW误差
            target_yaw = self._calculate_target_yaw(detection)
            current_yaw = self.current_arm_pose_list[5]
            yaw_error = abs(self._normalize_angle(target_yaw - current_yaw))
            
            # 检查是否到达
            xy_reached = distance_xy <= self.target_tolerance_xy
            yaw_reached = yaw_error <= self.target_tolerance_yaw
            reached = xy_reached and yaw_reached
            
            return reached, distance_xy, yaw_error
            
        except Exception as e:
            self._log_error(f"❌ 检查目标到达失败: {e}")
            return False, float('inf'), float('inf')
    
    def get_control_status(self) -> Dict[str, Any]:
        """获取控制状态"""
        try:
            status = {
                'current_pose': self.current_arm_pose,
                'current_pose_list': self.current_arm_pose_list if self.current_arm_pose_list else None,
                'last_successful_pose': self.last_successful_pose,
                'motion_history_count': len(self.motion_history),
                'last_yaw': self.last_yaw,
                'proportional_factor': self.proportional_factor,
                'target_tolerance_xy': self.target_tolerance_xy,
                'target_tolerance_yaw': self.target_tolerance_yaw,
                'workspace_limits': self.workspace_limits,
                'safe_height': self.safe_height,
                'min_z_height': self.min_z_height
            }
            
            # 添加最近的运动记录
            if self.motion_history:
                last_motion = self.motion_history[-1]
                status['last_motion'] = {
                    'command_type': last_motion.command_type,
                    'success': last_motion.success,
                    'distance_to_target': last_motion.distance_to_target,
                    'timestamp': last_motion.timestamp
                }
            
            return status
            
        except Exception as e:
            self._log_error(f"❌ 获取控制状态失败: {e}")
            return {}
    
    def reset(self):
        """重置控制器状态"""
        try:
            self.motion_history.clear()
            self.last_successful_pose = None
            self.last_yaw = None
            self._log_info("🔄 位姿控制器已重置")
            
        except Exception as e:
            self._log_error(f"❌ 重置控制器失败: {e}")
    
    def save_motion_data(self, output_path: str):
        """保存运动数据"""
        try:
            import json
            import os
            
            motion_data = {
                'motion_history': [],
                'control_parameters': {
                    'proportional_factor': self.proportional_factor,
                    'target_tolerance_xy': self.target_tolerance_xy,
                    'target_tolerance_yaw': self.target_tolerance_yaw,
                    'workspace_limits': self.workspace_limits
                },
                'timestamp': time.time()
            }
            
            # 转换运动历史为可序列化格式
            for record in self.motion_history:
                motion_data['motion_history'].append({
                    'timestamp': record.timestamp,
                    'from_pose': record.from_pose,
                    'to_pose': record.to_pose,
                    'command_type': record.command_type,
                    'success': record.success,
                    'target_position': record.target_position,
                    'distance_to_target': record.distance_to_target,
                    'state': record.state.value if record.state else 'unknown',
                    'mode': record.mode.value if record.mode else 'unknown'
                })
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(motion_data, f, indent=2, ensure_ascii=False)
            
            self._log_info(f"💾 运动数据已保存: {output_path}")
            
        except Exception as e:
            self._log_error(f"❌ 保存运动数据失败: {e}")
    
    def print_status_summary(self):
        """打印状态摘要"""
        status = self.get_control_status()
        
        print("\n" + "="*40)
        print("🎮 POSE CONTROLLER STATUS")
        print("="*40)
        print(f"📍 当前位姿: {status.get('current_pose_list', 'None')}")
        print(f"✅ 最后成功位姿: {status.get('last_successful_pose', 'None')}")
        print(f"📊 运动历史: {status.get('motion_history_count', 0)} 条记录")
        print(f"🔄 比例因子: {status.get('proportional_factor', 0)}")
        print(f"📏 XY容差: {status.get('target_tolerance_xy', 0)}mm")
        print(f"🔄 YAW容差: {status.get('target_tolerance_yaw', 0)}°")
        print(f"⚡ 安全高度: {status.get('safe_height', 0)}mm")
        print(f"🔧 最后YAW: {status.get('last_yaw', 'None')}°")
        
        if 'last_motion' in status:
            last_motion = status['last_motion']
            print(f"🚀 最后运动: {last_motion['command_type']} ({'成功' if last_motion['success'] else '失败'})")
            print(f"📐 目标距离: {last_motion['distance_to_target']:.1f}mm")
        
        print("="*40)
    
    # ============ 日志方法 ============
    
    def _log_info(self, message: str):
        """记录信息日志"""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[POSE_CONTROLLER] {message}")
    
    def _log_debug(self, message: str):
        """记录调试日志"""
        if self.logger:
            self.logger.debug(message)
        else:
            print(f"[POSE_CONTROLLER] DEBUG: {message}")
    
    def _log_warn(self, message: str):
        """记录警告日志"""
        if self.logger:
            self.logger.warn(message)
        else:
            print(f"[POSE_CONTROLLER] WARNING: {message}")
    
    def _log_error(self, message: str):
        """记录错误日志"""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"[POSE_CONTROLLER] ERROR: {message}")


if __name__ == "__main__":
    # 测试位姿控制器
    from ..utils.config import create_tracking_config
    
    config = create_tracking_config()
    controller = PoseController(config)
    
    print("🧪 测试位姿控制器...")
    
    # 模拟机械臂位姿
    test_pose = {
        'position': {'x': 300.0, 'y': 0.0, 'z': 400.0},
        'orientation': {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 1.0}
    }
    controller.update_current_pose(test_pose)
    
    # 创建测试检测结果
    test_detection = DetectionResult(
        object_id="test_lemon_0",
        class_id=4,
        class_name="lemon",
        bounding_box=[600, 300, 700, 400],
        mask=np.zeros((100, 100), dtype=np.uint8),
        centroid_2d=(650, 350),
        centroid_3d=(0.1, 0.0, 0.3),  # 相机坐标系（米）
        confidence=0.9,
        features={
            'shape': {
                'min_area_rect': {
                    'center': [650, 350],
                    'size': [60, 40],
                    'angle': 15
                }
            },
            'depth_info': {
                'height_mm': 35.0
            }
        }
    )
    
    # 测试计算目标位姿
    command = controller.calculate_target_pose(test_detection, TrackingState.TRACKING)
    if command:
        print(f"计算成功: {command.movement_type}, 距离: {command.distance_mm:.1f}mm")
    else:
        print("计算失败")
    
    # 打印状态摘要
    controller.print_status_summary()