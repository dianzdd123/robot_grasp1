#!/usr/bin/env python3

import numpy as np
import cv2
from typing import Dict, List, Optional, Tuple
import math

class VisualTracker:
    """视觉追踪器 - 处理图像级别的目标跟踪"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        
        # 追踪状态
        self.current_frame = None
        self.target_bbox = None
        self.target_mask = None
        self.tracking_confidence = 0.0
        
        # 卡尔曼滤波器用于位置预测
        self.kalman = self._init_kalman_filter()
        
        # 追踪历史
        self.position_history = []
        self.confidence_history = []
        
        self.logger.info("👁️ VisualTracker initialized")
    
    def _init_kalman_filter(self):
        """初始化卡尔曼滤波器用于位置预测"""
        kalman = cv2.KalmanFilter(4, 2)  # 4状态(x,y,vx,vy), 2观测(x,y)
        
        # 状态转移矩阵
        kalman.transitionMatrix = np.array([[1,0,1,0],
                                          [0,1,0,1], 
                                          [0,0,1,0],
                                          [0,0,0,1]], np.float32)
        
        # 观测矩阵
        kalman.measurementMatrix = np.array([[1,0,0,0],
                                           [0,1,0,0]], np.float32)
        
        # 初始协方差
        kalman.processNoiseCov = 0.03 * np.eye(4, dtype=np.float32)
        kalman.measurementNoiseCov = 0.1 * np.eye(2, dtype=np.float32)
        kalman.errorCovPost = 0.1 * np.eye(4, dtype=np.float32)
        
        return kalman
    
    def update_frame(self, frame: np.ndarray):
        """更新当前帧"""
        self.current_frame = frame.copy()
    
    def track_target(self, detection: Dict) -> Dict:
        """追踪目标对象"""
        if not detection:
            return self._handle_tracking_failure()
        
        # 提取目标信息
        bbox = detection.get('bounding_box', [0,0,0,0])
        confidence = detection.get('confidence', 0.0)
        
        # 更新目标状态
        self.target_bbox = bbox
        self.tracking_confidence = confidence
        
        # 计算质心
        centroid = self._calculate_centroid(bbox, detection.get('mask'))
        
        # 卡尔曼滤波预测
        predicted_pos = self._predict_position(centroid)
        
        # 更新历史
        self._update_history(centroid, confidence)
        
        # 计算运动特征
        motion_features = self._analyze_motion()
        
        tracking_result = {
            'bbox': bbox,
            'centroid': centroid,
            'predicted_position': predicted_pos,
            'confidence': confidence,
            'motion_features': motion_features,
            'tracking_quality': self._assess_tracking_quality()
        }
        
        return tracking_result
    
    def _calculate_centroid(self, bbox: List, mask=None) -> Tuple[float, float]:
        """计算目标质心"""
        if mask is not None and hasattr(mask, 'shape'):
            # 使用mask计算精确质心
            mask_array = np.array(mask) if not isinstance(mask, np.ndarray) else mask
            moments = cv2.moments(mask_array.astype(np.uint8))
            
            if moments['m00'] > 0:
                cx = moments['m10'] / moments['m00']
                cy = moments['m01'] / moments['m00']
                return (cx, cy)
        
        # 回退到bbox中心
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2, (y1 + y2) / 2)
    
    def _predict_position(self, current_pos: Tuple[float, float]) -> Tuple[float, float]:
        """使用卡尔曼滤波预测下一位置"""
        if not hasattr(self, '_kalman_initialized'):
            # 初始化卡尔曼滤波器状态
            self.kalman.statePre = np.array([current_pos[0], current_pos[1], 0, 0], np.float32)
            self.kalman.statePost = self.kalman.statePre.copy()
            self._kalman_initialized = True
            return current_pos
        
        # 预测
        prediction = self.kalman.predict()
        
        # 更新观测
        measurement = np.array([[current_pos[0]], [current_pos[1]]], np.float32)
        self.kalman.correct(measurement)
        
        return (prediction[0], prediction[1])
    
    def _update_history(self, position: Tuple[float, float], confidence: float):
        """更新追踪历史"""
        self.position_history.append(position)
        self.confidence_history.append(confidence)
        
        # 保持历史长度
        max_history = 30
        if len(self.position_history) > max_history:
            self.position_history = self.position_history[-max_history:]
            self.confidence_history = self.confidence_history[-max_history:]
    
    def _analyze_motion(self) -> Dict:
        """分析目标运动特征"""
        if len(self.position_history) < 3:
            return {
                'velocity': (0, 0),
                'acceleration': (0, 0),
                'direction': 0,
                'speed': 0,
                'is_moving': False
            }
        
        positions = np.array(self.position_history[-5:])  # 最近5帧
        
        # 计算速度 (pixels/frame)
        velocities = np.diff(positions, axis=0)
        avg_velocity = np.mean(velocities, axis=0)
        
        # 计算加速度
        if len(velocities) > 1:
            accelerations = np.diff(velocities, axis=0)
            avg_acceleration = np.mean(accelerations, axis=0)
        else:
            avg_acceleration = np.array([0, 0])
        
        # 计算运动方向和速度
        speed = np.linalg.norm(avg_velocity)
        direction = math.atan2(avg_velocity[1], avg_velocity[0]) if speed > 0 else 0
        
        # 判断是否在运动
        is_moving = speed > 2.0  # 像素阈值
        
        return {
            'velocity': tuple(avg_velocity),
            'acceleration': tuple(avg_acceleration), 
            'direction': direction,
            'speed': speed,
            'is_moving': is_moving
        }
    
    def _assess_tracking_quality(self) -> float:
        """评估追踪质量"""
        if len(self.confidence_history) == 0:
            return 0.0
        
        # 基于置信度历史
        recent_confidences = self.confidence_history[-10:]
        avg_confidence = np.mean(recent_confidences)
        confidence_stability = 1.0 - np.std(recent_confidences)
        
        # 基于位置稳定性
        position_stability = 1.0
        if len(self.position_history) > 5:
            recent_positions = np.array(self.position_history[-5:])
            position_variance = np.var(recent_positions, axis=0)
            position_stability = max(0, 1.0 - np.mean(position_variance) / 1000.0)
        
        # 综合质量分数
        quality = 0.6 * avg_confidence + 0.3 * confidence_stability + 0.1 * position_stability
        return max(0.0, min(1.0, quality))
    
    def _handle_tracking_failure(self) -> Dict:
        """处理追踪失败"""
        # 使用卡尔曼滤波预测位置
        if hasattr(self, '_kalman_initialized') and len(self.position_history) > 0:
            predicted = self.kalman.predict()
            predicted_pos = (predicted[0], predicted[1])
        else:
            predicted_pos = (0, 0)
        
        return {
            'bbox': [0, 0, 0, 0],
            'centroid': (0, 0),
            'predicted_position': predicted_pos,
            'confidence': 0.0,
            'motion_features': {
                'velocity': (0, 0),
                'acceleration': (0, 0),
                'direction': 0,
                'speed': 0,
                'is_moving': False
            },
            'tracking_quality': 0.0
        }
    
    def get_search_region(self, expansion_factor: float = 1.5) -> Tuple[int, int, int, int]:
        """获取搜索区域"""
        if not self.target_bbox:
            return (0, 0, 0, 0)
        
        x1, y1, x2, y2 = self.target_bbox
        width, height = x2 - x1, y2 - y1
        
        # 扩展搜索区域
        center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
        new_width = width * expansion_factor
        new_height = height * expansion_factor
        
        new_x1 = int(center_x - new_width / 2)
        new_y1 = int(center_y - new_height / 2)
        new_x2 = int(center_x + new_width / 2)
        new_y2 = int(center_y + new_height / 2)
        
        return (new_x1, new_y1, new_x2, new_y2)
    
    def reset(self):
        """重置追踪器"""
        self.target_bbox = None
        self.target_mask = None
        self.tracking_confidence = 0.0
        self.position_history.clear()
        self.confidence_history.clear()
        
        # 重新初始化卡尔曼滤波器
        self.kalman = self._init_kalman_filter()
        if hasattr(self, '_kalman_initialized'):
            delattr(self, '_kalman_initialized')
        
        self.logger.info("🔄 VisualTracker reset")