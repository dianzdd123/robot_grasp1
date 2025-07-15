#!/usr/bin/env python3

import numpy as np
import cv2
from typing import Dict, List, Optional, Tuple
from scipy import spatial
import json

class FeatureManager:
    """特征管理器 - 提取、比较和管理目标特征"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        
        # 特征权重配置
        self.weights = config.tracking.feature_weights
        
        # 阈值配置
        self.color_threshold = config.tracking.color_hist_threshold
        self.hu_threshold = config.tracking.hu_moment_threshold
        self.position_threshold = config.tracking.position_continuity_threshold
        
        self.logger.info("🧬 FeatureManager initialized")
    
    def extract_features(self, detection: Dict, image: Optional[np.ndarray] = None) -> Dict:
        """从检测结果提取追踪特征"""
        features = detection.get('features', {})
        
        # 基础特征
        tracking_features = {
            'color_histogram': self._extract_color_histogram(features),
            'hu_moments': self._extract_hu_moments(features),
            'shape_features': self._extract_shape_features(features),
            'spatial_features': self._extract_spatial_features(features),
            'texture_features': self._extract_texture_features(detection, image)
        }
        
        # 计算特征描述符
        tracking_features['descriptor'] = self._compute_feature_descriptor(tracking_features)
        
        return tracking_features
    
    def _extract_color_histogram(self, features: Dict) -> List[float]:
        """提取颜色直方图特征"""
        color_info = features.get('color', {})
        histogram = color_info.get('histogram', [])
        
        if not histogram:
            return [0.0] * 256  # 默认空直方图
        
        # 归一化直方图
        hist_array = np.array(histogram)
        if np.sum(hist_array) > 0:
            normalized = hist_array / np.sum(hist_array)
            return normalized.tolist()
        
        return histogram
    
    def _extract_hu_moments(self, features: Dict) -> List[float]:
        """提取Hu矩特征"""
        shape_info = features.get('shape', {})
        hu_moments = shape_info.get('hu_moments', [])
        
        if not hu_moments or len(hu_moments) < 7:
            return [0.0] * 7
        
        # 使用前7个Hu矩，但重点关注前3个
        return hu_moments[:7]
    
    def _extract_shape_features(self, features: Dict) -> Dict:
        """提取形状特征"""
        shape_info = features.get('shape', {})
        
        return {
            'area': shape_info.get('area', 0),
            'perimeter': shape_info.get('perimeter', 0),
            'circularity': shape_info.get('circularity', 0),
            'aspect_ratio': shape_info.get('aspect_ratio', 1.0),
            'extent': shape_info.get('extent', 0),
            'solidity': shape_info.get('solidity', 0),
            'compactness': shape_info.get('compactness', 0),
            'eccentricity': shape_info.get('eccentricity', 0),
            'orientation': shape_info.get('orientation', 0)
        }
    
    def _extract_spatial_features(self, features: Dict) -> Dict:
        """提取空间特征"""
        spatial_info = features.get('spatial', {})
        
        return {
            'centroid_2d': spatial_info.get('centroid_2d', (0, 0)),
            'normalized_coords': spatial_info.get('normalized_coords', (0, 0)),
            'region_position': spatial_info.get('region_position', 'center'),
            'world_coordinates': spatial_info.get('world_coordinates', (0, 0, 0)),
            'distance_to_camera': spatial_info.get('distance_to_camera', 1.0)
        }
    
    def _extract_texture_features(self, detection: Dict, image: Optional[np.ndarray]) -> Dict:
        """提取纹理特征（简化版）"""
        if image is None:
            return {'lbp_histogram': [], 'glcm_features': []}
        
        try:
            bbox = detection.get('bounding_box', [0, 0, 0, 0])
            x1, y1, x2, y2 = map(int, bbox)
            
            # 提取ROI
            roi = image[y1:y2, x1:x2]
            if roi.size == 0:
                return {'lbp_histogram': [], 'glcm_features': []}
            
            # 转换为灰度
            if len(roi.shape) == 3:
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            else:
                gray_roi = roi
            
            # 简单的纹理特征：梯度统计
            grad_x = cv2.Sobel(gray_roi, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray_roi, cv2.CV_64F, 0, 1, ksize=3)
            
            texture_features = {
                'grad_mean': float(np.mean(np.abs(grad_x) + np.abs(grad_y))),
                'grad_std': float(np.std(np.abs(grad_x) + np.abs(grad_y))),
                'intensity_mean': float(np.mean(gray_roi)),
                'intensity_std': float(np.std(gray_roi))
            }
            
            return texture_features
            
        except Exception as e:
            self.logger.error(f"Texture extraction failed: {e}")
            return {'grad_mean': 0, 'grad_std': 0, 'intensity_mean': 0, 'intensity_std': 0}
    
    def _compute_feature_descriptor(self, features: Dict) -> np.ndarray:
        """计算综合特征描述符"""
        descriptor_parts = []
        
        # 颜色直方图部分
        color_hist = features.get('color_histogram', [])
        if color_hist:
            # 降维到32个bin
            if len(color_hist) > 32:
                downsampled = np.array(color_hist).reshape(-1, len(color_hist)//32).mean(axis=1)
                descriptor_parts.extend(downsampled.tolist())
            else:
                descriptor_parts.extend(color_hist[:32])
        
        # Hu矩前3个
        hu_moments = features.get('hu_moments', [])
        if hu_moments:
            descriptor_parts.extend(hu_moments[:3])
        
        # 关键形状特征
        shape_features = features.get('shape_features', {})
        key_shape = [
            shape_features.get('area', 0),
            shape_features.get('aspect_ratio', 1.0),
            shape_features.get('circularity', 0),
            shape_features.get('eccentricity', 0)
        ]
        descriptor_parts.extend(key_shape)
        
        # 归一化
        descriptor = np.array(descriptor_parts)
        if np.linalg.norm(descriptor) > 0:
            descriptor = descriptor / np.linalg.norm(descriptor)
        
        return descriptor
    
    def compare_features(self, features1: Dict, features2: Dict) -> float:
        """比较两组特征的相似度"""
        total_similarity = 0.0
        weight_sum = 0.0
        
        # 颜色直方图相似度
        color_sim = self._compare_color_histograms(
            features1.get('color_histogram', []),
            features2.get('color_histogram', [])
        )
        if color_sim >= 0:
            total_similarity += self.weights['color_hist'] * color_sim
            weight_sum += self.weights['color_hist']
        
        # 形状相似度
        shape_sim = self._compare_shape_features(
            features1.get('hu_moments', []),
            features2.get('hu_moments', []),
            features1.get('shape_features', {}),
            features2.get('shape_features', {})
        )
        if shape_sim >= 0:
            total_similarity += self.weights['shape_moments'] * shape_sim
            weight_sum += self.weights['shape_moments']
        
        # 位置连续性
        position_sim = self._compare_spatial_features(
            features1.get('spatial_features', {}),
            features2.get('spatial_features', {})
        )
        if position_sim >= 0:
            total_similarity += self.weights['position_continuity'] * position_sim
            weight_sum += self.weights['position_continuity']
        
        # 综合相似度
        if weight_sum > 0:
            return total_similarity / weight_sum
        return 0.0
    
    def _compare_color_histograms(self, hist1: List, hist2: List) -> float:
        """比较颜色直方图（Chi-square距离）"""
        if not hist1 or not hist2 or len(hist1) != len(hist2):
            return -1.0
        
        h1 = np.array(hist1, dtype=np.float64)
        h2 = np.array(hist2, dtype=np.float64)
        
        # 归一化
        h1 = h1 / (np.sum(h1) + 1e-10)
        h2 = h2 / (np.sum(h2) + 1e-10)
        
        # Chi-square距离
        chi_square = np.sum((h1 - h2) ** 2 / (h1 + h2 + 1e-10))
        
        # 转换为相似度
        similarity = max(0, 1 - chi_square / 2)
        return similarity
    
    def _compare_shape_features(self, hu1: List, hu2: List, shape1: Dict, shape2: Dict) -> float:
        """比较形状特征"""
        similarities = []
        
        # Hu矩相似度
        if hu1 and hu2 and len(hu1) >= 3 and len(hu2) >= 3:
            hu_sim = self._compare_hu_moments(hu1[:3], hu2[:3])
            similarities.append(hu_sim)
        
        # 几何特征相似度
        geometric_features = ['area', 'aspect_ratio', 'circularity', 'eccentricity']
        for feature in geometric_features:
            val1 = shape1.get(feature, 0)
            val2 = shape2.get(feature, 0)
            
            if val1 > 0 and val2 > 0:
                ratio = min(val1, val2) / max(val1, val2)
                similarities.append(ratio)
        
        return np.mean(similarities) if similarities else -1.0
    
    def _compare_hu_moments(self, hu1: List, hu2: List) -> float:
        """比较Hu矩"""
        if not hu1 or not hu2 or len(hu1) != len(hu2):
            return 0.0
        
        # 对数变换以处理大值
        log_hu1 = [-np.sign(h) * np.log10(abs(h) + 1e-10) for h in hu1]
        log_hu2 = [-np.sign(h) * np.log10(abs(h) + 1e-10) for h in hu2]
        
        # 欧氏距离
        distance = np.linalg.norm(np.array(log_hu1) - np.array(log_hu2))
        
        # 转换为相似度
        similarity = max(0, 1 - distance / 10)
        return similarity
    
    def _compare_spatial_features(self, spatial1: Dict, spatial2: Dict) -> float:
        """比较空间特征"""
        centroid1 = spatial1.get('centroid_2d', (0, 0))
        centroid2 = spatial2.get('centroid_2d', (0, 0))
        
        if not centroid1 or not centroid2:
            return -1.0
        
        # 计算位置距离
        distance = np.sqrt((centroid1[0] - centroid2[0])**2 + (centroid1[1] - centroid2[1])**2)
        
        # 转换为相似度
        similarity = max(0, 1 - distance / self.position_threshold)
        return similarity
    
    def update_reference_features(self, current_features: Dict, reference_features: Dict, 
                                learning_rate: float = 0.1) -> Dict:
        """更新参考特征（适应性学习）"""
        updated_features = reference_features.copy()
        
        # 更新颜色直方图
        if (current_features.get('color_histogram') and 
            reference_features.get('color_histogram')):
            
            curr_hist = np.array(current_features['color_histogram'])
            ref_hist = np.array(reference_features['color_histogram'])
            
            if len(curr_hist) == len(ref_hist):
                updated_hist = (1 - learning_rate) * ref_hist + learning_rate * curr_hist
                updated_features['color_histogram'] = updated_hist.tolist()
        
        # 更新空间位置
        curr_spatial = current_features.get('spatial_features', {})
        if curr_spatial.get('centroid_2d'):
            updated_features['spatial_features'] = curr_spatial.copy()
        
        return updated_features
    
    def validate_features(self, features: Dict) -> bool:
        """验证特征的有效性"""
        # 检查必要特征
        required_features = ['color_histogram', 'hu_moments', 'spatial_features']
        
        for feature_name in required_features:
            if feature_name not in features:
                return False
            
            feature_data = features[feature_name]
            if not feature_data:
                return False
        
        # 检查数据格式
        color_hist = features['color_histogram']
        if not isinstance(color_hist, list) or len(color_hist) == 0:
            return False
        
        hu_moments = features['hu_moments']
        if not isinstance(hu_moments, list) or len(hu_moments) < 3:
            return False
        
        return True
    
    def get_feature_summary(self, features: Dict) -> str:
        """获取特征摘要"""
        summary_parts = []
        
        # 颜色信息
        color_hist = features.get('color_histogram', [])
        if color_hist:
            dominant_bins = np.argsort(color_hist)[-3:]
            summary_parts.append(f"Color peaks: {dominant_bins}")
        
        # 形状信息
        shape_features = features.get('shape_features', {})
        aspect_ratio = shape_features.get('aspect_ratio', 1.0)
        circularity = shape_features.get('circularity', 0.0)
        summary_parts.append(f"Shape: AR={aspect_ratio:.2f}, Circ={circularity:.2f}")
        
        # 位置信息
        spatial = features.get('spatial_features', {})
        centroid = spatial.get('centroid_2d', (0, 0))
        summary_parts.append(f"Position: ({centroid[0]:.0f}, {centroid[1]:.0f})")
        
        return " | ".join(summary_parts)