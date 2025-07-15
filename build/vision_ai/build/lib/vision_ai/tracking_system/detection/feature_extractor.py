import cv2
import numpy as np
from typing import Dict, Optional

class RealtimeFeatureExtractor:
    """
    实时特征提取器，只提取tracking需要的核心特征
    """
    
    def __init__(self, logger):
        self.logger = logger
    
    def extract_tracking_features(self, image_rgb: np.ndarray, mask: np.ndarray) -> Dict:
        """
        提取tracking需要的核心特征
        
        Args:
            image_rgb: RGB图像
            mask: 对象mask
            
        Returns:
            Dict: 特征字典
        """
        features = {}
        
        try:
            # 1. 颜色特征
            features['color'] = self._extract_color_features(image_rgb, mask)
            
            # 2. 形状特征
            features['shape'] = self._extract_shape_features(mask)
            
            # 3. 空间特征
            features['spatial'] = self._extract_spatial_features(mask)
            
        except Exception as e:
            self.logger.error(f'Feature extraction failed: {e}')
            features = {'error': str(e)}
        
        return features
    
    def _extract_color_features(self, image_rgb: np.ndarray, mask: np.ndarray) -> Dict:
        """提取颜色特征"""
        try:
            # 提取mask区域的像素
            masked_pixels = image_rgb[mask > 0]
            
            if len(masked_pixels) == 0:
                return {'color_name': 'unknown', 'histogram': []}
            
            # 1. 主色调检测
            color_name = self._detect_dominant_color(masked_pixels)
            
            # 2. 颜色直方图
            histogram = self._compute_color_histogram(masked_pixels)
            
            return {
                'color_name': color_name,
                'histogram': histogram.tolist() if histogram is not None else [],
                'mean_rgb': np.mean(masked_pixels, axis=0).tolist()
            }
            
        except Exception as e:
            self.logger.error(f'Color feature extraction failed: {e}')
            return {'color_name': 'unknown', 'histogram': []}
    
    def _detect_dominant_color(self, pixels: np.ndarray) -> str:
        """检测主色调"""
        try:
            # 计算中位数颜色
            median_color = np.median(pixels, axis=0)
            r, g, b = median_color
            
            # 转换为HSV
            hsv_color = cv2.cvtColor(np.uint8([[median_color]]), cv2.COLOR_RGB2HSV)[0][0]
            h, s, v = hsv_color
            
            # 基于HSV分类
            if s < 30:  # 低饱和度
                if v > 200:
                    return "white"
                elif v < 60:
                    return "black"
                else:
                    return "gray"
            
            # 高饱和度颜色分类
            if h < 15 or h > 165:
                return "red"
            elif 15 <= h < 35:
                return "yellow" if r > 180 and g > 150 else "orange"
            elif 35 <= h < 85:
                return "green"
            elif 85 <= h < 125:
                return "cyan"
            elif 125 <= h < 165:
                return "blue"
            
            return "mixed"
            
        except Exception:
            return "unknown"
    
    def _compute_color_histogram(self, pixels: np.ndarray) -> Optional[np.ndarray]:
        """计算颜色直方图"""
        try:
            # 转换为HSV
            hsv_pixels = cv2.cvtColor(pixels.reshape(-1, 1, 3), cv2.COLOR_RGB2HSV)
            hsv_pixels = hsv_pixels.reshape(-1, 3)
            
            # 计算2D直方图 (H-S)
            hist = cv2.calcHist([hsv_pixels], [0, 1], None, [50, 60], [0, 180, 0, 256])
            
            # 归一化
            hist = cv2.normalize(hist, hist).flatten()
            
            return hist
            
        except Exception as e:
            self.logger.error(f'Histogram computation failed: {e}')
            return None
    
    def _extract_shape_features(self, mask: np.ndarray) -> Dict:
        """提取形状特征"""
        try:
            # 查找轮廓
            contours, _ = cv2.findContours(
                mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            
            if not contours:
                return {'hu_moments': [], 'area': 0, 'contours': []}
            
            # 找到最大轮廓
            largest_contour = max(contours, key=cv2.contourArea)
            
            # 1. Hu矩
            hu_moments = self._compute_hu_moments(largest_contour)
            
            # 2. 基本几何特征
            area = cv2.contourArea(largest_contour)
            
            # 3. 简化轮廓
            epsilon = 0.02 * cv2.arcLength(largest_contour, True)
            approx_contour = cv2.approxPolyDP(largest_contour, epsilon, True)
            contour_points = approx_contour.reshape(-1, 2).tolist()
            
            return {
                'hu_moments': hu_moments.tolist() if hu_moments is not None else [],
                'area': float(area),
                'contours': contour_points
            }
            
        except Exception as e:
            self.logger.error(f'Shape feature extraction failed: {e}')
            return {'hu_moments': [], 'area': 0, 'contours': []}
    
    def _compute_hu_moments(self, contour: np.ndarray) -> Optional[np.ndarray]:
        """计算Hu矩"""
        try:
            # 计算moments
            moments = cv2.moments(contour)
            
            # 计算Hu矩
            hu_moments = cv2.HuMoments(moments).flatten()
            
            # 对数变换
            hu_moments = -np.sign(hu_moments) * np.log10(np.abs(hu_moments) + 1e-10)
            
            return hu_moments
            
        except Exception as e:
            self.logger.error(f'Hu moments computation failed: {e}')
            return None
    
    def _extract_spatial_features(self, mask: np.ndarray) -> Dict:
        """提取空间特征"""
        try:
            # 找到mask中心点
            ys, xs = np.where(mask > 0)
            
            if len(xs) == 0:
                return {'centroid_2d': [0, 0], 'area': 0}
            
            centroid_x = float(np.mean(xs))
            centroid_y = float(np.mean(ys))
            area = len(xs)
            
            return {
                'centroid_2d': [centroid_x, centroid_y],
                'area': area
            }
            
        except Exception as e:
            self.logger.error(f'Spatial feature extraction failed: {e}')
            return {'centroid_2d': [0, 0], 'area': 0}