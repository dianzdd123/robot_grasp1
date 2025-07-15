# detection/features/shape_features.py
import cv2
import numpy as np
from typing import Dict, Tuple

class ShapeFeatureExtractor:
    """形状特征提取器"""
    
    def __init__(self):
        """初始化形状特征提取器"""
        pass
    
    def compute_hu_moments(self, mask: np.ndarray) -> np.ndarray:
        """
        计算mask的Hu不变矩
        
        Args:
            mask: 二值掩码 (H, W)
            
        Returns:
            hu_moments: Hu不变矩 (7,)
        """
        # 确保mask是二值图像
        mask_binary = (mask > 0).astype(np.uint8) * 255
        
        # 计算图像矩
        moments = cv2.moments(mask_binary)
        
        # 计算Hu不变矩
        hu_moments = cv2.HuMoments(moments)
        
        # 对Hu矩进行对数变换，使其在相似的数量级上
        for i in range(7):
            if hu_moments[i] != 0:
                hu_moments[i] = -1 * np.sign(hu_moments[i]) * np.log10(np.abs(hu_moments[i]))
            else:
                hu_moments[i] = 0
        
        return hu_moments.flatten()
    
    def compute_shape_descriptors(self, mask: np.ndarray) -> Dict:
        """
        计算形状描述符
        
        Args:
            mask: 二值掩码 (H, W)
            
        Returns:
            descriptors: 形状描述符字典
        """
        if np.sum(mask) == 0:
            return {
                'area': 0,
                'perimeter': 0,
                'circularity': 0,
                'aspect_ratio': 0,
                'extent': 0,
                'solidity': 0,
                'compactness': 0
            }
        
        # 确保mask是二值图像
        mask_binary = (mask > 0).astype(np.uint8) * 255
        
        # 找到轮廓
        contours, _ = cv2.findContours(mask_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return {
                'area': 0,
                'perimeter': 0,
                'circularity': 0,
                'aspect_ratio': 0,
                'extent': 0,
                'solidity': 0,
                'compactness': 0
            }
        
        # 选择最大的轮廓
        largest_contour = max(contours, key=cv2.contourArea)
        
        # 计算基本几何属性
        area = cv2.contourArea(largest_contour)
        perimeter = cv2.arcLength(largest_contour, True)
        
        # 计算边界矩形
        x, y, w, h = cv2.boundingRect(largest_contour)
        bounding_area = w * h
        
        # 计算凸包
        hull = cv2.convexHull(largest_contour)
        hull_area = cv2.contourArea(hull)
        
        # 计算各种形状描述符
        circularity = 4 * np.pi * area / (perimeter * perimeter + 1e-10)
        aspect_ratio = float(w) / (h + 1e-10)
        extent = float(area) / (bounding_area + 1e-10)
        solidity = float(area) / (hull_area + 1e-10)
        compactness = (perimeter * perimeter) / (area + 1e-10)
        
        return {
            'area': area,
            'perimeter': perimeter,
            'circularity': circularity,
            'aspect_ratio': aspect_ratio,
            'extent': extent,
            'solidity': solidity,
            'compactness': compactness
        }
    
    def compute_contour_features(self, mask: np.ndarray) -> Dict:
        """
        计算轮廓特征
        
        Args:
            mask: 二值掩码 (H, W)
            
        Returns:
            features: 轮廓特征字典
        """
        if np.sum(mask) == 0:
            return {
                'centroid': (0, 0),
                'orientation': 0,
                'major_axis_length': 0,
                'minor_axis_length': 0,
                'eccentricity': 0
            }
        
        # 确保mask是二值图像
        mask_binary = (mask > 0).astype(np.uint8) * 255
        
        # 计算图像矩
        moments = cv2.moments(mask_binary)
        
        # 计算质心
        if moments['m00'] != 0:
            centroid_x = int(moments['m10'] / moments['m00'])
            centroid_y = int(moments['m01'] / moments['m00'])
        else:
            centroid_x, centroid_y = 0, 0
        
        # 计算中心矩
        mu20 = moments['mu20'] / moments['m00']
        mu02 = moments['mu02'] / moments['m00']
        mu11 = moments['mu11'] / moments['m00']
        
        # 计算协方差矩阵的特征值和特征向量
        # 用于计算主轴方向和长度
        delta = 4 * mu11**2 + (mu20 - mu02)**2
        if delta >= 0:
            lambda1 = (mu20 + mu02 + np.sqrt(delta)) / 2
            lambda2 = (mu20 + mu02 - np.sqrt(delta)) / 2
        else:
            lambda1 = lambda2 = (mu20 + mu02) / 2
        
        # 计算方向角（弧度）
        if mu20 != mu02:
            orientation = 0.5 * np.arctan(2 * mu11 / (mu20 - mu02))
        else:
            orientation = 0 if mu11 == 0 else np.pi / 4
        
        # 计算主轴长度
        major_axis_length = 2 * np.sqrt(2 * lambda1) if lambda1 > 0 else 0
        minor_axis_length = 2 * np.sqrt(2 * lambda2) if lambda2 > 0 else 0
        
        # 计算离心率
        if major_axis_length > 0:
            eccentricity = np.sqrt(1 - (minor_axis_length / major_axis_length)**2)
        else:
            eccentricity = 0
        
        return {
            'centroid': (centroid_x, centroid_y),
            'orientation': orientation,
            'major_axis_length': major_axis_length,
            'minor_axis_length': minor_axis_length,
            'eccentricity': eccentricity
        }
    
    def compute_hu_similarity(self, hu1: np.ndarray, hu2: np.ndarray) -> float:
        """
        计算两个Hu矩的相似度
        
        Args:
            hu1: 第一个Hu矩
            hu2: 第二个Hu矩
            
        Returns:
            similarity: 相似度 (0-1之间)
        """
        # 使用欧氏距离计算差异
        distance = np.linalg.norm(hu1 - hu2)
        
        # 将距离转换为相似度（0-1之间）
        # 使用指数函数，距离越小相似度越高
        similarity = np.exp(-distance / 10.0)  # 10.0是缩放因子，可以调整
        
        return similarity
    
    def extract_all_features(self, mask: np.ndarray) -> Dict:
        """
        提取所有形状特征
        
        Args:
            mask: 二值掩码 (H, W)
            
        Returns:
            features: 所有形状特征字典
        """
        hu_moments = self.compute_hu_moments(mask)
        shape_descriptors = self.compute_shape_descriptors(mask)
        contour_features = self.compute_contour_features(mask)
        
        # 合并所有特征
        all_features = {
            'hu_moments': hu_moments,
            **shape_descriptors,
            **contour_features
        }
        
        return all_features