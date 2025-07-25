#!/usr/bin/env python3
"""
Improved ID Matcher - 专注目标匹配的改进版本
增加详细调试输出和匹配结果保存功能
"""

import numpy as np
import time
from typing import List, Dict, Any, Optional, Tuple
import json
import os
import cv2
from ..utils.config import TrackingConfig, TrackingMode, DetectionResult


class ImprovedIDMatcher:
    """改进的ID匹配器 - 专注于目标对象匹配和详细调试"""
    
    def __init__(self, config: TrackingConfig, logger=None):
        """
        初始化ID匹配器
        
        Args:
            config: 追踪配置
            logger: 日志记录器
        """
        self.config = config
        self.logger = logger
        
        # 特征匹配配置 - 确保使用配置中的值
        self.feature_config = config.feature_config
        self.match_threshold = self.feature_config.get('match_threshold', 0.3)  # 使用配置值
        self.feature_weights = self.feature_config.get('weights', {
            'hu_moments': 0.6,
            'color_histogram': 0.8,
            'spatial_continuity': 0.2
        })
        
        # 参考特征数据库
        self.reference_features_db = {}
        
        # 轻量级追踪配置
        self.lightweight_continuity_frames = config.get_lightweight_continuity_frames()
        
        # 追踪历史
        self.tracking_history = {}
        self.class_detection_history = {}
        self.spatial_continuity_threshold = config.detection_params.get('spatial_continuity_threshold', 100.0)
        
        # 统计信息
        self.match_statistics = {
            'total_matches': 0,
            'successful_matches': 0,
            'failed_matches': 0,
            'lightweight_matches': 0
        }
        
        # 调试输出保存
        self.debug_output_dir = None
        self.match_debug_history = []
        
        self._log_info("🔍 改进版ID匹配器初始化完成")
        self._log_info(f"   匹配阈值: {self.match_threshold}")
        self._log_info(f"   特征权重: {self.feature_weights}")
    
    def set_debug_output_dir(self, output_dir: str):
        """设置调试输出目录"""
        self.debug_output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self._log_info(f"📁 调试输出目录: {output_dir}")
    
    def load_reference_features(self, scan_directory: str) -> bool:
        """加载参考特征数据库 - 支持mask数据加载"""
        try:
            detection_results_dir = os.path.join(scan_directory, "detection_results")
            
            if not os.path.exists(detection_results_dir):
                self._log_error(f"❌ detection_results目录不存在: {detection_results_dir}")
                return False
            
            # 查找JSON文件
            json_files = []
            for file in os.listdir(detection_results_dir):
                if file.endswith('.json') and ('detection_results' in file or 'results' in file):
                    json_files.append(file)
            
            if not json_files:
                json_files = [f for f in os.listdir(detection_results_dir) if f.endswith('.json')]
            
            if not json_files:
                self._log_error(f"❌ 未找到任何JSON文件: {detection_results_dir}")
                return False
            
            json_file = sorted(json_files)[-1]
            json_path = os.path.join(detection_results_dir, json_file)
            
            self._log_info(f"📄 使用检测结果文件: {json_file}")
            
            with open(json_path, 'r', encoding='utf-8') as f:
                detection_data = json.load(f)
            
            # 构建参考特征数据库
            self.reference_features_db = {}
            objects = detection_data.get('objects', [])
            
            if not objects:
                self._log_error(f"❌ 检测结果文件中没有对象数据")
                return False
            
            for obj in objects:
                object_id = obj.get('object_id')
                if object_id:
                    features = obj.get('features', {})
                    
                    # 🆕 加载原始mask数据
                    if ('shape' in features and 'raw_mask_file' in features['shape']):
                        mask_file_path = os.path.join(detection_results_dir, 
                                                    features['shape']['raw_mask_file'])
                        
                        if os.path.exists(mask_file_path):
                            try:
                                raw_mask = np.load(mask_file_path)
                                features['shape']['raw_mask'] = raw_mask
                                self._log_debug(f"✅ 为 {object_id} 加载了原始mask: {raw_mask.shape}")
                            except Exception as e:
                                self._log_warn(f"⚠️ 加载 {object_id} 的mask失败: {e}")
                    
                    self.reference_features_db[object_id] = {
                        'class_id': obj.get('class_id'),
                        'class_name': obj.get('class_name'),
                        'features': features,
                        'description': obj.get('description', ''),
                        'confidence': obj.get('confidence', 0.0)
                    }
            
            self._log_info(f"✅ 成功加载 {len(self.reference_features_db)} 个参考特征")
            
            # 统计改进特征
            improved_count = 0
            for obj_id, obj_data in self.reference_features_db.items():
                features = obj_data['features']
                if ('shape' in features and 
                    'raw_mask' in features['shape'] and
                    'hu_moments_robust' in features['shape']):
                    improved_count += 1
            
            self._log_info(f"📊 其中 {improved_count} 个对象包含改进特征")
            
            # 保存参考数据库的详细信息用于调试
            if self.debug_output_dir:
                self._save_reference_db_debug()
            
            return True
            
        except Exception as e:
            self._log_error(f"❌ 加载参考特征失败: {e}")
            import traceback
            self._log_error(f"详细错误: {traceback.format_exc()}")
            return False
    
    def _save_reference_db_debug(self):
        """保存参考数据库调试信息"""
        try:
            debug_info = {
                'timestamp': time.time(),
                'total_objects': len(self.reference_features_db),
                'objects': {}
            }
            
            for obj_id, obj_data in self.reference_features_db.items():
                features = obj_data['features']
                debug_info['objects'][obj_id] = {
                    'class_id': obj_data['class_id'],
                    'class_name': obj_data['class_name'],
                    'feature_types': list(features.keys()),
                    'color_features': {
                        'has_histogram': 'color' in features and 'histogram' in features.get('color', {}),
                        'histogram_length': len(features.get('color', {}).get('histogram', []))
                    },
                    'shape_features': {
                        'has_hu_moments': 'shape' in features and 'hu_moments' in features.get('shape', {}),
                        'hu_moments_count': len(features.get('shape', {}).get('hu_moments', []))
                    }
                }
            
            debug_file = os.path.join(self.debug_output_dir, 'reference_db_debug.json')
            with open(debug_file, 'w', encoding='utf-8') as f:
                json.dump(debug_info, f, indent=2, ensure_ascii=False)
            
            self._log_info(f"💾 参考数据库调试信息已保存: {debug_file}")
            
        except Exception as e:
            self._log_error(f"❌ 保存参考数据库调试信息失败: {e}")
    
    def match_target_only(self, detection_results: List[DetectionResult], 
                         target_class_id: int, target_object_id: str) -> Optional[DetectionResult]:
        """
        专门匹配目标対象 - 优化版本，只关注目标
        
        Args:
            detection_results: 检测结果列表
            target_class_id: 目标类别ID
            target_object_id: 目标对象ID
        
        Returns:
            匹配的目标检测结果，如果没找到则返回None
        """
        try:
            if not detection_results:
                self._log_debug("❌ 没有检测结果需要匹配")
                return None
            
            # 只筛选目标类别的检测结果
            target_class_detections = [d for d in detection_results if d.class_id == target_class_id]
            
            if not target_class_detections:
                self._log_debug(f"❌ 未找到目标类别 {target_class_id} 的检测结果")
                return None
            
            self._log_info(f"🎯 开始目标匹配: 找到 {len(target_class_detections)} 个目标类别对象")
            self._log_info(f"   目标ID: {target_object_id}")
            self._log_info(f"   目标类别: {target_class_id}")
            self._log_info(f"   匹配阈值: {self.match_threshold}")
            
            # 检查目标是否在参考数据库中
            if target_object_id not in self.reference_features_db:
                self._log_error(f"❌ 目标 {target_object_id} 不在参考数据库中")
                return None
            
            # 获取目标参考特征
            target_ref_data = self.reference_features_db[target_object_id]
            
            # 详细的匹配过程
            best_match = None
            best_score = 0.0
            match_details = []
            
            for i, detection in enumerate(target_class_detections):
                self._log_info(f"\n🔍 匹配候选对象 {i+1}/{len(target_class_detections)}:")
                
                # 计算详细的特征相似度
                similarity_details = self._calculate_detailed_similarity(
                    detection.features, target_ref_data['features']
                )
                
                # 空间连续性奖励
                spatial_bonus = self._calculate_spatial_bonus(detection, target_object_id)
                
                # 综合评分
                total_score = similarity_details['total_score'] * 0.8 + spatial_bonus * 0.2
                
                match_detail = {
                    'detection_index': i,
                    'detection_id': getattr(detection, 'object_id', f'temp_{i}'),
                    'similarity_details': similarity_details,
                    'spatial_bonus': spatial_bonus,
                    'total_score': total_score,
                    'above_threshold': total_score > self.match_threshold
                }
                
                match_details.append(match_detail)
                
                # 记录详细信息
                self._log_info(f"   检测对象临时ID: {match_detail['detection_id']}")
                self._log_info(f"   Hu矩相似度: {similarity_details['hu_similarity']:.4f} (权重: {self.feature_weights.get('hu_moments', 0)})")
                self._log_info(f"   颜色相似度: {similarity_details['color_similarity']:.4f} (权重: {self.feature_weights.get('color_histogram', 0)})")
                self._log_info(f"   几何相似度: {similarity_details['geometry_similarity']:.4f}")
                self._log_info(f"   特征总分: {similarity_details['total_score']:.4f}")
                self._log_info(f"   空间奖励: {spatial_bonus:.4f}")
                self._log_info(f"   综合得分: {total_score:.4f}")
                self._log_info(f"   超过阈值: {'✅' if total_score > self.match_threshold else '❌'} (阈值: {self.match_threshold})")
                
                if total_score > best_score:
                    best_score = total_score
                    best_match = detection
                    self._log_info(f"   🎯 新的最佳匹配!")
            
            # 保存匹配调试信息
            debug_info = {
                'timestamp': time.time(),
                'target_object_id': target_object_id,
                'target_class_id': target_class_id,
                'match_threshold': self.match_threshold,
                'candidate_count': len(target_class_detections),
                'match_details': match_details,
                'best_match_found': best_match is not None,
                'best_score': best_score
            }
            
            self.match_debug_history.append(debug_info)
            
            if self.debug_output_dir:
                self._save_match_debug(debug_info)
            
            # 处理匹配结果
            if best_match and best_score > self.match_threshold:
                best_match.object_id = target_object_id
                best_match.match_confidence = best_score
                best_match.match_method = "detailed_feature_matching"
                
                # 更新追踪历史
                self._update_single_object_tracking_history(best_match)
                
                self._log_info(f"\n✅ 成功匹配目标: {target_object_id}")
                self._log_info(f"   最终置信度: {best_score:.4f}")
                self._log_info(f"   匹配方法: {best_match.match_method}")
                
                return best_match
            else:
                self._log_info(f"\n❌ 未能匹配目标: {target_object_id}")
                if best_score > 0:
                    self._log_info(f"   最高得分: {best_score:.4f}")
                    self._log_info(f"   低于阈值: {self.match_threshold}")
                else:
                    self._log_info(f"   没有有效的特征匹配")
                
                return None
                
        except Exception as e:
            self._log_error(f"❌ 目标匹配失败: {e}")
            import traceback
            self._log_error(f"详细错误: {traceback.format_exc()}")
            return None
        
    def _improved_hu_moments_similarity_from_masks(self, mask1, mask2, mode='adaptive'):
        """使用原始mask的改进Hu矩相似度计算"""
        try:
            if mask1.dtype != bool:
                mask1 = mask1 > 0.5
            if mask2.dtype != bool:
                mask2 = mask2 > 0.5
            
            if mode == 'adaptive':
                return self._adaptive_hu_similarity_from_masks(mask1, mask2)
            else:
                # 简化的鲁棒计算
                features1 = self._extract_robust_features_from_mask(mask1)
                features2 = self._extract_robust_features_from_mask(mask2)
                return self._compute_robust_similarity(features1, features2)
                
        except Exception as e:
            self._log_error(f"❌ mask-based Hu矩计算失败: {e}")
            return 0.0    

    def _adaptive_hu_similarity_from_masks(self, mask1, mask2, occlusion_threshold=0.7):
        """自适应Hu矩相似度计算"""
        try:
            # 估算遮挡程度
            area1 = np.sum(mask1)
            area2 = np.sum(mask2)
            area_ratio = min(area1, area2) / (max(area1, area2) + 1e-8)
            
            # 根据遮挡程度调整权重
            if area_ratio < occlusion_threshold:
                # 存在遮挡，使用更宽松的计算
                weights = {'hu_moments': 0.2, 'shape_descriptors': 0.5, 'fourier_descriptors': 0.3}
            else:
                weights = {'hu_moments': 0.4, 'shape_descriptors': 0.3, 'fourier_descriptors': 0.3}
            
            features1 = self._extract_robust_features_from_mask(mask1)
            features2 = self._extract_robust_features_from_mask(mask2)
            
            return self._compute_robust_similarity(features1, features2, weights)
            
        except Exception as e:
            self._log_error(f"❌ 自适应Hu矩计算失败: {e}")
            return 0.0

    def _extract_robust_features_from_mask(self, mask):
        """从mask提取鲁棒特征"""
        try:
            # 与detection_pipeline中的方法保持一致
            if mask.dtype == bool:
                mask_uint8 = mask.astype(np.uint8) * 255
            else:
                mask_uint8 = (mask * 255).astype(np.uint8)
            
            # 形态学处理
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
            mask_smooth = cv2.morphologyEx(mask_uint8, cv2.MORPH_CLOSE, kernel)
            mask_smooth = cv2.morphologyEx(mask_smooth, cv2.MORPH_OPEN, kernel)
            
            features = {}
            
            # Hu矩
            moments = cv2.moments(mask_smooth)
            if moments['m00'] > 0:
                hu_moments = cv2.HuMoments(moments).flatten()
                hu_log = -np.sign(hu_moments) * np.log10(np.abs(hu_moments) + 1e-8)
                features['hu_moments'] = hu_log
            else:
                features['hu_moments'] = np.zeros(7)
            
            # 轮廓特征
            contours, _ = cv2.findContours(mask_smooth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                contour_area = cv2.contourArea(largest_contour)
                hull_area = cv2.contourArea(cv2.convexHull(largest_contour))
                solidity = contour_area / hull_area if hull_area > 0 else 0
                
                perimeter = cv2.arcLength(largest_contour, True)
                circularity = 4 * np.pi * contour_area / (perimeter * perimeter) if perimeter > 0 else 0
                
                rect = cv2.minAreaRect(largest_contour)
                width, height = rect[1]
                aspect_ratio = max(width, height) / (min(width, height) + 1e-8)
                
                features['shape_descriptors'] = np.array([solidity, circularity, aspect_ratio, 1.0])
            else:
                features['shape_descriptors'] = np.zeros(4)
            
            return features
            
        except Exception as e:
            self._log_error(f"❌ 鲁棒特征提取失败: {e}")
            return {'hu_moments': np.zeros(7), 'shape_descriptors': np.zeros(4)}

    def _compute_robust_similarity(self, features1, features2, weights=None):
        """计算鲁棒相似度"""
        try:
            if weights is None:
                weights = {'hu_moments': 0.4, 'shape_descriptors': 0.6}
            
            total_similarity = 0.0
            weight_sum = 0.0
            
            # Hu矩相似度
            if 'hu_moments' in weights:
                hu1, hu2 = features1['hu_moments'], features2['hu_moments']
                # 使用前4个Hu矩（更稳定）
                hu_dist = np.sum(np.abs(hu1[:4] - hu2[:4]))
                hu_sim = np.exp(-hu_dist * 0.5)
                total_similarity += weights['hu_moments'] * hu_sim
                weight_sum += weights['hu_moments']
            
            # 形状描述子相似度
            if 'shape_descriptors' in weights:
                shape1, shape2 = features1['shape_descriptors'], features2['shape_descriptors']
                shape_dist = np.sum(np.abs(shape1 - shape2))
                shape_sim = np.exp(-shape_dist)
                total_similarity += weights['shape_descriptors'] * shape_sim
                weight_sum += weights['shape_descriptors']
            
            return total_similarity / weight_sum if weight_sum > 0 else 0.0
            
        except Exception as e:
            self._log_error(f"❌ 鲁棒相似度计算失败: {e}")
            return 0.0
                
    def _calculate_detailed_similarity(self, detected_features: Dict[str, Any], 
                                    reference_features: Dict[str, Any]) -> Dict[str, float]:
        """计算详细的特征相似度 - 集成改进的mask-based计算"""
        try:
            results = {
                'hu_similarity': 0.0,
                'color_similarity': 0.0,
                'geometry_similarity': 0.0,
                'total_score': 0.0,
                'valid_features': [],
                'computation_method': 'unknown'
            }
            
            total_score = 0.0
            valid_weight_sum = 0.0
            # 在方法开始处添加
            self._log_info(f"🔍 调试特征数据:")
            self._log_info(f"  检测特征keys: {list(detected_features.keys())}")
            self._log_info(f"  参考特征keys: {list(reference_features.keys())}")

            if 'shape' in detected_features:
                shape_keys = list(detected_features['shape'].keys())
                self._log_info(f"  检测shape keys: {shape_keys}")
                
            if 'color' in detected_features:
                color_keys = list(detected_features['color'].keys())
                hist_len = len(detected_features['color'].get('histogram', []))
                self._log_info(f"  检测color keys: {color_keys}, histogram长度: {hist_len}")
            # 1. 改进的Hu矩相似度计算
            hu_weight = self.feature_weights.get('hu_moments', 0.3)
            if hu_weight > 0:
                # 🆕 首先尝试使用原始mask数据进行改进计算
                detected_mask = detected_features.get('shape', {}).get('raw_mask', None)
                reference_mask = reference_features.get('shape', {}).get('raw_mask', None)
                
                if detected_mask is not None and reference_mask is not None:
                    # 使用改进的mask-based Hu矩计算
                    hu_similarity = self._improved_hu_moments_similarity_from_masks(
                        detected_mask, reference_mask, mode='adaptive'
                    )
                    results['computation_method'] = 'improved_mask_based'
                    self._log_debug(f"      使用改进mask-based Hu计算: {hu_similarity:.4f}")
                    
                else:
                    # Fallback到传统Hu矩比较
                    detected_hu = detected_features.get('shape', {}).get('hu_moments', [])
                    reference_hu = reference_features.get('shape', {}).get('hu_moments', [])
                    
                    if detected_hu and reference_hu:
                        hu_similarity = self._compare_hu_moments_traditional(detected_hu, reference_hu)
                        results['computation_method'] = 'traditional_hu_array'
                        self._log_debug(f"      使用传统Hu数组计算: {hu_similarity:.4f}")
                    else:
                        hu_similarity = 0.0
                        results['computation_method'] = 'hu_unavailable'
                        self._log_debug(f"      Hu矩数据不可用")
                
                if hu_similarity > 0:
                    results['hu_similarity'] = hu_similarity
                    results['valid_features'].append('hu_moments')
                    
                    weighted_hu = hu_weight * hu_similarity
                    total_score += weighted_hu
                    valid_weight_sum += hu_weight
            
            # 2. 改进的颜色直方图相似度
            color_weight = self.feature_weights.get('color_histogram', 0.7)
            if color_weight > 0:
                detected_hist = detected_features.get('color', {}).get('histogram', [])
                reference_hist = reference_features.get('color', {}).get('histogram', [])
                
                if detected_hist and reference_hist:
                    color_similarity = self._color_histogram_similarity_improved(detected_hist, reference_hist)
                    results['color_similarity'] = color_similarity
                    results['valid_features'].append('color_histogram')
                    
                    weighted_color = color_weight * color_similarity
                    total_score += weighted_color
                    valid_weight_sum += color_weight
                    
                    self._log_debug(f"      改进颜色计算: {color_similarity:.4f}")
            
            # 3. 几何形状相似度（使用鲁棒特征或传统特征）
            geometry_weight = 0.2
            
            # 优先使用鲁棒几何特征
            detected_shape_desc = detected_features.get('shape', {}).get('shape_descriptors', [])
            reference_shape_desc = reference_features.get('shape', {}).get('shape_descriptors', [])
            
            if detected_shape_desc and reference_shape_desc:
                geometry_similarity = self._compare_shape_descriptors_robust(detected_shape_desc, reference_shape_desc)
                results['geometry_similarity'] = geometry_similarity
                results['valid_features'].append('robust_geometry')
                
                weighted_geometry = geometry_weight * geometry_similarity
                total_score += weighted_geometry
                valid_weight_sum += geometry_weight
                
                self._log_debug(f"      鲁棒几何计算: {geometry_similarity:.4f}")
            else:
                # Fallback到传统几何特征
                detected_shape = detected_features.get('shape', {})
                reference_shape = reference_features.get('shape', {})
                geometry_similarity = self._compare_geometry_detailed(detected_shape, reference_shape)
                results['geometry_similarity'] = geometry_similarity
                
                if geometry_similarity > 0:
                    results['valid_features'].append('traditional_geometry')
                    weighted_geometry = geometry_weight * geometry_similarity
                    total_score += weighted_geometry
                    valid_weight_sum += geometry_weight
            
            # 归一化总分
            if valid_weight_sum > 0:
                results['total_score'] = total_score / valid_weight_sum
            else:
                results['total_score'] = 0.0
            
            self._log_debug(f"      最终计算: 方法={results['computation_method']}, "
                        f"权重={valid_weight_sum:.2f}, 总分={results['total_score']:.4f}")
            
            return results
            
        except Exception as e:
            self._log_error(f"❌ 改进相似度计算失败: {e}")
            return {
                'hu_similarity': 0.0,
                'color_similarity': 0.0,
                'geometry_similarity': 0.0,
                'total_score': 0.0,
                'valid_features': [],
                'computation_method': 'error',
                'error': str(e)
            }
        
    def _compare_shape_descriptors_robust(self, desc1, desc2):
        """比较鲁棒形状描述子"""
        try:
            if len(desc1) != len(desc2):
                return 0.0
            
            d1, d2 = np.array(desc1), np.array(desc2)
            similarities = []
            
            for i in range(len(d1)):
                if d1[i] > 0 and d2[i] > 0:
                    ratio = min(d1[i], d2[i]) / max(d1[i], d2[i])
                    similarities.append(ratio)
            
            return np.mean(similarities) if similarities else 0.0
            
        except Exception as e:
            self._log_error(f"❌ 鲁棒形状描述子比较失败: {e}")
            return 0.0

    def _compare_hu_moments_traditional(self, hu1, hu2):
        """传统Hu矩比较"""
        try:
            if not hu1 or not hu2 or len(hu1) != len(hu2):
                return 0.0
            
            h1 = np.array(hu1, dtype=np.float64)
            h2 = np.array(hu2, dtype=np.float64)
            
            # 使用前4个Hu矩
            dist = np.sum(np.abs(h1[:4] - h2[:4]))
            similarity = np.exp(-dist * 0.5)
            
            return similarity
            
        except Exception as e:
            self._log_error(f"❌ 传统Hu矩比较失败: {e}")
            return 0.0

    def _color_histogram_similarity_improved(self, hist1, hist2):
        """改进的颜色直方图相似度计算"""
        try:
            if not hist1 or not hist2 or len(hist1) != len(hist2):
                return 0.0
            
            h1 = np.array(hist1, dtype=np.float64)
            h2 = np.array(hist2, dtype=np.float64)
            
            # 归一化
            h1_sum, h2_sum = np.sum(h1), np.sum(h2)
            if h1_sum <= 0 or h2_sum <= 0:
                return 0.0
            
            h1_norm = h1 / h1_sum
            h2_norm = h2 / h2_sum
            
            # 巴氏距离
            bhattacharyya = np.sum(np.sqrt(h1_norm * h2_norm))
            
            # 相关系数
            correlation = np.corrcoef(h1_norm, h2_norm)[0, 1]
            if np.isnan(correlation):
                correlation = 0.0
            
            # 卡方距离
            chi_square_dist = np.sum((h1_norm - h2_norm) ** 2 / (h1_norm + h2_norm + 1e-10))
            chi_square_similarity = max(0, 1 - chi_square_dist / 2.0)
            
            # 综合相似度
            similarity = (bhattacharyya * 0.5 + max(0, correlation) * 0.3 + chi_square_similarity * 0.2)
            return max(0, min(1, similarity))
            
        except Exception as e:
            self._log_error(f"❌ 改进颜色直方图计算失败: {e}")
            return 0.0    
    def _compare_hu_moments_detailed(self, hu1: List[float], hu2: List[float]) -> float:
        """详细比较Hu矩"""
        try:
            if not hu1 or not hu2:
                self._log_debug(f"        Hu矩数据为空: hu1={bool(hu1)}, hu2={bool(hu2)}")
                return 0.0
            
            if len(hu1) != len(hu2):
                self._log_debug(f"        Hu矩长度不匹配: {len(hu1)} vs {len(hu2)}")
                return 0.0
            
            # 转换为numpy数组，处理可能的inf值
            h1 = np.array(hu1, dtype=np.float64)
            h2 = np.array(hu2, dtype=np.float64)
            
            # 移除无穷大值
            valid_mask = np.isfinite(h1) & np.isfinite(h2)
            if not np.any(valid_mask):
                self._log_debug(f"        没有有效的Hu矩值")
                return 0.0
            
            h1_valid = h1[valid_mask]
            h2_valid = h2[valid_mask]
            
            # 使用修正的距离计算
            # 对于Hu矩，通常使用对数空间的距离
            h1_log = np.sign(h1_valid) * np.log10(np.abs(h1_valid) + 1e-10)
            h2_log = np.sign(h2_valid) * np.log10(np.abs(h2_valid) + 1e-10)
            
            # 计算欧氏距离
            distance = np.linalg.norm(h1_log - h2_log)
            
            # 转换为相似度 (调整归一化因子)
            similarity = max(0, 1 - distance / 5.0)  # 调整归一化因子
            
            self._log_debug(f"        Hu矩计算: 有效值={np.sum(valid_mask)}/{len(hu1)}, 距离={distance:.4f}, 相似度={similarity:.4f}")
            
            return similarity
            
        except Exception as e:
            self._log_error(f"❌ 详细比较Hu矩失败: {e}")
            return 0.0
    
    def _compare_color_histograms_detailed(self, hist1: List[float], hist2: List[float]) -> float:
        """详细比较颜色直方图"""
        try:
            if not hist1 or not hist2:
                self._log_debug(f"        颜色直方图数据为空: hist1={bool(hist1)}, hist2={bool(hist2)}")
                return 0.0
            
            if len(hist1) != len(hist2):
                self._log_debug(f"        颜色直方图长度不匹配: {len(hist1)} vs {len(hist2)}")
                return 0.0
            
            h1 = np.array(hist1, dtype=np.float64)
            h2 = np.array(hist2, dtype=np.float64)
            
            # 归一化
            h1_sum = np.sum(h1)
            h2_sum = np.sum(h2)
            
            if h1_sum <= 0 or h2_sum <= 0:
                self._log_debug(f"        颜色直方图归一化失败: sum1={h1_sum}, sum2={h2_sum}")
                return 0.0
            
            h1_norm = h1 / h1_sum
            h2_norm = h2 / h2_sum
            
            # 使用多种相似度度量
            # 1. 巴氏距离
            bhattacharyya = np.sum(np.sqrt(h1_norm * h2_norm))
            
            # 2. 相关系数
            correlation = np.corrcoef(h1_norm, h2_norm)[0, 1]
            if np.isnan(correlation):
                correlation = 0.0
            
            # 3. 卡方距离
            chi_square_dist = np.sum((h1_norm - h2_norm) ** 2 / (h1_norm + h2_norm + 1e-10))
            chi_square_similarity = max(0, 1 - chi_square_dist / 2.0)
            
            # 综合相似度
            similarity = (bhattacharyya * 0.5 + 
                         max(0, correlation) * 0.3 + 
                         chi_square_similarity * 0.2)
            
            self._log_debug(f"        颜色计算: Bhatta={bhattacharyya:.4f}, Corr={correlation:.4f}, ChiSq={chi_square_similarity:.4f}, 综合={similarity:.4f}")
            
            return max(0, min(1, similarity))
            
        except Exception as e:
            self._log_error(f"❌ 详细比较颜色直方图失败: {e}")
            return 0.0
    
    def _compare_geometry_detailed(self, shape1: Dict[str, Any], shape2: Dict[str, Any]) -> float:
        """详细比较几何特征"""
        try:
            features = ['area', 'aspect_ratio', 'circularity', 'solidity']
            similarities = []
            details = {}
            
            for feature in features:
                val1 = shape1.get(feature, 0)
                val2 = shape2.get(feature, 0)
                
                if val1 > 0 and val2 > 0:
                    # 计算相对相似度
                    ratio = min(val1, val2) / max(val1, val2)
                    similarities.append(ratio)
                    details[feature] = {'val1': val1, 'val2': val2, 'similarity': ratio}
                else:
                    details[feature] = {'val1': val1, 'val2': val2, 'similarity': 0.0}
            
            if similarities:
                overall_similarity = np.mean(similarities)
                self._log_debug(f"        几何特征详情: {details}")
                return overall_similarity
            else:
                self._log_debug(f"        没有有效的几何特征")
                return 0.0
                
        except Exception as e:
            self._log_error(f"❌ 详细比较几何特征失败: {e}")
            return 0.0
    
    def _calculate_spatial_bonus(self, detection: DetectionResult, ref_id: str) -> float:
        """计算空间连续性奖励"""
        try:
            if ref_id not in self.tracking_history:
                return 0.0
            
            history = self.tracking_history[ref_id]
            if not history:
                return 0.0
            
            last_position = history[-1]
            current_position = detection.centroid_2d
            
            distance = np.sqrt(
                (current_position[0] - last_position[0])**2 + 
                (current_position[1] - last_position[1])**2
            )
            
            max_distance = self.spatial_continuity_threshold
            bonus = max(0, 1 - distance / max_distance)
            
            self._log_debug(f"        空间奖励: 距离={distance:.1f}px, 阈值={max_distance}px, 奖励={bonus:.4f}")
            
            return bonus
            
        except Exception as e:
            self._log_error(f"❌ 计算空间奖励失败: {e}")
            return 0.0
    
    def _update_single_object_tracking_history(self, detection: DetectionResult):
        """更新单个对象的追踪历史"""
        try:
            object_id = detection.object_id
            position = detection.centroid_2d
            
            if object_id not in self.tracking_history:
                self.tracking_history[object_id] = []
            
            self.tracking_history[object_id].append(position)
            
            # 保持历史长度
            max_history = 50
            if len(self.tracking_history[object_id]) > max_history:
                self.tracking_history[object_id] = self.tracking_history[object_id][-max_history:]
                
        except Exception as e:
            self._log_error(f"❌ 更新追踪历史失败: {e}")
    
    def _save_match_debug(self, debug_info: Dict[str, Any]):
        """保存匹配调试信息"""
        try:
            timestamp = int(time.time())
            debug_file = os.path.join(self.debug_output_dir, f'match_debug_{timestamp}.json')
            
            with open(debug_file, 'w', encoding='utf-8') as f:
                json.dump(debug_info, f, indent=2, ensure_ascii=False)
            
            # 同时保存最新的调试信息
            latest_file = os.path.join(self.debug_output_dir, 'latest_match_debug.json')
            with open(latest_file, 'w', encoding='utf-8') as f:
                json.dump(debug_info, f, indent=2, ensure_ascii=False)
            
            self._log_debug(f"💾 匹配调试信息已保存: {debug_file}")
            
        except Exception as e:
            self._log_error(f"❌ 保存匹配调试信息失败: {e}")
    
    def save_all_debug_history(self):
        """保存所有调试历史"""
        try:
            if not self.debug_output_dir:
                return
            
            history_file = os.path.join(self.debug_output_dir, 'match_history_complete.json')
            
            complete_history = {
                'timestamp': time.time(),
                'total_matches': len(self.match_debug_history),
                'config': {
                    'match_threshold': self.match_threshold,
                    'feature_weights': self.feature_weights
                },
                'match_history': self.match_debug_history
            }
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(complete_history, f, indent=2, ensure_ascii=False)
            
            self._log_info(f"💾 完整调试历史已保存: {history_file}")
            
        except Exception as e:
            self._log_error(f"❌ 保存完整调试历史失败: {e}")
    
    def get_match_statistics(self) -> Dict[str, Any]:
        """获取匹配统计信息"""
        total_attempts = len(self.match_debug_history)
        successful_matches = sum(1 for match in self.match_debug_history if match['best_match_found'])
        
        if total_attempts == 0:
            return {
                'total_attempts': 0,
                'successful_matches': 0,
                'failed_matches': 0,  # 添加这个
                'success_rate': 0.0,
                'average_best_score': 0.0,
                'feature_db_size': len(self.reference_features_db),
                'tracking_objects': len(self.tracking_history),
                'match_threshold': self.match_threshold,
                'feature_weights': self.feature_weights
            }
        
        # 计算平均最佳得分
        total_best_score = sum(match['best_score'] for match in self.match_debug_history)
        average_best_score = total_best_score / total_attempts
        
        return {
            'total_attempts': total_attempts,
            'successful_matches': successful_matches,
            'failed_matches': total_attempts - successful_matches,  # 添加这个
            'success_rate': successful_matches / total_attempts,
            'average_best_score': average_best_score,
            'feature_db_size': len(self.reference_features_db),
            'tracking_objects': len(self.tracking_history),
            'match_threshold': self.match_threshold,
            'feature_weights': self.feature_weights
        }
    
    def print_detailed_status(self):
        """打印详细状态信息"""
        stats = self.get_match_statistics()
        
        print("\n" + "="*60)
        print("🔍 改进版ID匹配器状态报告")
        print("="*60)
        print(f"📚 参考特征数据库: {stats['feature_db_size']} 个对象")
        print(f"🎯 匹配尝试次数: {stats['total_attempts']}")
        print(f"✅ 成功匹配: {stats['successful_matches']}")
        print(f"❌ 失败匹配: {stats['failed_matches']}")
        print(f"📈 成功率: {stats['success_rate']:.2%}")
        print(f"📊 平均最佳得分: {stats['average_best_score']:.4f}")
        print(f"🔧 匹配阈值: {stats['match_threshold']}")
        print(f"⚖️ 特征权重:")
        for feature, weight in stats['feature_weights'].items():
            print(f"   - {feature}: {weight}")
        print(f"🎯 追踪对象数: {stats['tracking_objects']}")
        if self.debug_output_dir:
            print(f"📁 调试输出目录: {self.debug_output_dir}")
        print("="*60)
    
    # 兼容原有接口的方法
    def match_detections(self, detection_results: List[DetectionResult], 
                        target_class_id: int, target_object_id: str,
                        current_mode: TrackingMode = TrackingMode.FULL_MATCHING) -> List[DetectionResult]:
        """
        兼容原有接口的匹配方法 - 但现在专注于目标匹配
        
        Args:
            detection_results: 检测结果列表
            target_class_id: 目标类别ID
            target_object_id: 目标对象ID
            current_mode: 当前追踪模式（暂未使用）
        
        Returns:
            处理后的检测结果列表
        """
        try:
            # 使用新的目标专用匹配方法
            target_match = self.match_target_only(detection_results, target_class_id, target_object_id)
            
            # 为了兼容原有接口，返回所有检测结果，但只有目标被正确匹配
            result_list = []
            for detection in detection_results:
                if (target_match and 
                    detection.centroid_2d[0] == target_match.centroid_2d[0] and 
                    detection.centroid_2d[1] == target_match.centroid_2d[1]):
                    # 这是匹配的目标对象
                    result_list.append(target_match)
                else:
                    # 其他对象保持原样
                    detection.match_confidence = 0.0
                    detection.match_method = "not_target"
                    result_list.append(detection)
            
            return result_list
            
        except Exception as e:
            self._log_error(f"❌ 兼容匹配接口失败: {e}")
            return detection_results
    
    def get_target_detection(self, detection_results: List[DetectionResult], 
                           target_object_id: str) -> Optional[DetectionResult]:
        """
        从检测结果中获取目标对象 - 改进版本
        
        Args:
            detection_results: 检测结果列表
            target_object_id: 目标对象ID
        
        Returns:
            目标检测结果，如果未找到则返回None
        """
        try:
            self._log_debug(f"🎯 查找目标: {target_object_id}, 匹配阈值: {self.match_threshold}")
            
            # 详细记录所有检测结果
            self._log_debug(f"📋 可选检测结果 ({len(detection_results)} 个):")
            for i, detection in enumerate(detection_results):
                self._log_debug(f"  {i+1}. object_id={getattr(detection, 'object_id', 'None')}, "
                              f"match_confidence={getattr(detection, 'match_confidence', 0.0):.4f}, "
                              f"class_name={getattr(detection, 'class_name', 'Unknown')}, "
                              f"class_id={getattr(detection, 'class_id', -1)}")
            
            # 查找目标
            for detection in detection_results:
                if (hasattr(detection, 'object_id') and 
                    detection.object_id == target_object_id and 
                    hasattr(detection, 'match_confidence') and
                    detection.match_confidence > self.match_threshold):
                    
                    self._log_debug(f"✅ 找到目标: {target_object_id} (置信度: {detection.match_confidence:.4f})")
                    return detection
                elif (hasattr(detection, 'object_id') and 
                      detection.object_id == target_object_id):
                    self._log_debug(f"⚠️ 找到目标但置信度过低: {target_object_id} "
                                  f"(置信度: {getattr(detection, 'match_confidence', 0.0):.4f} < {self.match_threshold})")
            
            self._log_debug(f"❌ 未找到目标: {target_object_id}")
            return None
            
        except Exception as e:
            self._log_error(f"❌ 获取目标检测失败: {e}")
            return None
    
    # 日志方法
    def _log_info(self, message: str):
        """记录信息日志"""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[IMPROVED_ID_MATCHER] {message}")
    
    def _log_debug(self, message: str):
        """记录调试日志"""
        if self.logger:
            self.logger.debug(message)
        else:
            print(f"[IMPROVED_ID_MATCHER] DEBUG: {message}")
    
    def _log_warn(self, message: str):
        """记录警告日志"""
        if self.logger:
            self.logger.warn(message)
        else:
            print(f"[IMPROVED_ID_MATCHER] WARNING: {message}")
    
    def _log_error(self, message: str):
        """记录错误日志"""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"[IMPROVED_ID_MATCHER] ERROR: {message}")


