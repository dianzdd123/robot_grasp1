# features/similarity_calculator.py
import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy.spatial.distance import cosine, euclidean
from scipy.stats import wasserstein_distance
import cv2

class FeatureSimilarityCalculator:
    """特征相似度计算器 - 用于Track模块的特征匹配"""
    
    def __init__(self, feature_weights: Optional[Dict[str, float]] = None):
        """
        初始化相似度计算器
        
        Args:
            feature_weights: 各类特征的权重配置
        """
        self.feature_weights = feature_weights or {
            'geometric': 0.4,     # 3D几何特征权重最高
            'appearance': 0.2,    # 颜色特征权重较低
            'shape': 0.3,         # 2D形状特征中等权重
            'spatial': 0.1        # 空间上下文辅助权重
        }
        
        # 各特征类型的相似度计算方法
        self.similarity_methods = {
            'geometric': self._calculate_geometric_similarity,
            'appearance': self._calculate_appearance_similarity,
            'shape': self._calculate_shape_similarity,
            'spatial': self._calculate_spatial_similarity
        }
    
    def calculate_overall_similarity(self, ref_features: Dict, candidate_features: Dict) -> Dict:
        """
        计算整体相似度
        
        Args:
            ref_features: 参考特征
            candidate_features: 候选特征
            
        Returns:
            similarity_result: 包含各项相似度和最终分数的字典
        """
        similarities = {}
        valid_weights_sum = 0.0
        
        # 计算各类特征的相似度
        for feature_type, weight in self.feature_weights.items():
            if feature_type in ref_features and feature_type in candidate_features:
                try:
                    similarity_method = self.similarity_methods[feature_type]
                    similarity = similarity_method(
                        ref_features[feature_type], 
                        candidate_features[feature_type]
                    )
                    similarities[feature_type] = similarity
                    valid_weights_sum += weight
                except Exception as e:
                    print(f"[SIMILARITY] {feature_type}相似度计算失败: {e}")
                    similarities[feature_type] = 0.0
            else:
                similarities[feature_type] = 0.0
        
        # 计算加权总相似度
        if valid_weights_sum > 0:
            weighted_similarity = sum(
                similarities[ft] * self.feature_weights[ft] 
                for ft in similarities.keys()
            ) / valid_weights_sum
        else:
            weighted_similarity = 0.0
        
        return {
            'overall_similarity': weighted_similarity,
            'feature_similarities': similarities,
            'confidence': self._calculate_confidence(similarities),
            'valid_features': list(similarities.keys())
        }
    
    def _calculate_geometric_similarity(self, ref_geometric: Dict, candidate_geometric: Dict) -> float:
        """计算3D几何特征相似度"""
        similarities = []
        
        # 1. FPFH特征相似度
        if 'fpfh' in ref_geometric and 'fpfh' in candidate_geometric:
            fpfh_sim = self._calculate_fpfh_similarity(
                ref_geometric['fpfh'], candidate_geometric['fpfh']
            )
            similarities.append(fpfh_sim * 0.4)  # FPFH权重40%
        
        # 2. PCA特征相似度
        if 'pca_features' in ref_geometric and 'pca_features' in candidate_geometric:
            pca_sim = self._calculate_pca_similarity(
                ref_geometric['pca_features'], candidate_geometric['pca_features']
            )
            similarities.append(pca_sim * 0.3)  # PCA权重30%
        
        # 3. 包围盒相似度
        if 'bbox_dimensions' in ref_geometric and 'bbox_dimensions' in candidate_geometric:
            bbox_sim = self._calculate_bbox_similarity(
                ref_geometric['bbox_dimensions'], candidate_geometric['bbox_dimensions']
            )
            similarities.append(bbox_sim * 0.2)  # 包围盒权重20%
        
        # 4. 3D形状上下文相似度
        if 'shape_context_3d' in ref_geometric and 'shape_context_3d' in candidate_geometric:
            context_sim = self._calculate_histogram_similarity(
                ref_geometric['shape_context_3d'], candidate_geometric['shape_context_3d']
            )
            similarities.append(context_sim * 0.1)  # 形状上下文权重10%
        
        return np.mean(similarities) if similarities else 0.0
    
    def _calculate_fpfh_similarity(self, ref_fpfh: List[float], candidate_fpfh: List[float]) -> float:
        """计算FPFH特征相似度"""
        try:
            if len(ref_fpfh) != len(candidate_fpfh):
                return 0.0
            
            ref_array = np.array(ref_fpfh)
            candidate_array = np.array(candidate_fpfh)
            
            # 使用余弦相似度，对幅度变化更鲁棒
            similarity = 1.0 - cosine(ref_array, candidate_array)
            return max(0.0, similarity)  # 确保非负
            
        except Exception:
            return 0.0
    
    def _calculate_pca_similarity(self, ref_pca: Dict, candidate_pca: Dict) -> float:
        """计算PCA特征相似度"""
        try:
            similarities = []
            
            # 形状特征相似度
            shape_features = ['linearity', 'planarity', 'sphericity', 'anisotropy']
            for feature in shape_features:
                if feature in ref_pca and feature in candidate_pca:
                    # 使用相对差异计算相似度
                    diff = abs(ref_pca[feature] - candidate_pca[feature])
                    similarity = max(0.0, 1.0 - diff)
                    similarities.append(similarity)
            
            return np.mean(similarities) if similarities else 0.0
            
        except Exception:
            return 0.0
    
    def _calculate_bbox_similarity(self, ref_bbox: List[float], candidate_bbox: List[float]) -> float:
        """计算3D包围盒相似度"""
        try:
            if len(ref_bbox) != len(candidate_bbox) or len(ref_bbox) != 3:
                return 0.0
            
            ref_array = np.array(ref_bbox)
            candidate_array = np.array(candidate_bbox)
            
            # 计算尺寸比例相似度（对绝对尺寸变化鲁棒）
            ref_ratios = ref_array / (np.sum(ref_array) + 1e-8)
            candidate_ratios = candidate_array / (np.sum(candidate_array) + 1e-8)
            
            # 使用L2距离的相似度
            distance = np.linalg.norm(ref_ratios - candidate_ratios)
            similarity = max(0.0, 1.0 - distance)
            
            return similarity
            
        except Exception:
            return 0.0
    
    def _calculate_appearance_similarity(self, ref_appearance: Dict, candidate_appearance: Dict) -> float:
        """计算外观特征相似度"""
        similarities = []
        
        # 1. 颜色直方图相似度
        if 'histogram' in ref_appearance and 'histogram' in candidate_appearance:
            hist_sim = self._calculate_histogram_similarity(
                ref_appearance['histogram'], candidate_appearance['histogram']
            )
            similarities.append(hist_sim * 0.7)  # 直方图权重70%
        
        # 2. 颜色名称匹配
        if 'color_name' in ref_appearance and 'color_name' in candidate_appearance:
            color_match = 1.0 if ref_appearance['color_name'] == candidate_appearance['color_name'] else 0.0
            similarities.append(color_match * 0.3)  # 颜色名称权重30%
        
        return np.mean(similarities) if similarities else 0.0
    
    def _calculate_histogram_similarity(self, ref_hist: List[float], candidate_hist: List[float]) -> float:
        """计算直方图相似度"""
        try:
            if len(ref_hist) != len(candidate_hist):
                return 0.0
            
            ref_array = np.array(ref_hist)
            candidate_array = np.array(candidate_hist)
            
            # 使用多种相似度度量的组合
            # 1. 巴氏系数
            bc_similarity = np.sum(np.sqrt(ref_array * candidate_array))
            
            # 2. 相关系数
            correlation = np.corrcoef(ref_array, candidate_array)[0, 1]
            correlation = 0.0 if np.isnan(correlation) else correlation
            
            # 3. 卡方距离的相似度
            chi_square = np.sum((ref_array - candidate_array) ** 2 / (ref_array + candidate_array + 1e-8))
            chi_similarity = max(0.0, 1.0 - chi_square / len(ref_hist))
            
            # 组合相似度
            combined_similarity = (bc_similarity * 0.5 + 
                                 max(0.0, correlation) * 0.3 + 
                                 chi_similarity * 0.2)
            
            return min(1.0, combined_similarity)
            
        except Exception:
            return 0.0
    
    def _calculate_shape_similarity(self, ref_shape: Dict, candidate_shape: Dict) -> float:
        """计算2D形状特征相似度"""
        similarities = []
        
        # 1. Hu矩相似度
        if 'hu_moments' in ref_shape and 'hu_moments' in candidate_shape:
            hu_sim = self._calculate_hu_moments_similarity(
                ref_shape['hu_moments'], candidate_shape['hu_moments']
            )
            similarities.append(hu_sim * 0.4)  # Hu矩权重40%
        
        # 2. 鲁棒Hu矩相似度（如果有）
        if 'hu_moments_robust' in ref_shape and 'hu_moments_robust' in candidate_shape:
            robust_hu_sim = self._calculate_hu_moments_similarity(
                ref_shape['hu_moments_robust'], candidate_shape['hu_moments_robust']
            )
            similarities.append(robust_hu_sim * 0.3)  # 鲁棒Hu矩权重30%
        
        # 3. 形状描述符相似度
        if 'shape_descriptors' in ref_shape and 'shape_descriptors' in candidate_shape:
            desc_sim = self._calculate_shape_descriptors_similarity(
                ref_shape['shape_descriptors'], candidate_shape['shape_descriptors']
            )
            similarities.append(desc_sim * 0.2)  # 形状描述符权重20%
        
        # 4. 傅里叶描述子相似度
        if 'fourier_descriptors' in ref_shape and 'fourier_descriptors' in candidate_shape:
            fourier_sim = self._calculate_fourier_similarity(
                ref_shape['fourier_descriptors'], candidate_shape['fourier_descriptors']
            )
            similarities.append(fourier_sim * 0.1)  # 傅里叶描述子权重10%
        
        return np.mean(similarities) if similarities else 0.0
    
    def _calculate_hu_moments_similarity(self, ref_hu: List[float], candidate_hu: List[float]) -> float:
        """计算Hu矩相似度"""
        try:
            if len(ref_hu) != len(candidate_hu):
                return 0.0
            
            ref_array = np.array(ref_hu)
            candidate_array = np.array(candidate_hu)
            
            # 使用对数空间的欧几里得距离
            distances = np.abs(ref_array - candidate_array)
            # 将距离转换为相似度（距离越小，相似度越高）
            similarities = np.exp(-distances)
            
            return np.mean(similarities)
            
        except Exception:
            return 0.0
    
    def _calculate_shape_descriptors_similarity(self, ref_desc: List[float], candidate_desc: List[float]) -> float:
        """计算形状描述符相似度"""
        try:
            if len(ref_desc) != len(candidate_desc):
                return 0.0
            
            ref_array = np.array(ref_desc)
            candidate_array = np.array(candidate_desc)
            
            # 计算各个描述符的相似度
            similarities = []
            for i in range(len(ref_array)):
                if ref_array[i] > 0 and candidate_array[i] > 0:
                    # 使用比例相似度
                    ratio = min(ref_array[i], candidate_array[i]) / max(ref_array[i], candidate_array[i])
                    similarities.append(ratio)
                elif ref_array[i] == 0 and candidate_array[i] == 0:
                    similarities.append(1.0)
                else:
                    similarities.append(0.0)
            
            return np.mean(similarities) if similarities else 0.0
            
        except Exception:
            return 0.0
    
    def _calculate_fourier_similarity(self, ref_fourier: List[float], candidate_fourier: List[float]) -> float:
        """计算傅里叶描述子相似度"""
        try:
            if len(ref_fourier) != len(candidate_fourier):
                return 0.0
            
            ref_array = np.array(ref_fourier)
            candidate_array = np.array(candidate_fourier)
            
            # 使用归一化的欧几里得距离
            if np.sum(ref_array) > 0 and np.sum(candidate_array) > 0:
                ref_normalized = ref_array / np.sum(ref_array)
                candidate_normalized = candidate_array / np.sum(candidate_array)
                
                distance = np.linalg.norm(ref_normalized - candidate_normalized)
                similarity = max(0.0, 1.0 - distance)
                return similarity
            else:
                return 0.0
                
        except Exception:
            return 0.0
    
    def _calculate_spatial_similarity(self, ref_spatial: Dict, candidate_spatial: Dict) -> float:
        """计算空间特征相似度"""
        similarities = []
        
        # 1. 相对位置相似度
        if 'region_position' in ref_spatial and 'region_position' in candidate_spatial:
            position_match = 1.0 if ref_spatial['region_position'] == candidate_spatial['region_position'] else 0.0
            similarities.append(position_match * 0.4)
        
        # 2. 尺寸相似度
        if 'mask_area_pixels' in ref_spatial and 'mask_area_pixels' in candidate_spatial:
            area_ratio = min(ref_spatial['mask_area_pixels'], candidate_spatial['mask_area_pixels']) / \
                        max(ref_spatial['mask_area_pixels'], candidate_spatial['mask_area_pixels'])
            similarities.append(area_ratio * 0.3)
        
        # 3. 距离相似度
        if 'distance_to_camera' in ref_spatial and 'distance_to_camera' in candidate_spatial:
            ref_dist = ref_spatial['distance_to_camera']
            candidate_dist = candidate_spatial['distance_to_camera']
            if ref_dist > 0 and candidate_dist > 0:
                dist_ratio = min(ref_dist, candidate_dist) / max(ref_dist, candidate_dist)
                similarities.append(dist_ratio * 0.3)
        
        return np.mean(similarities) if similarities else 0.0
    
    def _calculate_confidence(self, similarities: Dict[str, float]) -> float:
        """计算匹配置信度"""
        # 基于相似度分布计算置信度
        sim_values = list(similarities.values())
        if not sim_values:
            return 0.0
        
        mean_sim = np.mean(sim_values)
        std_sim = np.std(sim_values)
        
        # 高相似度且低方差 = 高置信度
        confidence = mean_sim * (1.0 - min(std_sim, 0.5))
        
        return max(0.0, min(1.0, confidence))
    
    def find_best_match(self, target_features: Dict, candidate_list: List[Dict]) -> Optional[Dict]:
        """
        在候选列表中找到最佳匹配
        
        Args:
            target_features: 目标特征
            candidate_list: 候选特征列表
            
        Returns:
            best_match: 最佳匹配结果，包含候选索引和相似度信息
        """
        if not candidate_list:
            return None
        
        best_match = None
        best_similarity = 0.0
        
        for i, candidate in enumerate(candidate_list):
            if 'features' in candidate:
                similarity_result = self.calculate_overall_similarity(
                    target_features, candidate['features']
                )
                
                overall_sim = similarity_result['overall_similarity']
                
                if overall_sim > best_similarity:
                    best_similarity = overall_sim
                    best_match = {
                        'candidate_index': i,
                        'candidate_data': candidate,
                        'similarity_result': similarity_result
                    }
        
        return best_match
    
    def update_weights(self, new_weights: Dict[str, float]):
        """更新特征权重"""
        self.feature_weights.update(new_weights)
        
        # 归一化权重
        total_weight = sum(self.feature_weights.values())
        if total_weight > 0:
            self.feature_weights = {
                k: v / total_weight for k, v in self.feature_weights.items()
            }