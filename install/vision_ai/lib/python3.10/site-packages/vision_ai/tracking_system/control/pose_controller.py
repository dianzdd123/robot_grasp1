#!/usr/bin/env python3

import numpy as np
import math
from typing import Dict, List, Tuple, Optional
from scipy.spatial.transform import Rotation as R

class PoseController:
    """位姿控制器 - 处理机械臂位姿计算和轨迹规划"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        
        # 控制参数
        self.proportional_factor = config.tracking.proportional_factor
        self.movement_speed = config.tracking.movement_speed
        
        # 当前状态
        self.current_pose = None
        self.target_pose = None
        self.control_history = []
        
        self.logger.info("🎮 PoseController initialized")
    
    def update_current_pose(self, pose: Dict):
        """更新当前机械臂位姿"""
        self.current_pose = pose.copy()
    
    def calculate_target_pose(self, detection: Dict, phase: str) -> Dict:
        """计算目标位姿"""
        # 获取目标世界坐标
        spatial_features = detection.get('features', {}).get('spatial', {})
        world_coords = spatial_features.get('world_coordinates', (0, 0, 250))
        
        # 获取物体特征用于姿态计算
        shape_features = detection.get('features', {}).get('shape', {})
        depth_info = detection.get('features', {}).get('depth_info', {})
        
        # 计算基础位置
        target_position = self._calculate_target_position(world_coords, phase)
        
        # 计算目标姿态
        target_orientation = self._calculate_target_orientation(
            shape_features, depth_info, phase
        )
        
        # 应用相位特定的调整
        adjusted_pose = self._apply_phase_adjustments(
            target_position, target_orientation, phase
        )
        
        # 安全性检查
        safe_pose = self._ensure_pose_safety(adjusted_pose)
        
        self.target_pose = safe_pose
        return safe_pose
    
    def _calculate_target_position(self, world_coords: Tuple, phase: str) -> Dict:
        """计算目标位置"""
        x, y, z = world_coords
        
        # 根据阶段调整高度偏移
        height_offsets = {
            'LONG_RANGE': 100,
            'MEDIUM_RANGE': 50, 
            'SHORT_RANGE': 20,
            'GRASP_RANGE': 0
        }
        
        z_offset = height_offsets.get(phase, 50)
        target_z = z + z_offset
        
        # 应用比例控制
        if self.current_pose:
            current_pos = self.current_pose.get('position', {})
            
            # 兼容不同的位置格式
            if isinstance(current_pos, dict):
                current_x = current_pos.get('x', x)
                current_y = current_pos.get('y', y)
                current_z = current_pos.get('z', target_z)
            elif isinstance(current_pos, (list, tuple)) and len(current_pos) >= 3:
                current_x, current_y, current_z = current_pos[0], current_pos[1], current_pos[2]
            else:
                current_x, current_y, current_z = x, y, target_z
            
            # 计算位置误差
            error_x = x - current_x
            error_y = y - current_y
            error_z = target_z - current_z
            
            # 应用比例控制和速度限制
            speed_factor = self.movement_speed.get(phase, 0.5)
            control_factor = self.proportional_factor * speed_factor
            
            adjusted_x = current_x + error_x * control_factor
            adjusted_y = current_y + error_y * control_factor
            adjusted_z = current_z + error_z * control_factor
            
            return {
                'x': adjusted_x,
                'y': adjusted_y,
                'z': adjusted_z
            }
        
        return {'x': x, 'y': y, 'z': target_z}
    
    def _calculate_target_orientation(self, shape_features: Dict, depth_info: Dict, phase: str) -> Dict:
        """计算目标姿态"""
        # 基础姿态：朝下
        roll = 179
        pitch = 0
        yaw = 0
        
        # 根据物体高度计算pitch
        height_mm = depth_info.get('height_mm', 30.0)
        pitch = self.config.get_gripper_pitch(height_mm)
        
        # ⭐ 这里不再计算yaw，因为tracking_core.py已经计算了
        # yaw将由tracking_core传入
        
        # 根据阶段微调姿态
        if phase == 'GRASP_RANGE':
            # 抓取阶段：更精确的姿态
            pass
        elif phase == 'SHORT_RANGE':
            # 接近阶段：轻微调整pitch以便观察
            pitch += 5
        
        return {
            'roll': roll,
            'pitch': pitch,
            'yaw': yaw  # 默认值，将被tracking_core覆盖
        }
    
    def _apply_phase_adjustments(self, position: Dict, orientation: Dict, phase: str) -> Dict:
        """应用相位特定的调整"""
        adjusted_pose = {
            'position': position.copy(),
            'orientation': orientation.copy()
        }
        
        # 根据阶段调整控制策略
        if phase == 'LONG_RANGE':
            # 远距离：保守移动，较高位置
            adjusted_pose['position']['z'] = max(adjusted_pose['position']['z'], 350)
            
        elif phase == 'MEDIUM_RANGE':
            # 中距离：开始精确定位
            adjusted_pose['position']['z'] = max(adjusted_pose['position']['z'], 270)
            
        elif phase == 'SHORT_RANGE':
            # 短距离：悬停准备
            adjusted_pose['position']['z'] = max(adjusted_pose['position']['z'], 230)
            
        elif phase == 'GRASP_RANGE':
            # 抓取距离：精确下降
            pass
        
        return adjusted_pose
    
    def _ensure_pose_safety(self, pose: Dict) -> Dict:
        """确保位姿安全性"""
        safe_pose = pose.copy()
        
        # 位置安全检查
        position = safe_pose['position']
        
        # 工作空间限制
        x_min, x_max = self.config.workspace.x_limits
        y_min, y_max = self.config.workspace.y_limits
        z_min, z_max = self.config.workspace.z_limits
        
        position['x'] = max(x_min, min(x_max, position['x']))
        position['y'] = max(y_min, min(y_max, position['y']))
        position['z'] = max(z_min, min(z_max, position['z']))
        
        # 最小安全高度
        min_height = self.config.workspace.min_height
        position['z'] = max(min_height, position['z'])
        
        # 姿态安全检查
        orientation = safe_pose['orientation']
        
        # 限制姿态角度范围
        orientation['roll'] = max(160, min(200, orientation['roll']))
        orientation['pitch'] = max(-45, min(45, orientation['pitch']))
        orientation['yaw'] = max(-180, min(180, orientation['yaw']))
        
        return safe_pose
    
    def generate_trajectory(self, start_pose: Dict, end_pose: Dict, steps: int = 10) -> List[Dict]:
        """生成轨迹点序列"""
        trajectory = []
        
        start_pos = start_pose['position']
        end_pos = end_pose['position']
        start_ori = start_pose['orientation']
        end_ori = end_pose['orientation']
        
        for i in range(steps + 1):
            t = i / steps
            
            # 位置插值
            interp_pos = {
                'x': start_pos['x'] + t * (end_pos['x'] - start_pos['x']),
                'y': start_pos['y'] + t * (end_pos['y'] - start_pos['y']),
                'z': start_pos['z'] + t * (end_pos['z'] - start_pos['z'])
            }
            
            # 姿态插值（球面线性插值）
            interp_ori = self._interpolate_orientation(start_ori, end_ori, t)
            
            trajectory_point = {
                'position': interp_pos,
                'orientation': interp_ori,
                'timestamp': i
            }
            
            trajectory.append(trajectory_point)
        
        return trajectory
    
    def _interpolate_orientation(self, start_ori: Dict, end_ori: Dict, t: float) -> Dict:
        """姿态球面线性插值"""
        # 转换为旋转矩阵
        start_rot = R.from_euler('xyz', [
            math.radians(start_ori['roll']),
            math.radians(start_ori['pitch']),
            math.radians(start_ori['yaw'])
        ])
        
        end_rot = R.from_euler('xyz', [
            math.radians(end_ori['roll']),
            math.radians(end_ori['pitch']),
            math.radians(end_ori['yaw'])
        ])
        
        # 球面线性插值
        interp_rot = start_rot.slerp(end_rot, t)
        
        # 转换回欧拉角
        euler_angles = interp_rot.as_euler('xyz')
        
        return {
            'roll': math.degrees(euler_angles[0]),
            'pitch': math.degrees(euler_angles[1]),
            'yaw': math.degrees(euler_angles[2])
        }
    
    def check_position_reached(self, target_pose: Dict, current_pose: Dict, phase: str) -> bool:
        """检查是否到达目标位置"""
        if not current_pose or not target_pose:
            return False
        
        target_pos = target_pose['position']
        current_pos = current_pose.get('position', [0, 0, 0])
        
        # 计算位置误差
        error_x = abs(target_pos['x'] - current_pos[0])
        error_y = abs(target_pos['y'] - current_pos[1])
        error_z = abs(target_pos['z'] - current_pos[2])
        
        # 获取相位容差
        tolerance = self.config.tracking.alignment_thresholds['xy_tolerance']
        
        # 检查是否在容差范围内
        position_reached = (error_x <= tolerance and 
                          error_y <= tolerance and 
                          error_z <= tolerance)
        
        if position_reached:
            self.logger.debug(f"✅ Position reached for {phase}: errors=({error_x:.1f}, {error_y:.1f}, {error_z:.1f})")
        
        return position_reached
    
    def calculate_approach_vector(self, target_position: Dict) -> np.ndarray:
        """计算接近向量"""
        if not self.current_pose:
            return np.array([0, 0, -1])  # 默认向下
        
        current_pos = np.array([
            self.current_pose['position'][0],
            self.current_pose['position'][1], 
            self.current_pose['position'][2]
        ])
        
        target_pos = np.array([
            target_position['x'],
            target_position['y'],
            target_position['z']
        ])
        
        # 计算方向向量
        direction = target_pos - current_pos
        
        # 归一化
        if np.linalg.norm(direction) > 0:
            direction = direction / np.linalg.norm(direction)
        
        return direction
    
    def estimate_movement_time(self, start_pose: Dict, end_pose: Dict, phase: str) -> float:
        """估算移动时间"""
        start_pos = np.array([start_pose['position']['x'], start_pose['position']['y'], start_pose['position']['z']])
        end_pos = np.array([end_pose['position']['x'], end_pose['position']['y'], end_pose['position']['z']])
        
        # 计算距离
        distance = np.linalg.norm(end_pos - start_pos)
        
        # 使用统一的移动速度
        speed = 50  # mm/s
        estimated_time = distance / speed
        
        return max(0.5, estimated_time)  # 最小0.5秒
    
    def get_control_status(self) -> Dict:
        """获取控制状态"""
        try:
            status = {
                'current_pose': self.current_pose,
                'target_pose': self.target_pose,
                'control_active': self.target_pose is not None,
                'history_length': len(self.control_history)
            }
            
            if self.current_pose and self.target_pose:
                # 安全地获取当前位置
                current_pos = self.current_pose.get('position', {})
                target_pos = self.target_pose.get('position', {})
                
                # 兼容不同格式
                if isinstance(current_pos, dict):
                    curr_x = current_pos.get('x', 0)
                    curr_y = current_pos.get('y', 0)
                    curr_z = current_pos.get('z', 0)
                elif isinstance(current_pos, (list, tuple)) and len(current_pos) >= 3:
                    curr_x, curr_y, curr_z = current_pos[0], current_pos[1], current_pos[2]
                else:
                    curr_x = curr_y = curr_z = 0
                
                if isinstance(target_pos, dict):
                    targ_x = target_pos.get('x', 0)
                    targ_y = target_pos.get('y', 0)
                    targ_z = target_pos.get('z', 0)
                else:
                    targ_x = targ_y = targ_z = 0
                
                # 计算控制误差
                error = {
                    'x': targ_x - curr_x,
                    'y': targ_y - curr_y,
                    'z': targ_z - curr_z
                }
                
                status['position_error'] = error
                status['total_error'] = math.sqrt(error['x']**2 + error['y']**2 + error['z']**2)
            
            return status
            
        except Exception as e:
            # 返回简化状态而不是抛出异常
            return {
                'error': str(e),
                'current_pose': None,
                'target_pose': None,
                'control_active': False,
                'history_length': 0
            }
    
    def reset(self):
        """重置控制器"""
        self.target_pose = None
        self.control_history.clear()
        self.logger.info("🔄 PoseController reset")