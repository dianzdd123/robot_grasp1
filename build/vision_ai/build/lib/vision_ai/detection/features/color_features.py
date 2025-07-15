# detection/features/color_features.py
import cv2
import numpy as np
from typing import Tuple, Dict

class ColorFeatureExtractor:
    """颜色特征提取器"""
    
    def __init__(self, bins: int = 64):
        """
        初始化颜色特征提取器
        
        Args:
            bins: 直方图的bin数量
        """
        self.bins = bins
        
        # 颜色语义映射
        self.color_mapping = {
            'red': [(150, 255), (0, 100), (0, 100)],        # 红色
            'yellow': [(200, 255), (200, 255), (0, 100)],   # 黄色
            'orange': [(200, 255), (100, 200), (0, 100)],   # 橙色
            'green': [(0, 100), (150, 255), (0, 100)],      # 绿色
            'white': [(200, 255), (200, 255), (200, 255)],  # 白色
            'black': [(0, 80), (0, 80), (0, 80)],           # 黑色
            'purple': [(100, 255), (0, 100), (150, 255)],   # 紫色
            'brown': [(80, 150), (50, 120), (20, 80)],      # 棕色
        }
    
    def compute_color_histogram(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        计算mask区域的颜色直方图
        
        Args:
            image: RGB图像 (H, W, 3)
            mask: 二值掩码 (H, W)
            
        Returns:
            hist: 归一化的颜色直方图 (bins*3,)
        """
        if np.sum(mask) == 0:
            return np.zeros((self.bins * 3,))
        
        # 确保image是正确的数据类型和内存布局
        if image.dtype != np.uint8:
            image = image.astype(np.uint8)
        
        # 确保image是连续的内存布局
        if not image.flags['C_CONTIGUOUS']:
            image = np.ascontiguousarray(image)
        
        # 确保mask是正确的数据类型
        if mask.dtype != np.uint8:
            mask = mask.astype(np.uint8)
        
        # 创建mask用于calcHist（必须是uint8，值为0或255）
        mask_uint8 = np.zeros_like(mask, dtype=np.uint8)
        mask_uint8[mask > 0] = 255
        
        # 确保mask也是连续的
        if not mask_uint8.flags['C_CONTIGUOUS']:
            mask_uint8 = np.ascontiguousarray(mask_uint8)
        
        # 分别提取每个通道，确保是连续的
        r_channel = np.ascontiguousarray(image[:, :, 0])
        g_channel = np.ascontiguousarray(image[:, :, 1])
        b_channel = np.ascontiguousarray(image[:, :, 2])
        
        # 计算每个通道的直方图
        hist_r = cv2.calcHist([r_channel], [0], mask_uint8, [self.bins], [0, 256])
        hist_g = cv2.calcHist([g_channel], [0], mask_uint8, [self.bins], [0, 256])
        hist_b = cv2.calcHist([b_channel], [0], mask_uint8, [self.bins], [0, 256])
        
        # 合并直方图
        hist = np.concatenate([hist_r.flatten(), hist_g.flatten(), hist_b.flatten()])
        
        # 归一化
        hist = hist / (np.sum(hist) + 1e-10)
        
        return hist    
    def extract_dominant_color(self, image: np.ndarray, mask: np.ndarray) -> Tuple[np.ndarray, str]:
        """
        提取主色调和颜色语义
        
        Args:
            image: RGB图像 (H, W, 3)
            mask: 二值掩码 (H, W)
            
        Returns:
            dominant_rgb: 主色调RGB值 (3,)
            color_name: 颜色语义名称
        """
        if np.sum(mask) == 0:
            return np.array([0, 0, 0]), "unknown"
        
        # 提取mask区域的像素
        masked_pixels = image[mask > 0]
        
        if len(masked_pixels) == 0:
            return np.array([0, 0, 0]), "unknown"
        
        # 计算平均颜色
        mean_color = np.mean(masked_pixels, axis=0)
        
        # 映射到颜色语义
        color_name = self._map_to_color_name(mean_color)
        
        return mean_color.astype(np.uint8), color_name
    
    def _map_to_color_name(self, rgb: np.ndarray) -> str:
        """
        将RGB值映射到颜色语义名称
        
        Args:
            rgb: RGB值 (3,)
            
        Returns:
            color_name: 颜色语义名称
        """
        r, g, b = rgb
        
        # 检查每种颜色的范围
        for color_name, (r_range, g_range, b_range) in self.color_mapping.items():
            if (r_range[0] <= r <= r_range[1] and 
                g_range[0] <= g <= g_range[1] and 
                b_range[0] <= b <= b_range[1]):
                return color_name
        
        # 如果没有匹配，返回最接近的颜色
        return self._find_closest_color(rgb)
    
    def _find_closest_color(self, rgb: np.ndarray) -> str:
        """
        找到最接近的颜色
        
        Args:
            rgb: RGB值 (3,)
            
        Returns:
            color_name: 最接近的颜色名称
        """
        r, g, b = rgb
        min_distance = float('inf')
        closest_color = "mixed"
        
        for color_name, (r_range, g_range, b_range) in self.color_mapping.items():
            # 计算到范围中心的距离
            r_center = (r_range[0] + r_range[1]) / 2
            g_center = (g_range[0] + g_range[1]) / 2
            b_center = (b_range[0] + b_range[1]) / 2
            
            distance = np.sqrt((r - r_center)**2 + (g - g_center)**2 + (b - b_center)**2)
            
            if distance < min_distance:
                min_distance = distance
                closest_color = color_name
        
        return closest_color
    
    def compute_color_similarity(self, hist1: np.ndarray, hist2: np.ndarray) -> float:
        """
        计算两个颜色直方图的相似度
        
        Args:
            hist1: 第一个直方图
            hist2: 第二个直方图
            
        Returns:
            similarity: 相似度 (0-1之间)
        """
        return cv2.compareHist(hist1.astype(np.float32), hist2.astype(np.float32), cv2.HISTCMP_CORREL)
    
    def get_color_statistics(self, image: np.ndarray, mask: np.ndarray) -> Dict:
        """
        获取颜色统计信息
        
        Args:
            image: RGB图像 (H, W, 3)
            mask: 二值掩码 (H, W)
            
        Returns:
            stats: 颜色统计信息字典
        """
        if np.sum(mask) == 0:
            return {
                'mean_color': [0, 0, 0],
                'std_color': [0, 0, 0],
                'dominant_color': [0, 0, 0],
                'color_name': "unknown",
                'histogram': np.zeros((self.bins * 3,))
            }
        
        # 提取mask区域的像素
        masked_pixels = image[mask > 0]
        
        # 计算统计量
        mean_color = np.mean(masked_pixels, axis=0)
        std_color = np.std(masked_pixels, axis=0)
        
        # 提取主色调
        dominant_color, color_name = self.extract_dominant_color(image, mask)
        
        # 计算直方图
        histogram = self.compute_color_histogram(image, mask)
        
        return {
            'mean_color': mean_color.tolist(),
            'std_color': std_color.tolist(),
            'dominant_color': dominant_color.tolist(),
            'color_name': color_name,
            'histogram': histogram
        }