# 向后兼容的别名
IDMatcher = ImprovedIDMatcher


if __name__ == "__main__":
    # 测试改进版ID匹配器
    from ..utils.config import create_tracking_config
    
    config = create_tracking_config()
    matcher = ImprovedIDMatcher(config)
    
    # 设置调试输出
    matcher.set_debug_output_dir("/tmp/id_matcher_debug")
    
    print("🧪 测试改进版ID匹配器...")
    
    # 创建测试检测结果
    test_detection = DetectionResult(
        object_id="test_corn_0",
        class_id=3,
        class_name="corn",
        bounding_box=[100, 100, 200, 200],
        mask=np.zeros((100, 100), dtype=np.uint8),
        centroid_2d=(150, 150),
        centroid_3d=(150, 150, 300),
        confidence=0.9,
        features={
            'color': {'histogram': [0.1] * 64 * 3},
            'shape': {'hu_moments': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]},
        }
    )
    
    # 测试目标专用匹配
    target_match = matcher.match_target_only([test_detection], 3, "corn_0")
    
    if target_match:
        print(f"✅ 匹配成功: {target_match.object_id} (置信度: {target_match.match_confidence:.4f})")
    else:
        print("❌ 匹配失败")
    
    # 打印详细状态
    matcher.print_detailed_status()
    
    # 保存调试历史
    matcher.save_all_debug_history()