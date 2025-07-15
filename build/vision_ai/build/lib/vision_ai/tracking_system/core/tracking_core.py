#!/usr/bin/env python3

import json
import threading
import time
import os
import math
from typing import Dict, List, Optional, Tuple
import numpy as np
from enum import Enum

class TrackingState(Enum):
    IDLE = "IDLE"
    SEARCHING = "SEARCHING" 
    TRACKING = "TRACKING"
    APPROACHING = "APPROACHING"
    GRASPING = "GRASPING"
    COMPLETED = "COMPLETED"
    RECOVERING = "RECOVERING"

class TrackingCore:
    """追踪系统核心逻辑"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        
        # 状态管理
        self.current_state = TrackingState.IDLE
        self.target_object_id = None
        self.target_features = None
        
        # 追踪数据
        self.current_detection = None
        self.last_known_position = None
        self.lost_frame_count = 0
        self.tracking_history = []
        
        # 线程安全
        self.lock = threading.Lock()
        
        # 性能监控
        self.tracking_start_time = None
        self.phase_start_time = None
        
        self.logger.info("🎯 TrackingCore initialized")
    
    def load_target_selection(self) -> bool:
        """加载目标选择"""
        try:
            selection_file = self.config.paths['tracking_selection']
            
            if not os.path.exists(selection_file):
                self.logger.error(f"Selection file not found: {selection_file}")
                return False
            
            with open(selection_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析选择内容，提取object_id
            lines = content.strip().split('\n')
            for line in lines:
                if '(ID:' in line:
                    # 提取ID: redpepper_1)
                    start = line.find('(ID: ') + 5
                    end = line.find(')', start)
                    if start > 4 and end > start:
                        self.target_object_id = line[start:end]
                        break
            
            if not self.target_object_id:
                self.logger.error("Failed to extract target object ID")
                return False
            
            self.logger.info(f"✅ Target selected: {self.target_object_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load target selection: {e}")
            return False
    
    def start_tracking(self) -> bool:
        """启动追踪"""
        with self.lock:
            if self.current_state != TrackingState.IDLE:
                self.logger.warn(f"Cannot start tracking, current state: {self.current_state}")
                return False
            
            if not self.load_target_selection():
                return False
            
            self.current_state = TrackingState.SEARCHING
            self.tracking_start_time = time.time()
            self.phase_start_time = time.time()
            self.lost_frame_count = 0
            self.tracking_history.clear()
            
            self.logger.info(f"🚀 Tracking started for target: {self.target_object_id}")
            return True
    
    def stop_tracking(self) -> bool:
        """停止追踪"""
        with self.lock:
            if self.current_state == TrackingState.IDLE:
                return True
            
            self.current_state = TrackingState.IDLE
            self.target_object_id = None
            self.target_features = None
            self.current_detection = None
            self.last_known_position = None
            
            self.logger.info("⏹️ Tracking stopped")
            return True
    
    def process_detection_result(self, detection_data: Dict) -> Optional[Dict]:
        """处理检测结果"""
        with self.lock:
            if self.current_state == TrackingState.IDLE:
                return None
            
            # 查找目标对象
            target_detection = self._find_target_in_detections(detection_data)
            
            if target_detection:
                self._handle_target_found(target_detection)
                return self._generate_control_command(target_detection)
            else:
                self._handle_target_lost()
                return self._handle_recovery()
    
    def _find_target_in_detections(self, detection_data: Dict) -> Optional[Dict]:
        """在检测结果中查找目标对象"""
        objects = detection_data.get('objects', [])
        
        for obj in objects:
            if obj.get('object_id') == self.target_object_id:
                # 进行ID匹配验证
                if self._verify_object_identity(obj):
                    return obj
        
        return None
    
    def _verify_object_identity(self, detection: Dict) -> bool:
        """验证对象身份匹配"""
        if not self.target_features:
            # 第一次检测，保存特征作为参考
            self.target_features = self._extract_tracking_features(detection)
            self.logger.info(f"📝 Saved reference features for {self.target_object_id}")
            return True
        
        # 计算特征相似度
        similarity_score = self._calculate_feature_similarity(
            detection, self.target_features
        )
        
        threshold = 0.6  # 相似度阈值
        is_match = similarity_score >= threshold
        
        if is_match:
            self.logger.debug(f"✅ ID verified: {similarity_score:.3f}")
        else:
            self.logger.warn(f"❌ ID mismatch: {similarity_score:.3f}")
        
        return is_match
    
    def _extract_tracking_features(self, detection: Dict) -> Dict:
        """提取用于追踪的关键特征"""
        features = detection.get('features', {})
        
        tracking_features = {
            'color_histogram': features.get('color', {}).get('histogram', []),
            'hu_moments': features.get('shape', {}).get('hu_moments', [])[:3],  # 只用前3个
            'area': features.get('shape', {}).get('area', 0),
            'aspect_ratio': features.get('shape', {}).get('aspect_ratio', 1.0),
            'centroid': features.get('spatial', {}).get('centroid_2d', (0, 0))
        }
        
        return tracking_features
    
    def _calculate_feature_similarity(self, detection: Dict, reference: Dict) -> float:
        """计算特征相似度"""
        weights = self.config.tracking.feature_weights
        total_score = 0.0
        
        # 颜色直方图相似度
        if reference.get('color_histogram') and detection.get('features', {}).get('color', {}).get('histogram'):
            hist_similarity = self._compare_histograms(
                detection['features']['color']['histogram'],
                reference['color_histogram']
            )
            total_score += weights['color_hist'] * hist_similarity
        
        # 形状特征相似度
        if reference.get('hu_moments') and detection.get('features', {}).get('shape', {}).get('hu_moments'):
            shape_similarity = self._compare_hu_moments(
                detection['features']['shape']['hu_moments'][:3],
                reference['hu_moments']
            )
            total_score += weights['shape_moments'] * shape_similarity
        
        # 位置连续性
        if reference.get('centroid') and detection.get('features', {}).get('spatial', {}).get('centroid_2d'):
            position_similarity = self._compare_positions(
                detection['features']['spatial']['centroid_2d'],
                reference['centroid']
            )
            total_score += weights['position_continuity'] * position_similarity
        
        return total_score
    
    def _compare_histograms(self, hist1: List, hist2: List) -> float:
        """比较颜色直方图（Chi-square距离）"""
        if not hist1 or not hist2 or len(hist1) != len(hist2):
            return 0.0
        
        h1 = np.array(hist1)
        h2 = np.array(hist2)
        
        # 归一化
        h1 = h1 / (np.sum(h1) + 1e-6)
        h2 = h2 / (np.sum(h2) + 1e-6)
        
        # Chi-square距离
        chi_square = np.sum((h1 - h2) ** 2 / (h1 + h2 + 1e-6))
        
        # 转换为相似度 (0-1)
        similarity = max(0, 1 - chi_square / 2)
        return similarity
    
    def _compare_hu_moments(self, moments1: List, moments2: List) -> float:
        """比较Hu矩特征"""
        if not moments1 or not moments2 or len(moments1) != len(moments2):
            return 0.0
        
        m1 = np.array(moments1)
        m2 = np.array(moments2)
        
        # 计算欧氏距离并转换为相似度
        distance = np.linalg.norm(m1 - m2)
        similarity = max(0, 1 - distance / 10)  # 缩放因子
        return similarity
    
    def _compare_positions(self, pos1: Tuple, pos2: Tuple) -> float:
        """比较位置连续性"""
        if not pos1 or not pos2:
            return 0.0
        
        distance = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
        threshold = self.config.tracking.position_continuity_threshold
        
        similarity = max(0, 1 - distance / threshold)
        return similarity
    
    def _handle_target_found(self, detection: Dict):
        """处理目标找到"""
        self.current_detection = detection
        self.lost_frame_count = 0
        
        # 更新追踪历史
        self.tracking_history.append({
            'timestamp': time.time(),
            'detection': detection,
            'state': self.current_state.value
        })
        
        # 保持历史记录在合理范围内
        if len(self.tracking_history) > 100:
            self.tracking_history = self.tracking_history[-50:]
        
        # 更新参考特征（缓慢适应）
        if self.target_features:
            self._update_reference_features(detection)
        
        # 状态转换
        if self.current_state == TrackingState.SEARCHING:
            self.current_state = TrackingState.TRACKING
            self.phase_start_time = time.time()
            self.logger.info("🎯 Target acquired, switching to TRACKING")
    
    def _handle_target_lost(self):
        """处理目标丢失"""
        self.lost_frame_count += 1
        
        if self.lost_frame_count >= self.config.tracking.lost_frame_threshold:
            self.logger.warn(f"❌ Target lost for {self.lost_frame_count} frames")
            
            if self.current_state not in [TrackingState.RECOVERING, TrackingState.IDLE]:
                self.current_state = TrackingState.RECOVERING
                self.phase_start_time = time.time()
    
    def _update_reference_features(self, detection: Dict):
        """缓慢更新参考特征（适应变化）"""
        alpha = 0.1  # 学习率
        
        current_features = self._extract_tracking_features(detection)
        
        # 更新直方图
        if (current_features.get('color_histogram') and 
            self.target_features.get('color_histogram')):
            ref_hist = np.array(self.target_features['color_histogram'])
            cur_hist = np.array(current_features['color_histogram'])
            
            if len(ref_hist) == len(cur_hist):
                updated_hist = (1 - alpha) * ref_hist + alpha * cur_hist
                self.target_features['color_histogram'] = updated_hist.tolist()
        
        # 更新质心位置
        if current_features.get('centroid'):
            self.target_features['centroid'] = current_features['centroid']
    
    def _generate_control_command(self, detection: Dict) -> Dict:
        """生成控制命令"""
        spatial_features = detection.get('features', {}).get('spatial', {})
        world_coords = spatial_features.get('world_coordinates', (0, 0, 0))
        
        # 计算到相机的距离
        distance_mm = spatial_features.get('distance_to_camera', 1.0) * 1000
        
        # 确定当前阶段
        current_phase = self.config.get_phase_by_distance(distance_mm)
        
        # 状态转换
        if current_phase == 'GRASP_RANGE' and self.current_state == TrackingState.TRACKING:
            self.current_state = TrackingState.APPROACHING
            self.phase_start_time = time.time()
            self.logger.info("🤏 Entering GRASP_RANGE, switching to APPROACHING")
        
        # 生成位姿命令
        pose_command = self._calculate_target_pose(detection, current_phase)
        
        # 生成夹爪命令
        gripper_command = self._calculate_gripper_command(detection, current_phase)
        
        command = {
            'pose': pose_command,
            'gripper': gripper_command,
            'phase': current_phase,
            'distance_mm': distance_mm,
            'state': self.current_state.value
        }
        
        self.logger.debug(f"📋 Control command: {current_phase}, dist={distance_mm:.1f}mm")
        return command
    
    def _calculate_target_pose(self, detection: Dict, phase: str) -> Dict:
        """计算目标位姿"""
        spatial_features = detection.get('features', {}).get('spatial', {})
        world_coords = spatial_features.get('world_coordinates', (0, 0, 0))
        
        # 基础位置
        target_x, target_y, target_z = world_coords
        
        # 高度信息用于计算pitch
        depth_info = detection.get('features', {}).get('depth_info', {})
        height_mm = depth_info.get('height_mm', 30.0)
        
        # ⭐⭐⭐ 使用您的yaw计算方法 ⭐⭐⭐
        yaw = self._calculate_optimal_yaw(detection)
        
        # 计算pitch角（基于物体高度）
        pitch = self.config.get_gripper_pitch(height_mm)
        
        # 根据阶段调整位置
        if phase == 'LONG_RANGE':
            target_z += 100  # 保持较高高度
        elif phase == 'MEDIUM_RANGE':
            target_z += 50
        elif phase == 'SHORT_RANGE':
            target_z += 20
        # GRASP_RANGE使用原始高度
        
        return {
            'position': {
                'x': target_x,
                'y': target_y, 
                'z': target_z
            },
            'orientation': {
                'roll': 179,  # 固定朝下
                'pitch': pitch,
                'yaw': yaw
            }
        }
    
    def _calculate_optimal_yaw(self, detection: Dict) -> float:
        """⭐⭐⭐ 使用您的yaw计算方法 ⭐⭐⭐"""
        try:
            import cv2
            
            mask = detection.get('mask')
            
            # 检查多种mask格式
            if mask is None:
                # 尝试从features中获取mask
                features = detection.get('features', {})
                mask = features.get('mask')
                
            if mask is None:
                # 尝试从shape特征中获取orientation作为备选
                shape_features = detection.get('features', {}).get('shape', {})
                orientation = shape_features.get('orientation', 0)
                if orientation != 0:
                    yaw_angle =90 -math.degrees(orientation)
                    self.logger.info(f"📐 Using shape orientation: {yaw_angle:.1f} (no mask available)")
                    return yaw_angle
                
                self.logger.warn("No mask or orientation available for yaw calculation")
                return getattr(self, 'last_yaw', 0.0)
            
            # 确保mask是numpy数组
            if not isinstance(mask, np.ndarray):
                if isinstance(mask, list):
                    mask = np.array(mask)
                else:
                    self.logger.error(f"Invalid mask type: {type(mask)}")
                    return getattr(self, 'last_yaw', 0.0)
            
            # 确保mask是正确的数据类型
            if mask.dtype != np.uint8:
                mask = mask.astype(np.uint8)
            
            # 检查mask尺寸
            if mask.size == 0 or len(mask.shape) == 0:
                self.logger.warn("Empty mask for yaw calculation")
                return getattr(self, 'last_yaw', 0.0)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                self.logger.warn("No contours found for yaw calculation")
                return getattr(self, 'last_yaw', 0.0)
            
            largest_contour = max(contours, key=cv2.contourArea)
            rect = cv2.minAreaRect(largest_contour)
            _, (width, height), angle = rect
            
            self.logger.info(f"🔧 Rect: w={width:.1f}, h={height:.1f}, angle={angle:.1f}")
            
            # ⭐⭐⭐ 您的yaw计算公式核心 ⭐⭐⭐
            if width > height:
                yaw_angle = 90 - angle
                self.logger.info(f"📏 Width > Height: yaw = 90 - {angle:.1f} = {yaw_angle:.1f}")
            else:
                yaw_angle = -angle
                self.logger.info(f"📏 Height >= Width: yaw = -{angle:.1f} = {yaw_angle:.1f}")
            
            # 先规范化到[-180, 180]
            while yaw_angle > 180:
                yaw_angle -= 360
            while yaw_angle < -180:
                yaw_angle += 360
            
            # ⭐⭐⭐ 与当前yaw对比，选择最小转变 ⭐⭐⭐
            if hasattr(self, 'last_yaw'):
                current_yaw = self.last_yaw
                
                # 计算三种可能的yaw值（原值，+180°，-180°）
                yaw_options = [
                    yaw_angle,
                    yaw_angle + 180,
                    yaw_angle - 180
                ]
                
                # 规范化所有选项到[-180, 180]
                normalized_options = []
                for yaw_opt in yaw_options:
                    while yaw_opt > 180:
                        yaw_opt -= 360
                    while yaw_opt < -180:
                        yaw_opt += 360
                    normalized_options.append(yaw_opt)
                
                # 选择与当前yaw差异最小的
                differences = [abs(opt - current_yaw) for opt in normalized_options]
                best_idx = differences.index(min(differences))
                best_yaw = normalized_options[best_idx]
                
                self.logger.info(f"🔄 Yaw options: {[f'{opt:.1f}' for opt in normalized_options]}")
                self.logger.info(f"🔄 Current: {current_yaw:.1f}, chosen: {best_yaw:.1f} (diff: {min(differences):.1f})")
                
                yaw_angle = best_yaw
            else:
                self.logger.info(f"🆕 First yaw calculation: {yaw_angle:.1f}")
            
            # 最终规范化到[-180, 180]
            while yaw_angle > 180:
                yaw_angle -= 360
            while yaw_angle < -180:
                yaw_angle += 360
            
            # 保存当前yaw为下次对比
            self.last_yaw = yaw_angle
            
            return yaw_angle
            
        except Exception as e:
            self.logger.error(f"Yaw calculation failed: {e}")
            import traceback
            traceback.print_exc()
            return getattr(self, 'last_yaw', 0.0)
    
    def _calculate_gripper_command(self, detection: Dict, phase: str) -> Dict:
        """计算夹爪命令"""
        if phase == 'GRASP_RANGE':
            # 计算夹爪宽度
            shape_features = detection.get('features', {}).get('shape', {})
            minor_axis = shape_features.get('minor_axis_length', 50)
            
            gripper_width = self.config.calculate_gripper_width(minor_axis)
            
            return {
                'position': gripper_width,
                'action': 'grasp'
            }
        else:
            # 非抓取阶段保持打开
            return {
                'position': self.config.gripper.open_position,
                'action': 'open'
            }
    
    def _handle_recovery(self) -> Optional[Dict]:
        """处理回退策略"""
        if not self.last_known_position:
            self.logger.warn("No last known position for recovery")
            return None
        
        # 简单回退：返回最后已知位置
        recovery_command = {
            'pose': {
                'position': self.last_known_position,
                'orientation': {'roll': 179, 'pitch': 0, 'yaw': 0}
            },
            'gripper': {
                'position': self.config.gripper.open_position,
                'action': 'open'
            },
            'phase': 'RECOVERY',
            'state': 'RECOVERING'
        }
        
        return recovery_command
    
    def update_current_pose(self, pose: Dict):
        """更新当前机械臂位姿"""
        self.current_arm_pose = pose
        
        # 记录最后已知位置
        if pose and 'position' in pose:
            self.last_known_position = pose['position'].copy()
    
    def get_status(self) -> Dict:
        """获取追踪状态"""
        with self.lock:
            return {
                'state': self.current_state.value,
                'target_id': self.target_object_id,
                'lost_frames': self.lost_frame_count,
                'tracking_time': time.time() - self.tracking_start_time if self.tracking_start_time else 0,
                'phase_time': time.time() - self.phase_start_time if self.phase_start_time else 0,
                'has_detection': self.current_detection is not None
            }