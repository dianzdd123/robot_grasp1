# tracking/enhanced_tracker.py
import os
import json
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import time

# 导入增强组件
from ..detection.features.similarity_calculator import FeatureSimilarityCalculator
from ..detection.utils.coordinate_calculator import CoordinateCalculator, ObjectAnalyzer
from ..detection.utils.adaptive_learner import AdaptiveThresholdManager
from ..detection.utils.enhanced_config_manager import EnhancedConfigManager

class EnhancedTracker:
    """增强Track模块 - 独立的特征匹配追踪器"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化增强追踪器
        
        Args:
            config_file: 配置文件路径
        """
        # 配置管理
        self.config_manager = EnhancedConfigManager(config_file)
        
        # 初始化核心组件
        self._initialize_components()
        
        # 数据存储
        self.reference_library = {}
        self.current_targets = {}
        self.tracking_history = []
        
        # 追踪状态
        self.tracking_active = False
        self.current_frame_count = 0
        
        print("[ENHANCED_TRACKER] 增强追踪器初始化完成")
    
    def _initialize_components(self):
        """初始化核心组件"""
        try:
            # 相似度计算器
            similarity_config = self.config_manager.get_similarity_config()
            feature_weights = similarity_config.get('feature_weights', {})
            self.similarity_calculator = FeatureSimilarityCalculator(feature_weights)
            
            # 坐标计算器
            camera_config = self.config_manager.get_camera_config()
            calibration_data = {
                'camera_intrinsics': camera_config.get('intrinsics', {}),
                'hand_eye_translation': camera_config.get('hand_eye_calibration', {}).get('translation'),
                'hand_eye_quaternion': camera_config.get('hand_eye_calibration', {}).get('quaternion')
            }
            self.coordinate_calculator = CoordinateCalculator(calibration_data)
            self.object_analyzer = ObjectAnalyzer(self.coordinate_calculator)
            
            # 自适应学习管理器
            adaptive_config = self.config_manager.get_adaptive_learning_config()
            if adaptive_config.get('enabled', True):
                learning_file = adaptive_config.get('learning_data_file', 'data/tracking_adaptive_learning.json')
                self.adaptive_manager = AdaptiveThresholdManager(learning_file)
                print("[ENHANCED_TRACKER] 自适应学习已启用")
            else:
                self.adaptive_manager = None
                
            print("[ENHANCED_TRACKER] 核心组件初始化成功")
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 组件初始化失败: {e}")
            raise
    
    def load_reference_features(self, reference_library_path: str) -> bool:
        """
        从Detect结果加载参考特征库
        
        Args:
            reference_library_path: 参考特征库文件路径
            
        Returns:
            success: 是否加载成功
        """
        try:
            if not os.path.exists(reference_library_path):
                print(f"[ENHANCED_TRACKER] 参考特征库文件不存在: {reference_library_path}")
                return False
            
            with open(reference_library_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 加载参考特征库
            self.reference_library = data
            
            print(f"[ENHANCED_TRACKER] 成功加载 {len(self.reference_library)} 个参考特征")
            
            # 显示加载的特征摘要
            self._display_reference_library_summary()
            
            return True
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 加载参考特征库失败: {e}")
            return False
    
    def _display_reference_library_summary(self):
        """显示参考特征库摘要"""
        try:
            print(f"\n{'='*50}")
            print("参考特征库摘要")
            print(f"{'='*50}")
            
            # 按类别统计
            by_class = {}
            quality_scores = []
            
            for obj_id, entry in self.reference_library.items():
                if isinstance(entry, dict) and 'metadata' in entry:
                    class_name = entry['metadata'].get('class_name', 'unknown')
                    quality_score = entry.get('quality_score', 0)
                    
                    if class_name not in by_class:
                        by_class[class_name] = []
                    by_class[class_name].append((obj_id, quality_score))
                    quality_scores.append(quality_score)
            
            print(f"总计: {len(self.reference_library)} 个参考特征")
            
            if quality_scores:
                print(f"平均特征质量: {np.mean(quality_scores):.1f}%")
                print(f"质量范围: {np.min(quality_scores):.1f}% - {np.max(quality_scores):.1f}%")
            
            print("\n按类别分布:")
            for class_name, objects in by_class.items():
                avg_quality = np.mean([q for _, q in objects])
                print(f"  {class_name}: {len(objects)} 个对象 (平均质量: {avg_quality:.1f}%)")
            
            print(f"{'='*50}\n")
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 显示摘要失败: {e}")
    
    def select_tracking_target(self, target_id: str) -> bool:
        """
        选择要追踪的目标
        
        Args:
            target_id: 目标对象ID
            
        Returns:
            success: 是否选择成功
        """
        try:
            if target_id not in self.reference_library:
                print(f"[ENHANCED_TRACKER] 目标ID不存在: {target_id}")
                return False
            
            # 获取目标的参考特征
            target_entry = self.reference_library[target_id]
            
            # 设置当前追踪目标
            self.current_targets[target_id] = {
                'reference_features': target_entry['features'],
                'metadata': target_entry['metadata'],
                'quality_score': target_entry.get('quality_score', 0),
                'tracking_state': 'initialized',
                'last_detection': None,
                'confidence_history': [],
                'position_history': []
            }
            
            print(f"[ENHANCED_TRACKER] 已选择追踪目标: {target_id}")
            print(f"  - 类别: {target_entry['metadata'].get('class_name', 'unknown')}")
            print(f"  - 特征质量: {target_entry.get('quality_score', 0):.1f}%")
            
            return True
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 选择追踪目标失败: {e}")
            return False
    
    def track_target(self, target_id: str, current_image: np.ndarray, 
                    current_depth: np.ndarray, waypoint_data: Dict,
                    candidate_detections: List[Dict]) -> Optional[Dict]:
        """
        追踪指定目标
        
        Args:
            target_id: 目标ID
            current_image: 当前RGB图像
            current_depth: 当前深度图像
            waypoint_data: 当前waypoint数据
            candidate_detections: 候选检测结果列表
            
        Returns:
            tracking_result: 追踪结果，包含最佳匹配和抓取信息
        """
        try:
            if target_id not in self.current_targets:
                print(f"[ENHANCED_TRACKER] 目标未被选择用于追踪: {target_id}")
                return None
            
            target_info = self.current_targets[target_id]
            reference_features = target_info['reference_features']
            
            print(f"[ENHANCED_TRACKER] 开始追踪目标: {target_id}")
            print(f"  - 候选检测数量: {len(candidate_detections)}")
            
            # Step 1: 为每个候选提取特征
            enhanced_candidates = []
            for i, candidate in enumerate(candidate_detections):
                try:
                    # 提取当前帧特征
                    candidate_features = self._extract_candidate_features(
                        candidate, current_image, current_depth, waypoint_data
                    )
                    
                    enhanced_candidates.append({
                        'index': i,
                        'original_data': candidate,
                        'features': candidate_features
                    })
                    
                except Exception as e:
                    print(f"[ENHANCED_TRACKER] 候选 {i} 特征提取失败: {e}")
                    continue
            
            if not enhanced_candidates:
                print("[ENHANCED_TRACKER] 没有有效的候选特征")
                return None
            
            # Step 2: 计算相似度并找到最佳匹配
            best_match = self.similarity_calculator.find_best_match(
                reference_features, enhanced_candidates
            )
            
            if not best_match:
                print("[ENHANCED_TRACKER] 未找到合适的匹配")
                return self._handle_tracking_failure(target_id)
            
            # Step 3: 应用自适应阈值
            overall_similarity = best_match['similarity_result']['overall_similarity']
            confidence = best_match['similarity_result']['confidence']
            
            # 获取动态阈值
            threshold = self._get_adaptive_threshold(target_info, confidence)
            
            print(f"[ENHANCED_TRACKER] 最佳匹配相似度: {overall_similarity:.3f} (阈值: {threshold:.3f})")
            
            if overall_similarity < threshold:
                print("[ENHANCED_TRACKER] 相似度低于阈值，匹配失败")
                return self._handle_tracking_failure(target_id)
            
            # Step 4: 时序一致性检查
            if not self._temporal_consistency_check(target_id, best_match):
                print("[ENHANCED_TRACKER] 时序一致性检查失败")
                return self._handle_tracking_failure(target_id)
            
            # Step 5: 生成追踪结果
            tracking_result = self._generate_tracking_result(
                target_id, best_match, waypoint_data
            )
            
            # Step 6: 更新追踪状态
            self._update_tracking_state(target_id, tracking_result)
            
            # Step 7: 自适应学习反馈（标记为成功匹配）
            if self.adaptive_manager:
                self._update_adaptive_learning(target_id, best_match, True)
            
            print(f"[ENHANCED_TRACKER] 追踪成功: {target_id}")
            return tracking_result
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 追踪失败: {e}")
            return None
    
    def _extract_candidate_features(self, candidate: Dict, image: np.ndarray,
                                   depth: np.ndarray, waypoint_data: Dict) -> Dict:
        """为候选检测提取特征"""
        # 这里应该使用与Detect模块相同的特征提取逻辑
        # 为了简化，我们假设candidate已经包含了基本特征
        # 在实际实现中，需要调用enhanced_detection_pipeline的特征提取方法
        
        # 获取基本信息
        bbox = candidate.get('bounding_box', [0, 0, 100, 100])
        mask = candidate.get('mask', np.zeros((image.shape[0], image.shape[1]), dtype=bool))
        
        # 提取空间特征
        spatial_features = self.object_analyzer.calculate_3d_spatial_features(
            mask, depth, waypoint_data, bbox
        )
        
        # 这里应该调用完整的特征提取器
        # 为了演示，返回简化的特征结构
        features = {
            'geometric': candidate.get('geometric_features', {}),
            'appearance': candidate.get('appearance_features', {}),
            'shape': candidate.get('shape_features', {}),
            'spatial': spatial_features
        }
        
        return features
    
    def _get_adaptive_threshold(self, target_info: Dict, confidence: float) -> float:
        """获取自适应阈值"""
        if not self.adaptive_manager:
            # 使用配置文件中的默认阈值
            similarity_config = self.config_manager.get_similarity_config()
            return similarity_config.get('thresholds', {}).get('overall_match', 0.75)
        
        # 使用自适应阈值
        feature_quality = target_info.get('quality_score', 75.0)
        context = {
            'tracking_state': target_info.get('tracking_state', 'unknown'),
            'confidence_history': target_info.get('confidence_history', [])
        }
        
        return self.adaptive_manager.get_adaptive_threshold(
            'overall', 'match', feature_quality, context
        )
    
    def _temporal_consistency_check(self, target_id: str, best_match: Dict) -> bool:
        """时序一致性检查"""
        try:
            target_info = self.current_targets[target_id]
            position_history = target_info.get('position_history', [])
            
            if len(position_history) < 2:
                return True  # 历史数据不足，跳过检查
            
            # 获取当前位置
            current_spatial = best_match['candidate_data']['features'].get('spatial', {})
            current_position = current_spatial.get('world_coordinates', [0, 0, 0])
            
            # 计算与最近位置的距离
            last_position = position_history[-1]
            distance = np.linalg.norm(np.array(current_position) - np.array(last_position))
            
            # 最大允许移动距离（毫米）
            max_movement = 200.0  # 200mm
            
            if distance > max_movement:
                print(f"[ENHANCED_TRACKER] 时序一致性检查失败: 移动距离 {distance:.1f}mm > {max_movement}mm")
                return False
            
            return True
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 时序一致性检查异常: {e}")
            return True  # 异常时允许通过
    
    def _generate_tracking_result(self, target_id: str, best_match: Dict, 
                                waypoint_data: Dict) -> Dict:
        """生成追踪结果"""
        try:
            candidate_data = best_match['candidate_data']
            similarity_result = best_match['similarity_result']
            
            # 获取3D坐标和抓取信息
            spatial_features = candidate_data['features'].get('spatial', {})
            world_coordinates = spatial_features.get('world_coordinates', [0, 0, 0])
            gripper_info = spatial_features.get('gripper_width_info', {})
            
            # 构建追踪结果
            tracking_result = {
                'target_id': target_id,
                'detection_confidence': candidate_data['original_data'].get('confidence', 0.0),
                'tracking_confidence': similarity_result['overall_similarity'],
                'match_confidence': similarity_result['confidence'],
                
                # 抓取坐标信息
                'grasp_coordinate': {
                    'x': float(world_coordinates[0]),
                    'y': float(world_coordinates[1]),
                    'z': float(world_coordinates[2])
                },
                
                # 物体抓取信息
                'object_info': {
                    'object_id': target_id,
                    'class_name': self.current_targets[target_id]['metadata'].get('class_name', 'unknown'),
                    'estimated_height': spatial_features.get('height_mm', 30.0),
                    'background_z': spatial_features.get('background_world_z', 300.0),
                    'recommended_gripper_width': gripper_info.get('recommended_gripper_width', 150),
                    'grasp_angle': gripper_info.get('angle', 0.0)
                },
                
                # 详细相似度信息
                'similarity_breakdown': similarity_result['feature_similarities'],
                'valid_features': similarity_result['valid_features'],
                
                # 追踪元数据
                'timestamp': datetime.now().isoformat(),
                'frame_count': self.current_frame_count,
                'waypoint_info': waypoint_data
            }
            
            return tracking_result
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 生成追踪结果失败: {e}")
            return None
    
    def _update_tracking_state(self, target_id: str, tracking_result: Dict):
        """更新追踪状态"""
        try:
            target_info = self.current_targets[target_id]
            
            # 更新基本状态
            target_info['tracking_state'] = 'tracking'
            target_info['last_detection'] = tracking_result
            
            # 更新置信度历史
            confidence_history = target_info.get('confidence_history', [])
            confidence_history.append(tracking_result['tracking_confidence'])
            if len(confidence_history) > 10:  # 保持最近10个记录
                confidence_history = confidence_history[-10:]
            target_info['confidence_history'] = confidence_history
            
            # 更新位置历史
            position_history = target_info.get('position_history', [])
            current_position = [
                tracking_result['grasp_coordinate']['x'],
                tracking_result['grasp_coordinate']['y'],
                tracking_result['grasp_coordinate']['z']
            ]
            position_history.append(current_position)
            if len(position_history) > 5:  # 保持最近5个位置
                position_history = position_history[-5:]
            target_info['position_history'] = position_history
            
            # 更新帧计数
            self.current_frame_count += 1
            
            print(f"[ENHANCED_TRACKER] 已更新追踪状态: {target_id}")
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 更新追踪状态失败: {e}")
    
    def _handle_tracking_failure(self, target_id: str) -> Optional[Dict]:
        """处理追踪失败"""
        try:
            target_info = self.current_targets[target_id]
            
            # 更新失败状态
            target_info['tracking_state'] = 'lost'
            
            # 检查是否有最近的检测结果可以使用
            last_detection = target_info.get('last_detection')
            if last_detection:
                # 返回最后一次成功的检测结果，但标记为不确定
                failure_result = last_detection.copy()
                failure_result['tracking_confidence'] = 0.0
                failure_result['match_confidence'] = 0.0
                failure_result['status'] = 'lost'
                failure_result['timestamp'] = datetime.now().isoformat()
                
                print(f"[ENHANCED_TRACKER] 追踪失败，返回最后已知位置: {target_id}")
                return failure_result
            
            print(f"[ENHANCED_TRACKER] 追踪彻底失败: {target_id}")
            return None
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 处理追踪失败异常: {e}")
            return None
    
    def _update_adaptive_learning(self, target_id: str, match_result: Dict, is_correct: bool):
        """更新自适应学习"""
        try:
            if not self.adaptive_manager:
                return
            
            target_info = self.current_targets[target_id]
            similarity_result = match_result['similarity_result']
            feature_similarities = similarity_result['feature_similarities']
            feature_quality = target_info.get('quality_score', 75.0)
            
            # 为每个特征类型更新学习历史
            for feature_type, similarity in feature_similarities.items():
                self.adaptive_manager.update_learning_history(
                    feature_type=feature_type,
                    sub_feature='overall',
                    similarity=similarity,
                    feature_quality=feature_quality,
                    is_correct_match=is_correct,
                    context={
                        'target_id': target_id,
                        'frame_count': self.current_frame_count,
                        'tracking_state': target_info.get('tracking_state', 'unknown')
                    }
                )
            
            print(f"[ENHANCED_TRACKER] 已更新自适应学习: {target_id} ({'成功' if is_correct else '失败'})")
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 更新自适应学习失败: {e}")
    
    def get_tracking_status(self) -> Dict:
        """获取追踪状态"""
        try:
            status = {
                'tracking_active': self.tracking_active,
                'current_frame_count': self.current_frame_count,
                'total_targets': len(self.current_targets),
                'targets_status': {}
            }
            
            for target_id, target_info in self.current_targets.items():
                confidence_history = target_info.get('confidence_history', [])
                status['targets_status'][target_id] = {
                    'state': target_info.get('tracking_state', 'unknown'),
                    'quality_score': target_info.get('quality_score', 0),
                    'avg_confidence': np.mean(confidence_history) if confidence_history else 0.0,
                    'last_confidence': confidence_history[-1] if confidence_history else 0.0,
                    'detection_count': len(confidence_history)
                }
            
            return status
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 获取追踪状态失败: {e}")
            return {'error': str(e)}
    
    def optimize_tracking_parameters(self) -> Dict:
        """优化追踪参数"""
        try:
            if not self.adaptive_manager:
                return {'message': 'adaptive learning disabled'}
            
            # 执行阈值优化
            optimization_results = self.adaptive_manager.optimize_thresholds(min_samples=20)
            
            if optimization_results:
                # 更新相似度计算器的权重
                updated_weights = {}
                for feature_key, result in optimization_results.items():
                    if '.' in feature_key:
                        main_type = feature_key.split('.')[0]
                        if main_type not in updated_weights:
                            updated_weights[main_type] = 0.0
                        # 根据优化结果调整权重
                        improvement = result.get('improvement', 0)
                        updated_weights[main_type] += improvement * 0.1  # 小幅调整
                
                if updated_weights:
                    # 归一化权重
                    total_weight = sum(abs(w) for w in updated_weights.values())
                    if total_weight > 0:
                        current_weights = self.similarity_calculator.feature_weights.copy()
                        for feature_type, adjustment in updated_weights.items():
                            if feature_type in current_weights:
                                current_weights[feature_type] += adjustment * 0.1
                        
                        # 重新归一化
                        total = sum(current_weights.values())
                        if total > 0:
                            current_weights = {k: v/total for k, v in current_weights.items()}
                            self.similarity_calculator.update_weights(current_weights)
                
                print(f"[ENHANCED_TRACKER] 参数优化完成: {len(optimization_results)} 个特征已优化")
                return {
                    'optimized_features': len(optimization_results),
                    'results': optimization_results
                }
            else:
                return {'message': 'insufficient data for optimization'}
                
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 参数优化失败: {e}")
            return {'error': str(e)}
    
    def save_tracking_session(self, output_path: str):
        """保存追踪会话数据"""
        try:
            session_data = {
                'session_info': {
                    'start_time': datetime.now().isoformat(),
                    'frame_count': self.current_frame_count,
                    'total_targets': len(self.current_targets)
                },
                'targets': {},
                'tracking_history': self.tracking_history,
                'adaptive_learning_stats': self.adaptive_manager.get_performance_report() if self.adaptive_manager else None
            }
            
            # 保存目标信息（移除不能序列化的数据）
            for target_id, target_info in self.current_targets.items():
                session_data['targets'][target_id] = {
                    'metadata': target_info['metadata'],
                    'quality_score': target_info['quality_score'],
                    'tracking_state': target_info['tracking_state'],
                    'confidence_history': target_info['confidence_history'],
                    'position_history': target_info['position_history']
                }
            
            # 保存到文件
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            print(f"[ENHANCED_TRACKER] 追踪会话已保存: {output_path}")
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 保存追踪会话失败: {e}")
    
    def reset_tracking(self):
        """重置追踪状态"""
        try:
            self.current_targets.clear()
            self.tracking_history.clear()
            self.current_frame_count = 0
            self.tracking_active = False
            
            print("[ENHANCED_TRACKER] 追踪状态已重置")
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 重置追踪状态失败: {e}")
    
    def get_performance_report(self) -> Dict:
        """获取性能报告"""
        try:
            report = {
                'session_stats': {
                    'total_frames': self.current_frame_count,
                    'active_targets': len([t for t in self.current_targets.values() 
                                         if t.get('tracking_state') == 'tracking']),
                    'lost_targets': len([t for t in self.current_targets.values() 
                                       if t.get('tracking_state') == 'lost'])
                },
                'feature_performance': {},
                'adaptive_learning': None
            }
            
            # 计算各特征的平均性能
            all_confidences = {}
            for target_info in self.current_targets.values():
                for confidence in target_info.get('confidence_history', []):
                    if 'overall' not in all_confidences:
                        all_confidences['overall'] = []
                    all_confidences['overall'].append(confidence)
            
            for feature_type, confidences in all_confidences.items():
                if confidences:
                    report['feature_performance'][feature_type] = {
                        'mean_confidence': float(np.mean(confidences)),
                        'std_confidence': float(np.std(confidences)),
                        'min_confidence': float(np.min(confidences)),
                        'max_confidence': float(np.max(confidences)),
                        'sample_count': len(confidences)
                    }
            
            # 自适应学习报告
            if self.adaptive_manager:
                report['adaptive_learning'] = self.adaptive_manager.get_performance_report()
            
            return report
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 获取性能报告失败: {e}")
            return {'error': str(e)}