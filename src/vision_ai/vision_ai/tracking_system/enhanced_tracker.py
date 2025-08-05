# tracking/enhanced_tracker.py
import os
import json
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import time
import cv2
import math
# 导入增强组件
from ..detection.features.similarity_calculator import FeatureSimilarityCalculator
from ..detection.utils.coordinate_calculator import CoordinateCalculator, ObjectAnalyzer
from ..detection.utils.adaptive_learner import AdaptiveThresholdManager
from ..detection.utils.enhanced_config_manager import EnhancedConfigManager

class EnhancedTracker:
    """增强Track模块 - 独立的特征匹配追踪器"""
    
    def __init__(self, config_path: str):
        """初始化增强追踪器 - 修复版"""
        try:
            # 加载配置
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            tracking_config = self.config.get('tracking', {})
            
            # 🔧 确保设置相似度阈值
            self.similarity_threshold = tracking_config.get('similarity_threshold', 0.6)  # 降低默认阈值
            self.confidence_threshold = tracking_config.get('confidence_threshold', 0.6)
            self.max_tracking_distance = tracking_config.get('max_tracking_distance', 600.0)
            
            print(f"[ENHANCED_TRACKER] 配置加载完成:")
            print(f"  - 相似度阈值: {self.similarity_threshold}")
            print(f"  - 置信度阈值: {self.confidence_threshold}")
            print(f"  - 最大追踪距离: {self.max_tracking_distance}mm")
            
            # 初始化组件
            self.similarity_calculator = FeatureSimilarityCalculator()
            self.coordinate_calculator = None  # 将在需要时初始化
            
            # 数据存储
            self.reference_library = {}
            self.current_target_id = None
            self.current_target_class = None
            self.config_manager = EnhancedConfigManager(config_path)
            # 🆕 添加ID映射缓存
            self.id_to_class_mapping = {}
            self.class_to_ids_mapping = {}
            self.position_history = []
            self.confidence_history = []
            print("[ENHANCED_TRACKER] 增强追踪器初始化完成")
            self._initialize_components()

        except Exception as e:
            print(f"[ENHANCED_TRACKER] 初始化失败: {e}")
            # 设置默认值
            self.similarity_threshold = 0.3
            self.confidence_threshold = 0.5
            self.max_tracking_distance = 500.0
            self.similarity_calculator = FeatureSimilarityCalculator()
            self.reference_library = {}
            self.current_target_id = None
            self.current_target_class = None
            self.id_to_class_mapping = {}
            self.class_to_ids_mapping = {}
    
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
    
    def load_reference_features(self, library_file: str) -> bool:
        """加载参考特征库 - 优化版，构建ID映射"""
        try:
            with open(library_file, 'r', encoding='utf-8') as f:
                library_data = json.load(f)
            
            self.reference_library = {}
            
            # 🆕 构建ID映射
            for obj_id, entry in library_data.items():
                self.reference_library[obj_id] = entry
                
                # 提取类别信息
                class_name = obj_id.split('_')[0]
                self.id_to_class_mapping[obj_id] = class_name
                
                # 构建类别到ID的映射
                if class_name not in self.class_to_ids_mapping:
                    self.class_to_ids_mapping[class_name] = []
                self.class_to_ids_mapping[class_name].append(obj_id)
            
            print(f"[ENHANCED_TRACKER] 参考特征库加载完成")
            print(f"[ENHANCED_TRACKER] 总对象数: {len(self.reference_library)}")
            print(f"[ENHANCED_TRACKER] 类别统计:")
            for class_name, ids in self.class_to_ids_mapping.items():
                print(f"  - {class_name}: {len(ids)} 个对象 {ids}")
            
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
        """选择追踪目标 - 添加验证"""
        try:
            if target_id not in self.reference_library:
                print(f"[ENHANCED_TRACKER] 错误: 目标 {target_id} 不存在于参考库中")
                print(f"[ENHANCED_TRACKER] 可用目标: {list(self.reference_library.keys())}")
                return False
            
            self.current_target_id = target_id
            self.current_target_class = self.id_to_class_mapping[target_id]
            
            print(f"[ENHANCED_TRACKER] 已选择追踪目标: {target_id}")
            print(f"[ENHANCED_TRACKER] 目标类别: {self.current_target_class}")
            print(f"[ENHANCED_TRACKER] 同类别其他对象: {[id for id in self.class_to_ids_mapping[self.current_target_class] if id != target_id]}")
            
            return True
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 选择追踪目标失败: {e}")
            return False
    
    def track_target(self, target_id: str, image_rgb: np.ndarray, 
                    depth_image: np.ndarray, waypoint_data: Dict,
                    candidate_detections: List[Dict]) -> Optional[Dict]:
        """追踪目标 - 增强版，加入自适应权重和位置验证"""
        try:
            print(f"[ENHANCED_TRACKER] 开始增强追踪: {target_id}")
            
            # ... 现有的候选过滤代码 ...
            target_class = target_id.split('_')[0]
            same_class_candidates = [d for d in candidate_detections if d['class_name'] == target_class]
            
            if len(same_class_candidates) == 0:
                print(f"[ENHANCED_TRACKER] 未发现同类别候选")
                return None
            
            reference_features = self.reference_library[target_id]['features']
            
            # 🆕 构建追踪上下文
            tracking_context = self._build_tracking_context(waypoint_data)
            
            best_match = None
            best_detailed_similarity = None
            best_similarity = 0.0
            
            for i, detection in enumerate(same_class_candidates):
                try:
                    # 🆕 计算候选位置
                    candidate_coord = self._extract_candidate_position(detection, waypoint_data, depth_image)
                    
                    # 🆕 位置连续性验证
                    continuity_score = self._validate_position_continuity(candidate_coord)
                    
                    # 🆕 遮挡检测
                    current_confidence = detection.get('confidence', 0.0)
                    occlusion_score = self._detect_occlusion(current_confidence, detection.get('features', {}))
                    
                    # 更新追踪上下文
                    tracking_context.update({
                        'continuity_score': continuity_score,
                        'occlusion_score': occlusion_score,
                        'candidate_position': candidate_coord
                    })
                    
                    # 🆕 使用自适应相似度计算
                    detailed_similarity = self.similarity_calculator.calculate_detailed_similarity_breakdown_adaptive(
                        reference_features, 
                        detection.get('features', {}), 
                        waypoint_data,
                        tracking_context
                    )
                    
                    # 🆕 综合分数：相似度 × 位置连续性 × (1 - 遮挡分数)
                    raw_similarity = detailed_similarity['final_score']
                    adjusted_similarity = raw_similarity * continuity_score * (1.0 - occlusion_score * 0.5)
                    
                    print(f"[ENHANCED_TRACKER] 候选 {i+1}: 原始={raw_similarity:.3f}, 连续性={continuity_score:.3f}, 遮挡={occlusion_score:.3f} → 调整后={adjusted_similarity:.3f}")
                    
                    if adjusted_similarity > best_similarity:
                        best_similarity = adjusted_similarity
                        best_match = detection
                        best_detailed_similarity = detailed_similarity
                        best_detailed_similarity['adjusted_similarity'] = adjusted_similarity
                        best_detailed_similarity['continuity_score'] = continuity_score
                        best_detailed_similarity['occlusion_score'] = occlusion_score
                        
                except Exception as e:
                    print(f"[ENHANCED_TRACKER] 处理候选 {i} 失败: {e}")
                    continue
            
            if best_match and best_similarity >= self.similarity_threshold:
                print(f"[ENHANCED_TRACKER] 增强匹配成功: {best_similarity:.3f}")
                
                # 🆕 更新历史记录
                self._update_tracking_history(best_detailed_similarity.get('candidate_position', {}), best_similarity)
                
                return self._build_tracking_result_with_detailed_features(
                    target_id, best_match, best_detailed_similarity, waypoint_data, image_rgb, depth_image
                )
            else:
                print(f"[ENHANCED_TRACKER] 增强匹配失败")
                return None
                
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 增强追踪失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    def _build_tracking_context(self, waypoint_data: Dict) -> Dict:
        """构建追踪上下文"""
        try:
            # 计算与当前位置的距离
            current_pos = waypoint_data.get('world_pos', [0, 0, 350])
            distance_3d = 100.0  # 默认值
            
            if self.position_history:
                last_pos = self.position_history[-1]
                distance_3d = math.sqrt(
                    (current_pos[0] - last_pos['x'])**2 +
                    (current_pos[1] - last_pos['y'])**2 +
                    (current_pos[2] - last_pos['z'])**2
                )
            
            context = {
                'distance_3d': distance_3d,
                'confidence_history': self.confidence_history.copy(),
                'current_position': {
                    'x': current_pos[0], 
                    'y': current_pos[1], 
                    'z': current_pos[2]
                },
                'lighting_change': 0.0  # 后续可以通过图像分析得到
            }
            
            return context
            
        except Exception as e:
            print(f"[TRACKING_CONTEXT] 构建上下文失败: {e}")
            return {'distance_3d': 100.0, 'confidence_history': []}

    def _extract_candidate_position(self, detection: Dict, waypoint_data: Dict, depth_image: np.ndarray) -> Dict:
        """提取候选位置坐标"""
        try:
            # 使用现有的坐标计算方法
            grasp_coord = self._calculate_grasp_coordinate(detection, waypoint_data, depth_image)
            return grasp_coord
        except Exception as e:
            print(f"[POSITION_EXTRACT] 提取候选位置失败: {e}")
            return {'x': 0.0, 'y': 0.0, 'z': 350.0}

    def _update_tracking_history(self, position: Dict, confidence: float):
        """更新追踪历史"""
        try:
            self.position_history.append(position)
            self.confidence_history.append(confidence)
            
            # 保持历史长度
            max_history = 10
            if len(self.position_history) > max_history:
                self.position_history = self.position_history[-max_history:]
            if len(self.confidence_history) > max_history:
                self.confidence_history = self.confidence_history[-max_history:]
                
        except Exception as e:
            print(f"[TRACKING_HISTORY] 更新历史失败: {e}")
            
    def _build_tracking_result_with_detailed_features(self, target_id: str, detection: Dict, 
                                                    detailed_similarity: Dict, waypoint_data: Dict,
                                                    image_rgb: np.ndarray, depth_image: np.ndarray) -> Dict:
        """构建包含详细特征的追踪结果"""
        try:
            print("[ENHANCED_TRACKER] 构建详细追踪结果...")
            
            # 🆕 计算最小外接矩形
            bounding_rect = self._calculate_minimum_bounding_rect(detection)
            
            # 计算3D抓取坐标
            grasp_coord = self._calculate_grasp_coordinate(detection, waypoint_data, depth_image)
            
            # 分析物体信息
            features = detection.get('features', {})
            object_info = self._analyze_object_for_grasping_fixed(detection, waypoint_data, features, depth_image)
            
            # 构建追踪结果
            tracking_result = {
                'target_id': target_id,
                'detection_confidence': float(detection.get('confidence', 0.0)),
                'tracking_confidence': float(detailed_similarity['final_score']),
                
                # 抓取坐标
                'grasp_coordinate': grasp_coord,
                
                # 物体信息
                'object_info': object_info,
                
                # 🆕 最小外接矩形信息
                'bounding_rect': bounding_rect,
                
                # 🆕 详细相似度分解 - 确保传递
                'detailed_similarity_breakdown': detailed_similarity.get('detailed_breakdown', {}),
                'similarity_breakdown': detailed_similarity.get('feature_contributions', {}),
                'feature_weights_used': detailed_similarity.get('feature_weights_used', {}),
                
                # 元数据
                'timestamp': datetime.now().isoformat(),
                'waypoint_info': waypoint_data
            }
            
            print(f"[ENHANCED_TRACKER] 详细追踪结果构建完成:")
            print(f"  抓取坐标: {grasp_coord}")
            print(f"  详细特征数量: {len(detailed_similarity.get('detailed_breakdown', {}))}")
            print(f"  相似度分解数量: {len(detailed_similarity.get('feature_contributions', {}))}")
            
            return tracking_result
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 构建详细追踪结果失败: {e}")
            import traceback
            traceback.print_exc()
            return None
            
    def _build_tracking_result_from_detection(self, target_id: str, detection: Dict, 
                                            similarity_score: float, waypoint_data: Dict,
                                            image_rgb: np.ndarray, depth_image: np.ndarray) -> Dict:
        """从检测结果构建追踪结果 - 使用参考库数据"""
        try:
            print("[ENHANCED_TRACKER] 构建追踪结果...")
            print(f"[ENHANCED_TRACKER] 目标ID: {target_id}")

            bounding_rect = self._calculate_minimum_bounding_rect(detection)
            
            # 🔧 验证参考库数据
            if hasattr(self, 'reference_library') and target_id in self.reference_library:
                ref_entry = self.reference_library[target_id]
                spatial_ref = ref_entry.get('features', {}).get('spatial', {})
                
                print(f"[ENHANCED_TRACKER] 参考库验证:")
                print(f"  height_mm: {spatial_ref.get('height_mm')}")
                print(f"  background_world_z: {spatial_ref.get('background_world_z')}")
            
            features = detection.get('features', {})
            if not features:
                features = {
                    'geometric': detection.get('geometric_features', {}),
                    'appearance': detection.get('appearance_features', {}),
                    'shape': detection.get('shape_features', {}),
                    'spatial': detection.get('spatial_features', {})
                }
            
            # 计算3D抓取坐标
            grasp_coord = self._calculate_grasp_coordinate(detection, waypoint_data, depth_image)
            
            # 分析物体信息
            object_info = self._analyze_object_for_grasping_fixed(detection, waypoint_data, features, depth_image)
            
            # 构建追踪结果
            tracking_result = {
                'target_id': target_id,
                'detection_confidence': float(detection.get('confidence', 0.0)),
                'tracking_confidence': float(similarity_score),
                
                # 抓取坐标
                'grasp_coordinate': grasp_coord,
                
                # 物体信息
                'object_info': object_info,
                
                # 🆕 添加最小外接矩形信息
                'bounding_rect': bounding_rect,
                
                # 相似度分解
                'similarity_breakdown': {},
                
                # 元数据
                'timestamp': datetime.now().isoformat(),
                'waypoint_info': waypoint_data
            }
            
            print(f"[ENHANCED_TRACKER] 追踪结果构建完成:")
            print(f"  抓取坐标: {grasp_coord}")
            print(f"  物体高度: {object_info['estimated_height']:.1f}mm")
            print(f"  背景高度: {object_info['background_z']:.1f}mm")
            print(f"  最小外接矩形: {bounding_rect['width']:.1f}x{bounding_rect['height']:.1f}, 角度{bounding_rect['angle']:.1f}°")
            
            return tracking_result
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 构建追踪结果失败: {e}")
            import traceback
            traceback.print_exc()
            return None
        
    def _calculate_minimum_bounding_rect(self, detection: Dict) -> Dict:
        """基于mask计算最小外接矩形"""
        try:
            import cv2
            import numpy as np
            
            mask = detection.get('mask')
            if mask is None or not isinstance(mask, np.ndarray):
                print("[ENHANCED_TRACKER] 无效的mask数据")
                return {'width': 0, 'height': 0, 'angle': 0, 'center': [0, 0]}
            
            # 确保mask是正确的格式
            if mask.dtype != np.uint8:
                if mask.dtype == bool:
                    mask = mask.astype(np.uint8) * 255
                else:
                    mask = mask.astype(np.uint8)
            
            # 找到轮廓
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                print("[ENHANCED_TRACKER] 未找到有效轮廓")
                return {'width': 0, 'height': 0, 'angle': 0, 'center': [0, 0]}
            
            # 获取最大轮廓的最小外接矩形
            largest_contour = max(contours, key=cv2.contourArea)
            rect = cv2.minAreaRect(largest_contour)
            center, (width, height), angle = rect
            if width < height:
                yaw_angle = -angle + 90 
            else:
                yaw_angle = -angle
            print(f"[ENHANCED_TRACKER] 最小外接矩形: 中心{center}, 尺寸({width:.1f}x{height:.1f}), 角度{yaw_angle:.1f}°")
            
            return {
                'width': float(width),
                'height': float(height), 
                'angle': float(yaw_angle),
                'center': [float(center[0]), float(center[1])]
            }
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 最小外接矩形计算失败: {e}")
            return {'width': 0, 'height': 0, 'angle': 0, 'center': [0, 0]}        
    
    def _calculate_grasp_coordinate(self, detection: Dict, waypoint_data: Dict, depth_image: np.ndarray) -> Dict:
        """通过ObjectAnalyzer计算3D抓取坐标"""
        try:
            mask = detection.get('mask')
            bbox = detection.get('bounding_box', [0, 0, 100, 100])
            
            if mask is None or depth_image is None:
                raise ValueError("缺少mask或depth图")

            spatial_features = self.object_analyzer.calculate_3d_spatial_features(
                mask, depth_image, waypoint_data, bbox
            )

            coords = spatial_features.get('world_coordinates', [0, 0, 350])
            return {
                'x': float(coords[0]),
                'y': float(coords[1]),
                'z': float(coords[2])
            }
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 统一坐标转换失败: {e}")
            return {'x': 0.0, 'y': 0.0, 'z': 350.0}

    def _analyze_object_for_grasping_fixed(self, detection: Dict, waypoint_data, features: Dict, 
                                        depth_image: np.ndarray) -> Dict:
        """分析物体抓取信息 - 最终修复版"""
        try:
            print(f"[ENHANCED_TRACKER] 开始物体分析，目标ID: {self.current_target_id}")
            
            # 🔧 直接从参考库获取数据，不依赖任何缓存
            if (hasattr(self, 'current_target_id') and 
                self.current_target_id and 
                hasattr(self, 'reference_library') and
                self.current_target_id in self.reference_library):
                
                ref_entry = self.reference_library[self.current_target_id]
                spatial_features = ref_entry.get('features', {}).get('spatial', {})
                metadata = ref_entry.get('metadata', {})
                
                # 🔧 直接从参考库读取
                height_mm = spatial_features.get('height_mm')
                background_world_z = spatial_features.get('background_world_z')
                class_name = metadata.get('class_name', 'unknown')
                
                print(f"[ENHANCED_TRACKER] 参考库原始数据:")
                print(f"  height_mm: {height_mm}")
                print(f"  background_world_z: {background_world_z}")
                print(f"  class_name: {class_name}")
                
                if height_mm is not None and background_world_z is not None:
                    object_info = {
                        'object_id': self.current_target_id,
                        'class_name': class_name,
                        'estimated_height': float(height_mm),
                        'background_z': float(background_world_z),
                        'recommended_gripper_width': 500,
                        'grasp_angle': waypoint_data.get('yaw', 0.0)
                    }
                    
                    print(f"[ENHANCED_TRACKER] ✅ 使用参考库固定数据:")
                    print(f"  高度: {object_info['estimated_height']:.1f}mm (来源: reference_library)")
                    print(f"  背景: {object_info['background_z']:.1f}mm (来源: reference_library)")
                    print(f"  类别: {object_info['class_name']}")
                    
                    return object_info
                else:
                    print(f"[ENHANCED_TRACKER] ⚠️ 参考库中数据为空:")
                    print(f"  height_mm 为空: {height_mm is None}")
                    print(f"  background_world_z 为空: {background_world_z is None}")
            else:
                print(f"[ENHANCED_TRACKER] ⚠️ 参考库访问检查:")
                print(f"  has_current_target_id: {hasattr(self, 'current_target_id')}")
                print(f"  current_target_id: {getattr(self, 'current_target_id', None)}")
                print(f"  has_reference_library: {hasattr(self, 'reference_library')}")
                if hasattr(self, 'reference_library'):
                    print(f"  reference_library_size: {len(self.reference_library)}")
                    print(f"  reference_library_keys: {list(self.reference_library.keys())}")
                    if self.current_target_id:
                        print(f"  target_in_library: {self.current_target_id in self.reference_library}")
            
            # 如果参考库数据不可用，使用默认值
            print(f"[ENHANCED_TRACKER] ⚠️ 使用默认值")
            return {
                'object_id': 'unknown',
                'class_name': 'unknown',
                'estimated_height': 30.0,
                'background_z': 300.0,
                'recommended_gripper_width': 500,
                'grasp_angle': 0.0
            }
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 物体分析失败: {e}")
            import traceback
            traceback.print_exc()
            return {
                'object_id': 'unknown',
                'class_name': 'unknown',
                'estimated_height': 30.0,
                'background_z': 300.0,
                'recommended_gripper_width': 500,
                'grasp_angle': 0.0
            }

    def _get_fixed_object_info_with_cache(self, detection: Dict) -> Dict:
        """从固定检测结果获取物体信息 - 优先使用参考库数据"""
        try:
            object_id = detection.get('object_id')
            class_name = detection.get('class_name', 'unknown')
            
            # 默认值
            default_info = {
                'object_id': object_id or 'unknown',
                'class_name': class_name,
                'estimated_height': 30.0,
                'background_z': 300.0,
                'recommended_gripper_width': 500,
            }
            
            print(f"[ENHANCED_TRACKER] 获取物体信息: 目标ID={self.current_target_id}")
            
            # 🔧 关键修复：优先使用参考库数据
            if hasattr(self, 'current_target_id') and self.current_target_id:
                if self.current_target_id in self.reference_library:
                    ref_entry = self.reference_library[self.current_target_id]
                    if 'features' in ref_entry and 'spatial' in ref_entry['features']:
                        spatial_ref = ref_entry['features']['spatial']
                        depth_info = spatial_ref.get('depth_info', {})
                        
                        if 'height_mm' in depth_info:
                            default_info['estimated_height'] = float(depth_info['height_mm'])
                            print(f"[ENHANCED_TRACKER] 📚 使用参考库高度: {default_info['estimated_height']:.1f}mm")
                        if 'background_world_z' in depth_info:
                            default_info['background_z'] = float(depth_info['background_world_z'])
                            print(f"[ENHANCED_TRACKER] 📚 使用参考库背景: {default_info['background_z']:.1f}mm")
                        
                        # 如果参考库中有完整数据，直接返回
                        if 'height_mm' in depth_info and 'background_world_z' in depth_info:
                            print(f"[ENHANCED_TRACKER] ✅ 使用参考库完整数据 (优先级1)")
                            return default_info
            
            # 🔧 备用方案：使用检测结果缓存
            if hasattr(self, 'detection_results_cache') and self.current_target_id:
                print(f"[ENHANCED_TRACKER] 检查缓存，缓存大小: {len(getattr(self, 'detection_results_cache', {}))}")
                
                if self.current_target_id in self.detection_results_cache:
                    cache_data = self.detection_results_cache[self.current_target_id]
                    
                    # 🆕 只在参考库数据不完整时使用缓存数据
                    if default_info['estimated_height'] == 30.0:  # 参考库没有高度数据
                        default_info['estimated_height'] = cache_data['height_mm']
                        print(f"[ENHANCED_TRACKER] 💾 补充缓存高度: {default_info['estimated_height']:.1f}mm")
                    
                    if default_info['background_z'] == 300.0:  # 参考库没有背景数据
                        default_info['background_z'] = cache_data['background_world_z']
                        print(f"[ENHANCED_TRACKER] 💾 补充缓存背景: {default_info['background_z']:.1f}mm")
                    
                    if default_info['class_name'] == 'unknown':  # 补充类别信息
                        default_info['class_name'] = cache_data['class_name']
                    
                    print(f"[ENHANCED_TRACKER] ✅ 使用参考库+缓存组合数据 (优先级2)")
                    return default_info
                else:
                    print(f"[ENHANCED_TRACKER] ⚠️ 目标 {self.current_target_id} 不在缓存中")
                    print(f"[ENHANCED_TRACKER] 可用缓存键: {list(self.detection_results_cache.keys())}")
            else:
                print(f"[ENHANCED_TRACKER] ⚠️ 缓存不可用: hasattr={hasattr(self, 'detection_results_cache')}, target_id={self.current_target_id}")
            
            print(f"[ENHANCED_TRACKER] ⚠️ 使用默认值 (优先级3): 高度={default_info['estimated_height']:.1f}mm, 背景={default_info['background_z']:.1f}mm")
            return default_info
            
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 获取固定物体信息失败: {e}")
            import traceback
            traceback.print_exc()
            return {
                'object_id': 'unknown',
                'class_name': 'unknown', 
                'estimated_height': 30.0,
                'background_z': 300.0,
                'recommended_gripper_width': 500,
                'grasp_angle': 0.0
            }
        
    def set_detection_results_cache(self, cache: Dict):
        """设置检测结果缓存"""
        self.detection_results_cache = cache
        print(f"[ENHANCED_TRACKER] 检测结果缓存已设置: {len(cache)} 个目标")

    def _calculate_similarity(self, reference_features: Dict, 
                            candidate_detection: Dict, 
                            waypoint_data: Dict) -> float:
        """计算相似度 - 修复版本"""
        try:
            # 🔧 提取候选特征（适配不同的特征格式）
            candidate_features = {}
            
            # 尝试多种特征提取方式
            if 'geometric_features' in candidate_detection:
                candidate_features['geometric'] = candidate_detection['geometric_features']
            if 'appearance_features' in candidate_detection:
                candidate_features['appearance'] = candidate_detection['appearance_features']
            if 'shape_features' in candidate_detection:
                candidate_features['shape'] = candidate_detection['shape_features']
            if 'spatial_features' in candidate_detection:
                candidate_features['spatial'] = candidate_detection['spatial_features']
            
            # 如果上面没有找到，尝试从features字段提取
            if not candidate_features and 'features' in candidate_detection:
                features = candidate_detection['features']
                candidate_features['geometric'] = features.get('geometric', {})
                candidate_features['appearance'] = features.get('appearance', features.get('color', {}))
                candidate_features['shape'] = features.get('shape', {})
                candidate_features['spatial'] = features.get('spatial', {})
            
            print(f"[SIMILARITY] 参考特征类型: {list(reference_features.keys())}")
            print(f"[SIMILARITY] 候选特征类型: {list(candidate_features.keys())}")
            
            # 🔧 使用修复后的相似度计算方法
            similarity_result = self.similarity_calculator.calculate_comprehensive_similarity(
                reference_features, 
                candidate_features, 
                waypoint_data
            )
            
            final_score = similarity_result.get('final_score', 0.0)
            breakdown = similarity_result.get('breakdown', {})
            
            print(f"[SIMILARITY] 相似度分解:")
            for feature_type, score in breakdown.items():
                print(f"  - {feature_type}: {score:.3f}")
            print(f"[SIMILARITY] 最终得分: {final_score:.3f}")
            
            return final_score
            
        except Exception as e:
            print(f"[SIMILARITY] 相似度计算失败: {e}")
            import traceback
            traceback.print_exc()
            return 0.0
        
    def _extract_candidate_features(self, candidate: Dict, image: np.ndarray,
                                   depth: np.ndarray, waypoint_data: Dict) -> Dict:
        """为候选检测提取特征 - 优化版本"""
        try:
            # 🆕 如果candidate已经包含detection_pipeline提取的特征，直接使用
            if 'geometric_features' in candidate:
                features = {
                    'geometric': candidate.get('geometric_features', {}),
                    'appearance': candidate.get('appearance_features', {}),
                    'shape': candidate.get('shape_features', {}),
                    'spatial': candidate.get('spatial_features', {})
                }
                
                # 验证空间特征是否完整，如果不完整则重新计算
                if not features['spatial'].get('world_coordinates'):
                    bbox = candidate.get('bounding_box', [0, 0, 100, 100])
                    mask = candidate.get('mask', np.zeros((image.shape[0], image.shape[1]), dtype=bool))
                    
                    spatial_features = self.object_analyzer.calculate_3d_spatial_features(
                        mask, depth, waypoint_data, bbox
                    )
                    features['spatial'] = spatial_features
                
                print(f"[ENHANCED_TRACKER] 使用detection_pipeline提取的特征")
                return features
            
            # 🆕 如果没有预提取特征，执行完整特征提取（备用方案）
            else:
                bbox = candidate.get('bounding_box', [0, 0, 100, 100])
                mask = candidate.get('mask', np.zeros((image.shape[0], image.shape[1]), dtype=bool))
                
                # 调用完整的特征提取管道
                spatial_features = self.object_analyzer.calculate_3d_spatial_features(
                    mask, depth, waypoint_data, bbox
                )
                
                # 这里可以调用其他特征提取器
                # geometric_features = self.extract_geometric_features(mask, depth)
                # appearance_features = self.extract_appearance_features(image, mask)
                # shape_features = self.extract_shape_features(mask)
                
                features = {
                    'geometric': {},  # 暂时为空，可以后续添加
                    'appearance': {},
                    'shape': {},
                    'spatial': spatial_features
                }
                
                print(f"[ENHANCED_TRACKER] 执行完整特征提取")
                return features
                
        except Exception as e:
            print(f"[ENHANCED_TRACKER] 特征提取失败: {e}")
            return {
                'geometric': {},
                'appearance': {},
                'shape': {},
                'spatial': {}
            }
    
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
            angle = gripper_info.get('angle', 0.0)
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
    
    def _validate_position_continuity(self, candidate_coord: Dict, max_jump: float = 150.0) -> float:
        """验证位置连续性，返回位置合理性分数"""
        try:
            if not self.position_history:
                return 1.0  # 没有历史位置，认为合理
            
            last_known_coord = self.position_history[-1]
            
            distance = math.sqrt(
                (candidate_coord['x'] - last_known_coord['x'])**2 +
                (candidate_coord['y'] - last_known_coord['y'])**2 +
                (candidate_coord['z'] - last_known_coord['z'])**2
            )
            
            print(f"[POSITION_CONTINUITY] 位置跳跃检查: {distance:.1f}mm (阈值: {max_jump}mm)")
            
            # 距离越大，合理性越低
            if distance > max_jump:
                continuity_score = max(0.1, 1.0 - (distance - max_jump) / max_jump)
                print(f"[POSITION_CONTINUITY] 位置跳跃过大，合理性分数: {continuity_score:.3f}")
                return continuity_score
            else:
                print(f"[POSITION_CONTINUITY] 位置变化合理")
                return 1.0
                
        except Exception as e:
            print(f"[POSITION_CONTINUITY] 位置连续性验证失败: {e}")
            return 1.0  # 异常时认为合理

    def _detect_occlusion(self, current_confidence: float, candidate_features: Dict) -> float:
        """检测遮挡情况，返回遮挡分数 (0-1, 1表示严重遮挡)"""
        try:
            occlusion_score = 0.0
            
            # 1. 置信度突然下降
            if len(self.confidence_history) >= 2:
                confidence_drop = self.confidence_history[-1] - current_confidence
                if confidence_drop > 0.2:  # 置信度下降超过0.2
                    occlusion_score += 0.4
                    print(f"[OCCLUSION] 检测到置信度突然下降: {confidence_drop:.3f}")
            
            # 2. 外观特征异常
            appearance_features = candidate_features.get('appearance', {})
            if appearance_features:
                # 检查亮度变化
                mean_brightness = (appearance_features.get('mean_r', 128) + 
                                 appearance_features.get('mean_g', 128) + 
                                 appearance_features.get('mean_b', 128)) / 3
                
                if mean_brightness < 80:  # 亮度过低，可能被遮挡
                    occlusion_score += 0.3
                    print(f"[OCCLUSION] 检测到亮度异常: {mean_brightness:.1f}")
            
            # 3. 形状特征异常（如果有的话）
            shape_features = candidate_features.get('shape', {})
            if shape_features and hasattr(self, 'last_shape_features'):
                # 简单的形状变化检测
                shape_change = abs(shape_features.get('circularity', 0.5) - 
                                 self.last_shape_features.get('circularity', 0.5))
                if shape_change > 0.3:
                    occlusion_score += 0.2
                    print(f"[OCCLUSION] 检测到形状异常变化: {shape_change:.3f}")
            
            self.last_shape_features = shape_features.copy() if shape_features else {}
            
            occlusion_score = min(1.0, occlusion_score)
            if occlusion_score > 0.3:
                print(f"[OCCLUSION] 遮挡分数: {occlusion_score:.3f}")
            
            return occlusion_score
            
        except Exception as e:
            print(f"[OCCLUSION] 遮挡检测失败: {e}")
            return 0.0