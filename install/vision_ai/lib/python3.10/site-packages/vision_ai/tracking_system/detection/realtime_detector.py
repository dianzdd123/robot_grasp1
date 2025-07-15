# =============================================================================
# 文件 1: realtime_detector.py
# =============================================================================

import cv2
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import time
from datetime import datetime

class RealtimeDetector:
    """
    独立的实时检测器，专门为tracking系统设计
    避免与detection_pipeline冲突
    """
    
    def __init__(self, config, logger):
        """
        初始化实时检测器
        
        Args:
            config: TrackingSystemConfig实例
            logger: ROS logger
        """
        self.config = config
        self.logger = logger
        
        # 模型组件
        self.detector = None
        self.segmentor = None
        
        # 特征提取器
        self.feature_extractor = None
        
        # 性能统计
        self.detection_stats = {
            'total_detections': 0,
            'total_time': 0.0,
            'avg_fps': 0.0
        }
        
        self._initialize_models()
        self._initialize_feature_extractor()
    
    def _initialize_models(self):
        """初始化YOLO和SAM2模型"""
        try:
            # 复用detection模块的ModelFactory，但不创建pipeline
            from vision_ai.detection.utils.model_factory import ModelFactory
            
            detector_config = self._get_detector_config()
            segmentor_config = self._get_segmentor_config()
            
            self.detector, self.segmentor = ModelFactory.create_from_config(
                detector_config, segmentor_config
            )
            
            self.logger.info('✅ Realtime detector models initialized')
            
        except Exception as e:
            self.logger.error(f'❌ Failed to initialize detection models: {e}')
            raise
    
    def _get_detector_config(self):
        """获取检测器配置"""
        return {
            'model_type': 'yolo',
            'model_path': '/home/qi/ros2_ws/src/vision_ai/models/yolo/best.pt',
            'confidence_threshold': 0.6,  # 稍高的阈值用于实时检测
            'nms_threshold': 0.4,
            'device': 'cuda'
        }
    
    def _get_segmentor_config(self):
        """获取分割器配置"""
        return {
            'model_type': 'sam2',
            'checkpoint_path': '/home/qi/ros2_ws/src/vision_ai/models/sam2/sam2_hiera_large.pt',
            'model_cfg': 'sam2_hiera_l.yaml',
            'device': 'cuda'
        }
    
    def _initialize_feature_extractor(self):
        """初始化轻量级特征提取器"""
        try:
            from .feature_extractor import RealtimeFeatureExtractor
            
            self.feature_extractor = RealtimeFeatureExtractor(self.logger)
            
            self.logger.info('✅ Realtime feature extractor initialized')
            
        except Exception as e:
            self.logger.error(f'❌ Failed to initialize feature extractor: {e}')
            raise
    
    def detect_and_segment(self, image_rgb: np.ndarray) -> List[Dict]:
        """
        执行实时检测和分割
        
        Args:
            image_rgb: RGB图像 (H, W, 3)
            
        Returns:
            List[Dict]: 检测结果列表
        """
        start_time = time.time()
        
        try:
            # 1. YOLO检测
            boxes, class_ids, confidences = self.detector.detect(image_rgb)
            
            if len(boxes) == 0:
                return []
            
            # 2. SAM2分割
            masks = self.segmentor.segment(image_rgb, boxes)
            
            # 3. 构建结果
            results = []
            class_names = self.detector.get_class_names()
            
            for box, class_id, confidence, mask in zip(boxes, class_ids, confidences, masks):
                # 提取基本特征
                features = self.feature_extractor.extract_tracking_features(
                    image_rgb, mask
                )
                
                result = {
                    'class_id': int(class_id),
                    'class_name': class_names.get(class_id, f'class_{class_id}'),
                    'confidence': float(confidence),
                    'bounding_box': box.tolist(),
                    'mask': mask,
                    'features': features,
                    'detection_time': time.time()
                }
                
                results.append(result)
            
            # 更新统计信息
            detection_time = time.time() - start_time
            self._update_stats(len(results), detection_time)
            
            return results
            
        except Exception as e:
            self.logger.error(f'Realtime detection failed: {e}')
            return []
    
    def _update_stats(self, detection_count: int, detection_time: float):
        """更新性能统计"""
        self.detection_stats['total_detections'] += detection_count
        self.detection_stats['total_time'] += detection_time
        
        if self.detection_stats['total_time'] > 0:
            self.detection_stats['avg_fps'] = 1.0 / (
                self.detection_stats['total_time'] / max(1, self.detection_stats['total_detections'])
            )
    
    def get_stats(self) -> Dict:
        """获取性能统计"""
        return self.detection_stats.copy()
    
    def reset_stats(self):
        """重置统计信息"""
        self.detection_stats = {
            'total_detections': 0,
            'total_time': 0.0,
            'avg_fps': 0.0
        }