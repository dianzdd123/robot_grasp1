# detection/enhanced_detection_pipeline.py
import os
import cv2
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import time
import json

from .features.shape_features import EnhancedShapeFeatureExtractor, FeatureQualityAssessor
from .features.color_features import ColorFeatureExtractor
from .features.spatial_features import SpatialFeatureExtractor
from .utils.coordinate_calculator import CoordinateCalculator, ObjectAnalyzer, AdaptiveThresholdManager
from .utils.config_manager import ConfigManager
from .utils.model_factory import ModelFactory
from .utils.detection_post_processor import Detection3DPostProcessor
class EnhancedDetectionPipeline:
    """增强的检测管道 - 集成3D点云特征和自适应学习"""
    
    def __init__(self, config_file: str = None, output_dir: str = None):
        """初始化增强检测管道"""
        # 配置管理
        self.config_manager = ConfigManager(config_file)
        self.config = self.config_manager.config
        
        # 输出目录
        self.output_dir = output_dir or f"detection_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 初始化核心组件
        self._initialize_models()
        self._initialize_enhanced_components()
        
        # 数据存储
        self.reference_library = {}
        self.selected_tracking_ids = []
        self.next_object_id = {}
        self.post_processor = Detection3DPostProcessor(self.coordinate_calculator)
        
        #  后处理配置
        self.enable_3d_post_processing = True  # 可以通过配置文件控制
        
        print(f"[ENHANCED_PIPELINE] 增强检测管道初始化完成")
        print(f"[ENHANCED_PIPELINE] 输出目录: {self.output_dir}")
    
    def _initialize_models(self):
        """初始化检测和分割模型"""
        try:
            detector_config = self.config_manager.get_detector_config().copy()
            segmentor_config = self.config_manager.get_segmentor_config().copy()
            
            self.detector, self.segmentor = ModelFactory.create_from_config(
                detector_config, segmentor_config
            )
            
            print("[ENHANCED_PIPELINE] 模型初始化成功")
            
        except Exception as e:
            raise RuntimeError(f"模型初始化失败: {e}") from e
    
    def _initialize_enhanced_components(self):
        """初始化增强组件"""
        # 获取配置
        features_config = self.config_manager.get_features_config()
        camera_config = self.config_manager.get_camera_config()
        
        # 坐标计算器
        calibration_data = {
            'camera_intrinsics': camera_config.get('intrinsics', {}),
            'hand_eye_translation': camera_config.get('hand_eye_translation'),
            'hand_eye_quaternion': camera_config.get('hand_eye_quaternion')
        }
        self.coordinate_calculator = CoordinateCalculator(calibration_data)
        
        # 物体分析器
        self.object_analyzer = ObjectAnalyzer(self.coordinate_calculator)
        
        # 增强特征提取器
        camera_intrinsics = camera_config.get('intrinsics', {})
        self.enhanced_shape_extractor = EnhancedShapeFeatureExtractor(camera_intrinsics)
        
        # 传统特征提取器（保留）
        color_config = features_config.get('color', {})
        self.color_extractor = ColorFeatureExtractor(
            bins=color_config.get('histogram_bins', 32)
        )
        self.spatial_extractor = SpatialFeatureExtractor(camera_intrinsics)
        
        # 特征质量评估器
        self.quality_assessor = FeatureQualityAssessor()
        
        # 自适应阈值管理器
        self.threshold_manager = AdaptiveThresholdManager()
        
        print("[ENHANCED_PIPELINE] 增强组件初始化完成")
    
    def build_reference_library(self, image_rgb: np.ndarray, 
                            depth_image: np.ndarray,
                            waypoint_data: Dict,
                            generate_visualization: bool = True) -> Dict:
        """构建参考特征库 - 集成3D后处理"""
        print("[ENHANCED_PIPELINE] Starting reference library construction...")
        start_time = time.time()
        
        try:
            # 1. YOLO检测
            boxes, class_ids, confidences = self.detector.detect(image_rgb)
            print(f"[ENHANCED_PIPELINE] YOLO detected {len(boxes)} targets")
            
            if len(boxes) == 0:
                return {
                    'success': True,
                    'reference_library': {},
                    'detection_count': 0,
                    'processing_time': time.time() - start_time,
                    'message': 'No targets detected'
                }
            
            # 2. SAM2分割
            masks = self.segmentor.segment(image_rgb, boxes)
            print(f"[ENHANCED_PIPELINE] SAM2 segmentation completed")
            
            # 3.  构建初始检测结果（用于后处理）
            initial_detections = []
            class_names = self.detector.get_class_names()
            
            for i, (box, class_id, confidence, mask) in enumerate(zip(boxes, class_ids, confidences, masks)):
                class_name = class_names.get(class_id, f'class_{class_id}')
                detection = {
                    'bounding_box': box.tolist(),
                    'class_id': int(class_id),
                    'class_name': class_name,
                    'confidence': float(confidence),
                    'mask': mask,
                    'original_index': i
                }
                initial_detections.append(detection)
            
            # 4.  3D后处理（过滤重复检测）
            if self.enable_3d_post_processing and depth_image is not None and len(initial_detections) > 1:
                print(f"[ENHANCED_PIPELINE] Applying 3D post-processing to {len(initial_detections)} detections...")
                filtered_detections = self.post_processor.process_detections(
                    initial_detections, image_rgb, depth_image, waypoint_data
                )
                print(f"[ENHANCED_PIPELINE] Post-processing: {len(initial_detections)} -> {len(filtered_detections)} detections")
            else:
                filtered_detections = initial_detections
                print("[ENHANCED_PIPELINE] 3D post-processing skipped")
            
            # 5. 构建参考特征库（使用过滤后的检测结果）
            reference_library = {}
            visualization_objects = []
            
            for i, detection in enumerate(filtered_detections):
                try:
                    # 分配对象ID
                    object_id = self._assign_object_id(detection['class_id'])
                    class_name = detection['class_name']
                    full_object_id = f"{class_name}_{object_id}"
                    
                    # 提取多层次特征
                    features = self._extract_enhanced_features(
                        image_rgb, detection['mask'], depth_image, waypoint_data, detection['bounding_box']
                    )
                    
                    # 评估特征质量
                    quality_score = self.quality_assessor.assess_feature_quality(features)
                    
                    # 生成描述
                    description = self._generate_enhanced_description(
                        class_name, features, object_id
                    )
                    
                    #  添加后处理信息
                    post_processing_info = {
                        'was_merged': detection.get('merged_from', 1) > 1,
                        'merged_from_count': detection.get('merged_from', 1),
                        'original_confidences': detection.get('original_confidences', [detection['confidence']]),
                        'post_processed': self.enable_3d_post_processing
                    }
                    
                    # 构建参考特征条目
                    reference_entry = {
                        'features': features,
                        'quality_score': quality_score,
                        'post_processing_info': post_processing_info,  #  后处理信息
                        'metadata': {
                            'object_id': full_object_id,
                            'class_id': int(detection['class_id']),
                            'class_name': class_name,
                            'confidence': float(detection['confidence']),
                            'bounding_box': detection['bounding_box'],
                            'description': description,
                            'detection_timestamp': datetime.now().isoformat(),
                            'waypoint_info': {
                                'world_pos': waypoint_data['world_pos'],
                                'orientation': [waypoint_data['roll'], waypoint_data['pitch'], waypoint_data['yaw']]
                            }
                        }
                    }
                    
                    reference_library[full_object_id] = reference_entry
                    
                    # 为可视化准备对象信息
                    viz_obj = {
                        'object_id': full_object_id,
                        'class_id': int(detection['class_id']),
                        'class_name': class_name,
                        'confidence': float(detection['confidence']),
                        'bounding_box': detection['bounding_box'],
                        'mask': detection['mask'],
                        'features': features,
                        'description': description,
                        'quality_score': quality_score,
                        'post_processing_info': post_processing_info  #  传递给可视化
                    }
                    visualization_objects.append(viz_obj)
                    
                    print(f"[ENHANCED_PIPELINE] Built reference entry: {full_object_id} (quality: {quality_score:.1f}%)")
                    
                    #  记录合并信息
                    if post_processing_info['was_merged']:
                        print(f"[ENHANCED_PIPELINE] --> Merged from {post_processing_info['merged_from_count']} original detections")
                        print(f"[ENHANCED_PIPELINE] --> Original confidences: {post_processing_info['original_confidences']}")
                    
                except Exception as e:
                    print(f"[ENHANCED_PIPELINE] Error processing detection {i}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
            
            # 6. 保存参考特征库
            self._save_reference_library(reference_library)
            
            # 7. 生成可视化
            visualization_image = None
            if generate_visualization and len(visualization_objects) > 0:
                print("[ENHANCED_PIPELINE] Generating enhanced visualization...")
                visualization_image = self._generate_enhanced_visualization(image_rgb, visualization_objects)
                
                if visualization_image is not None:
                    vis_filename = os.path.join(self.output_dir, "detection_visualization.jpg")
                    success = cv2.imwrite(vis_filename, cv2.cvtColor(visualization_image, cv2.COLOR_RGB2BGR))
                    if success:
                        print(f"[ENHANCED_PIPELINE] Visualization saved: {vis_filename}")
            
            result = {
                'success': True,
                'reference_library': reference_library,
                'detection_count': len(reference_library),
                'processing_time': time.time() - start_time,
                'visualization_image': visualization_image,
                'post_processing_stats': {  #  后处理统计
                    'original_detections': len(initial_detections),
                    'filtered_detections': len(filtered_detections),
                    'duplicates_removed': len(initial_detections) - len(filtered_detections),
                    'post_processing_enabled': self.enable_3d_post_processing
                },
                'message': f'Successfully built {len(reference_library)} reference features'
            }
            
            # 存储到实例变量
            self.reference_library = reference_library
            
            print(f"[ENHANCED_PIPELINE] Reference library construction completed: {len(reference_library)} targets")
            
            #  显示后处理摘要
            self._log_post_processing_summary(result['post_processing_stats'], filtered_detections)
            
            return result
            
        except Exception as e:
            print(f"[ENHANCED_PIPELINE] Reference library construction failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'reference_library': {},
                'detection_count': 0,
                'processing_time': time.time() - start_time,
                'message': f'Construction failed: {str(e)}'
            }

    def _log_post_processing_summary(self, stats: Dict, filtered_detections: List[Dict]):
        """记录后处理摘要"""
        try:
            print(f"\n[POST_PROCESSING_SUMMARY]")
            print(f"Original YOLO detections: {stats['original_detections']}")
            print(f"After 3D post-processing: {stats['filtered_detections']}")
            print(f"Duplicates removed: {stats['duplicates_removed']}")
            print(f"Post-processing enabled: {stats['post_processing_enabled']}")
            
            if stats['duplicates_removed'] > 0:
                print(f" Successfully removed {stats['duplicates_removed']} duplicate detection(s)")
                
                # 显示合并的检测信息
                merged_count = 0
                for detection in filtered_detections:
                    if detection.get('merged_from', 1) > 1:
                        merged_count += 1
                        print(f"   -> {detection['class_name']} (merged from {detection['merged_from']} detections)")
                
                if merged_count > 0:
                    print(f" {merged_count} detection(s) were merged from duplicates")
            
            print(f"[POST_PROCESSING_SUMMARY] Complete\n")
            
        except Exception as e:
            print(f"[POST_PROCESSING_SUMMARY] Logging failed: {e}")

    def _generate_enhanced_visualization(self, image_rgb: np.ndarray, objects: List[Dict]) -> np.ndarray:
        """生成增强可视化 - 包含后处理信息"""
        try:
            print(f"[VISUALIZATION] Generating enhanced visualization for {len(objects)} objects")
            
            # 亮度增强
            vis_image = image_rgb.copy().astype(np.float32)
            mean_brightness = np.mean(vis_image)
            if mean_brightness < 120:
                vis_image = np.clip(vis_image * 1.2, 0, 255)
            vis_image = vis_image.astype(np.uint8)
            
            # 创建统一的mask覆盖层
            mask_overlay = np.zeros_like(vis_image, dtype=np.float32)
            combined_mask = np.zeros((vis_image.shape[0], vis_image.shape[1]), dtype=bool)
            
            # 颜色调色板
            colors = [
                (255, 120, 120), (120, 255, 120), (120, 180, 255), (255, 255, 120),
                (255, 120, 255), (120, 255, 255), (255, 180, 120), (200, 255, 180)
            ]
            
            valid_objects = []
            for i, obj in enumerate(objects):
                mask = obj.get('mask')
                if mask is not None and isinstance(mask, np.ndarray):
                    mask_bool = mask > 0.5 if mask.dtype != bool else mask
                    if mask_bool.shape[:2] == vis_image.shape[:2]:
                        #  为合并的检测使用特殊颜色
                        post_info = obj.get('post_processing_info', {})
                        if post_info.get('was_merged', False):
                            # 合并的检测使用更亮的颜色
                            color = tuple(min(255, c + 30) for c in colors[i % len(colors)])
                        else:
                            color = colors[i % len(colors)]
                        
                        mask_overlay[mask_bool] = color
                        combined_mask = combined_mask | mask_bool
                        valid_objects.append((i, obj, mask_bool, color))
            
            # 应用浅色mask覆盖
            if len(valid_objects) > 0:
                alpha = 0.3
                vis_image_float = vis_image.astype(np.float32)
                vis_image_float[combined_mask] = (vis_image_float[combined_mask] * (1 - alpha) + 
                                                mask_overlay[combined_mask] * alpha)
                vis_image = np.clip(vis_image_float, 0, 255).astype(np.uint8)
            
            # 绘制对象
            font = cv2.FONT_HERSHEY_SIMPLEX
            for i, obj, mask_bool, color in valid_objects:
                # 计算mask中心点
                center_x, center_y = self._calculate_mask_center(mask_bool)
                bbox = obj['bounding_box']
                x1, y1, x2, y2 = map(int, bbox)
                
                #  为合并的检测绘制特殊边框
                post_info = obj.get('post_processing_info', {})
                if post_info.get('was_merged', False):
                    # 双重边框表示合并的检测
                    cv2.rectangle(vis_image, (x1-2, y1-2), (x2+2, y2+2), (255, 255, 255), 2)
                    cv2.rectangle(vis_image, (x1, y1), (x2, y2), color, 3)
                else:
                    cv2.rectangle(vis_image, (x1, y1), (x2, y2), color, 3)
                
                # 绘制中心点
                cv2.circle(vis_image, (center_x, center_y), 12, color, -1)
                cv2.circle(vis_image, (center_x, center_y), 15, (255, 255, 255), 2)
                
                # 绘制编号
                number_text = str(i + 1)
                text_size = cv2.getTextSize(number_text, font, 0.8, 2)[0]
                text_x = center_x - text_size[0] // 2
                text_y = center_y + text_size[1] // 2
                cv2.putText(vis_image, number_text, (text_x, text_y), font, 0.8, (0, 0, 0), 3)
                cv2.putText(vis_image, number_text, (text_x, text_y), font, 0.8, (255, 255, 255), 2)
                
                # 生成英文描述
                description = self._generate_english_description(obj)
                
                #  为合并的检测添加标记
                if post_info.get('was_merged', False):
                    description += f" [M{post_info['merged_from_count']}]"
                
                # 智能标签位置
                label_positions = [(x1, y1 - 10), (x1, y2 + 25), (x2 + 10, y1 + 20)]
                label_x, label_y = label_positions[0]
                for pos_x, pos_y in label_positions:
                    if pos_x >= 0 and pos_y >= 20 and pos_x + 300 < vis_image.shape[1]:
                        label_x, label_y = pos_x, pos_y
                        break
                
                # 绘制标签
                label_width = len(description) * 8
                cv2.rectangle(vis_image, (label_x - 3, label_y - 18), 
                            (label_x + label_width, label_y + 8), color, -1)
                cv2.putText(vis_image, description, (label_x, label_y), 
                        font, 0.5, (255, 255, 255), 1)
            
            #  添加后处理信息到图像底部
            self._add_post_processing_info_panel(vis_image, objects)
            
            return vis_image
            
        except Exception as e:
            print(f"[VISUALIZATION] Generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    def _add_post_processing_info_panel(self, vis_image: np.ndarray, objects: List[Dict]):
        """添加后处理信息面板"""
        try:
            # 统计后处理信息
            total_objects = len(objects)
            merged_objects = sum(1 for obj in objects 
                            if obj.get('post_processing_info', {}).get('was_merged', False))
            
            if merged_objects > 0:
                # 在图像底部添加信息条
                panel_height = 40
                panel_y = vis_image.shape[0] - panel_height
                
                # 创建半透明背景
                overlay = vis_image.copy()
                cv2.rectangle(overlay, (0, panel_y), (vis_image.shape[1], vis_image.shape[0]), 
                            (50, 50, 50), -1)
                cv2.addWeighted(overlay, 0.8, vis_image, 0.2, 0, vis_image)
                
                # 添加文字信息
                font = cv2.FONT_HERSHEY_SIMPLEX
                info_text = f"3D Post-Processing: {merged_objects}/{total_objects} objects merged from duplicates"
                
                cv2.putText(vis_image, info_text, (10, panel_y + 25), 
                        font, 0.6, (255, 255, 255), 2)
                
                # 添加图例
                legend_text = "[M#] = Merged from # detections"
                cv2.putText(vis_image, legend_text, (vis_image.shape[1] - 300, panel_y + 25), 
                        font, 0.5, (200, 200, 200), 1)
            
        except Exception as e:
            print(f"[POST_PROCESSING_INFO] Adding info panel failed: {e}")

    # 4. 🆕 添加配置方法
    def set_post_processing_config(self, config: Dict):
        """设置后处理配置"""
        try:
            if hasattr(self, 'post_processor'):
                # 更新后处理器参数
                if 'spatial_distance_threshold' in config:
                    self.post_processor.spatial_distance_threshold = config['spatial_distance_threshold']
                if 'depth_similarity_threshold' in config:
                    self.post_processor.depth_similarity_threshold = config['depth_similarity_threshold']
                if 'mask_overlap_threshold' in config:
                    self.post_processor.mask_overlap_threshold = config['mask_overlap_threshold']
                if 'height_similarity_threshold' in config:
                    self.post_processor.height_similarity_threshold = config['height_similarity_threshold']
                
                print(f"[ENHANCED_PIPELINE] Post-processing config updated: {config}")
        
        except Exception as e:
            print(f"[ENHANCED_PIPELINE] Post-processing config update failed: {e}")
    def _calculate_mask_center(self, mask: np.ndarray) -> Tuple[int, int]:
        """计算mask的几何中心点"""
        try:
            # 找到mask的所有像素
            mask_indices = np.where(mask > 0)
            if len(mask_indices[0]) == 0:
                return 100, 100
            
            # 计算质心
            center_y = int(np.mean(mask_indices[0]))
            center_x = int(np.mean(mask_indices[1]))
            
            # 确保在图像范围内
            center_x = max(10, min(mask.shape[1] - 10, center_x))
            center_y = max(10, min(mask.shape[0] - 10, center_y))
            
            return center_x, center_y
            
        except Exception:
            return 100, 100

    def _generate_english_description(self, obj: Dict) -> str:
        """生成简洁的英文描述"""
        try:
            features = obj.get('features', {})
            class_name = obj['class_name']
            confidence = obj['confidence']
            
            # 颜色信息
            color_name = features.get('appearance', {}).get('color_name', '')
            if color_name and color_name != 'unknown':
                color_desc = color_name.capitalize()
            else:
                color_desc = ''
            
            # 高度信息
            height_mm = features.get('spatial', {}).get('height_mm', 0)
            if height_mm > 0:
                height_desc = f"{height_mm:.0f}mm"
            else:
                height_desc = ''
            
            # 组合描述
            parts = []
            if color_desc:
                parts.append(color_desc)
            parts.append(class_name)
            if height_desc:
                parts.append(f"h:{height_desc}")
            parts.append(f"conf:{confidence:.2f}")
            
            return ' '.join(parts)
            
        except Exception:
            return f"{obj.get('class_name', 'object')} conf:{obj.get('confidence', 0):.2f}"


    def _add_info_panel(self, vis_image: np.ndarray, objects: List[Dict]):
        """在图像上添加信息面板"""
        try:
            # 在图像底部添加信息条
            panel_height = 60
            panel_y = vis_image.shape[0] - panel_height
            
            # 创建半透明背景
            overlay = vis_image.copy()
            cv2.rectangle(overlay, (0, panel_y), (vis_image.shape[1], vis_image.shape[0]), 
                        (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.7, vis_image, 0.3, 0, vis_image)
            
            # 添加文字信息
            font = cv2.FONT_HERSHEY_SIMPLEX
            info_text = f"Enhanced Detection: {len(objects)} objects detected"
            avg_quality = np.mean([obj.get('quality_score', 0) for obj in objects])
            quality_text = f"Avg Feature Quality: {avg_quality:.1f}%"
            
            cv2.putText(vis_image, info_text, (10, panel_y + 20), 
                    font, 0.6, (255, 255, 255), 2)
            cv2.putText(vis_image, quality_text, (10, panel_y + 40), 
                    font, 0.6, (255, 255, 255), 2)
            
            # 在右侧添加时间戳
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(vis_image, timestamp, (vis_image.shape[1] - 200, panel_y + 30), 
                    font, 0.5, (200, 200, 200), 1)
            
        except Exception as e:
            print(f"[INFO_PANEL] 添加信息面板失败: {e}")


    # def _calculate_3d_center_point(self, mask: np.ndarray, features: Dict) -> Tuple[int, int]:
    #     """
    #     计算物体的3D中心点在2D图像中的投影位置
        
    #     Args:
    #         mask: 物体mask
    #         features: 物体特征（包含3D信息）
            
    #     Returns:
    #         center_x, center_y: 3D中心点的2D投影坐标
    #     """
    #     try:
    #         # 方法1: 如果有3D空间信息，优先使用
    #         spatial_features = features.get('spatial', {})
            
    #         # 检查是否有3D质心信息
    #         centroid_3d_camera = spatial_features.get('centroid_3d_camera')
    #         if centroid_3d_camera and len(centroid_3d_camera) == 3:
    #             # 如果有相机坐标系的3D质心，投影到2D
    #             cam_x, cam_y, cam_z = centroid_3d_camera
                
    #             # 使用相机内参投影到2D（需要相机内参）
    #             fx = getattr(self, 'camera_fx', 912.7)  # 默认焦距
    #             fy = getattr(self, 'camera_fy', 910.3)
    #             cx = getattr(self, 'camera_cx', 624.0)
    #             cy = getattr(self, 'camera_cy', 320.7)
                
    #             if cam_z > 0.01:  # 有效深度
    #                 pixel_x = int(cam_x * fx / cam_z + cx)
    #                 pixel_y = int(cam_y * fy / cam_z + cy)
                    
    #                 # 检查投影点是否在图像范围内
    #                 if (0 <= pixel_x < mask.shape[1] and 0 <= pixel_y < mask.shape[0]):
    #                     print(f"[3D_CENTER] 使用3D质心投影: ({pixel_x}, {pixel_y})")
    #                     return pixel_x, pixel_y
            
    #         # 方法2: 使用2D质心但考虑高度信息调整
    #         mask_indices = np.where(mask > 0)
    #         if len(mask_indices[0]) > 0:
    #             # 基础2D质心
    #             centroid_2d_y = np.mean(mask_indices[0])
    #             centroid_2d_x = np.mean(mask_indices[1])
                
    #             # 获取物体高度信息
    #             height_mm = spatial_features.get('height_mm', 0)
                
    #             # 根据高度调整Y坐标（高物体中心点稍微上移）
    #             if height_mm > 50:  # 高物体（>50mm）
    #                 # 向上偏移，偏移量与高度成正比
    #                 height_offset = min(0, height_mm / 5)  # 最多上移20像素
    #                 centroid_2d_y -= height_offset
    #                 print(f"[3D_CENTER] 高物体调整: 高度{height_mm}mm, 上移{height_offset}像素")
                
    #             center_x = int(centroid_2d_x)
    #             center_y = int(centroid_2d_y)
                
    #             print(f"[3D_CENTER] 使用2D质心+高度调整: ({center_x}, {center_y})")
    #             return center_x, center_y
            
    #         # 方法3: fallback到bbox中心
    #         bbox = features.get('bbox', [0, 0, 100, 100])
    #         if len(bbox) >= 4:
    #             center_x = int((bbox[0] + bbox[2]) / 2)
    #             center_y = int((bbox[1] + bbox[3]) / 2)
    #             print(f"[3D_CENTER] 使用bbox中心: ({center_x}, {center_y})")
    #             return center_x, center_y
            
    #         # 默认返回
    #         return 100, 100
            
    #     except Exception as e:
    #         print(f"[3D_CENTER] 计算3D中心点失败: {e}")
    #         # fallback到mask质心
    #         mask_indices = np.where(mask > 0)
    #         if len(mask_indices[0]) > 0:
    #             return int(np.mean(mask_indices[1])), int(np.mean(mask_indices[0]))
    #         return 100, 100
    
    def _extract_enhanced_features(self, image_rgb: np.ndarray, mask: np.ndarray,
                                depth_image: np.ndarray, waypoint_data: Dict,
                                bbox: List[int]) -> Dict:
        """提取增强的多层次特征 - 调试版本"""
        features = {}
        
        try:
            print(f"[FEATURES] 开始提取特征，输入: image{image_rgb.shape}, mask{mask.shape}, depth{depth_image.shape if depth_image is not None else None}")
            
            # 1. 几何特征（最稳定 - 权重最高）
            if depth_image is not None:
                #print("[FEATURES] 开始提取几何特征...")
                try:
                    geometric_features = self.enhanced_shape_extractor.extract_all_features(
                        mask, depth_image, waypoint_data
                    )
                    features['geometric'] = geometric_features
                    print(f"[FEATURES] 几何特征提取完成: {list(geometric_features.keys())}")
                    
                    # # 调试输出几何特征的内容
                    # for key, value in geometric_features.items():
                    #     if isinstance(value, list):
                    #         print(f"[FEATURES] {key}: list长度={len(value)}, 非零={sum(1 for x in value if abs(x) > 1e-6)}")
                    #     elif isinstance(value, dict):
                    #         print(f"[FEATURES] {key}: dict键={list(value.keys())}")
                    #     else:
                    #         print(f"[FEATURES] {key}: {type(value)}")
                            
                except Exception as e:
                    #print(f"[FEATURES] 几何特征提取失败: {e}")
                    import traceback
                    traceback.print_exc()
                    features['geometric'] = {}
            else:
                ##print("[FEATURES] 无深度数据，跳过几何特征提取")
                features['geometric'] = {}
            
            # 2. 形状特征（中等稳定）
            #print("[FEATURES] 开始提取形状特征...")
            try:
                shape_features = self.enhanced_shape_extractor._extract_2d_shape_features(mask)
                features['shape'] = shape_features
                #print(f"[FEATURES] 形状特征提取完成: {list(shape_features.keys())}")
            except Exception as e:
                #print(f"[FEATURES] 形状特征提取失败: {e}")
                features['shape'] = {}
            
            # 3. 外观特征（较不稳定 - 权重较低）
            ##print("[FEATURES] 开始提取外观特征...")
            try:
                color_stats = self.color_extractor.get_color_statistics(image_rgb, mask)
                # 使用改进的颜色直方图
                improved_histogram = self._extract_improved_color_histogram(image_rgb, mask)
                color_stats['histogram'] = improved_histogram
                color_stats['color_name'] = self._improve_color_detection(image_rgb, mask)
                features['appearance'] = color_stats
                # print(f"[FEATURES] 外观特征提取完成: 颜色={color_stats.get('color_name', 'unknown')}")
            except Exception as e:
                # print(f"[FEATURES] 外观特征提取失败: {e}")
                features['appearance'] = {}
            
            # 4. 空间上下文特征（辅助信息）
            #print("[FEATURES] 开始提取空间特征...")
            try:
                if depth_image is not None and waypoint_data is not None:
                    spatial_features = self.object_analyzer.calculate_3d_spatial_features(
                        mask, depth_image, waypoint_data, bbox
                    )
                    
                    # 添加高度和背景信息
                    height_info = self.object_analyzer.calculate_object_height_and_background(
                        mask, depth_image, bbox, waypoint_data
                    )
                    spatial_features.update(height_info)
                    
                    features['spatial'] = spatial_features
                    #print(f"[FEATURES] 空间特征提取完成: 3D坐标={spatial_features.get('world_coordinates', 'N/A')}")
                else:
                    # 基本的2D空间信息
                    ys, xs = np.where(mask > 0)
                    if len(xs) > 0:
                        centroid_x, centroid_y = np.mean(xs), np.mean(ys)
                        image_height, image_width = mask.shape
                        norm_x = centroid_x / image_width
                        norm_y = centroid_y / image_height
                        
                        region_position = self.spatial_extractor._determine_region_position(norm_x, norm_y)
                        
                        features['spatial'] = {
                            'centroid_2d': (centroid_x, centroid_y),
                            'normalized_coords': (norm_x, norm_y),
                            'region_position': region_position
                        }
                        #print(f"[FEATURES] 2D空间特征提取完成: 质心=({centroid_x:.1f},{centroid_y:.1f})")
            except Exception as e:
                #print(f"[FEATURES] 空间特征提取失败: {e}")
                import traceback
                traceback.print_exc()
                features['spatial'] = {}
            
            #print(f"[FEATURES] 特征提取完成，总类型数: {len(features)}")
            
        except Exception as e:
            #print(f"[FEATURES] 特征提取整体失败: {e}")
            import traceback
            traceback.print_exc()
            features['extraction_error'] = str(e)
        
        return features
    
    def _extract_improved_color_histogram(self, image: np.ndarray, mask: np.ndarray, bins: int = 32) -> List[float]:
        """改进的颜色直方图提取"""
        if mask.dtype != bool:
            mask = mask > 0.5
        
        masked_pixels = image[mask]
        if len(masked_pixels) == 0:
            return [0.0] * (bins * 3)
        
        # 分别计算RGB三个通道的直方图
        hist_r = np.histogram(masked_pixels[:, 0], bins=bins, range=(0, 256))[0]
        hist_g = np.histogram(masked_pixels[:, 1], bins=bins, range=(0, 256))[0]
        hist_b = np.histogram(masked_pixels[:, 2], bins=bins, range=(0, 256))[0]
        
        # 归一化直方图
        hist_r = hist_r / (np.sum(hist_r) + 1e-10)
        hist_g = hist_g / (np.sum(hist_g) + 1e-10)
        hist_b = hist_b / (np.sum(hist_b) + 1e-10)
        
        return np.concatenate([hist_r, hist_g, hist_b]).tolist()
    
    def _improve_color_detection(self, image: np.ndarray, mask: np.ndarray) -> str:
        """改进的颜色检测"""
        if np.sum(mask) == 0:
            return "unknown"
        
        masked_pixels = image[mask > 0]
        if len(masked_pixels) == 0:
            return "unknown"
        
        # 使用中位数而不是平均值
        median_color = np.median(masked_pixels, axis=0)
        
        # 转换为HSV进行颜色分类
        hsv_color = cv2.cvtColor(np.uint8([[median_color]]), cv2.COLOR_RGB2HSV)[0][0]
        h, s, v = hsv_color
        
        # 改进的颜色分类逻辑
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
            return "yellow" if median_color[0] > 180 and median_color[1] > 150 else "orange"
        elif 35 <= h < 85:
            return "green"
        elif 85 <= h < 125:
            return "cyan"
        elif 125 <= h < 165:
            return "blue"
        
        return "mixed"
    
    def _assign_object_id(self, class_id: int) -> int:
        """为对象分配ID"""
        if class_id not in self.next_object_id:
            self.next_object_id[class_id] = 0
        else:
            self.next_object_id[class_id] += 1
        
        return self.next_object_id[class_id]
    
    def _generate_enhanced_description(self, class_name: str, features: Dict, object_id: int) -> str:
        """生成增强描述"""
        try:
            # 基础信息
            description_parts = []
            
            # 颜色信息
            color_name = features.get('appearance', {}).get('color_name', 'unknown')
            if color_name and color_name != 'unknown':
                description_parts.append(color_name.capitalize())
            
            # 对象名称
            description_parts.append(class_name)
            
            # 高度信息
            height_mm = features.get('spatial', {}).get('height_mm')
            if height_mm is not None:
                if height_mm < 20:
                    description_parts.append("(flat)")
                elif height_mm < 80:
                    description_parts.append("(low)")
                elif height_mm < 120:
                    description_parts.append("(medium height)")
                else:
                    description_parts.append("(tall)")
            
            # 距离信息
            distance = features.get('spatial', {}).get('distance_to_camera')
            if distance is not None:
                if distance < 0.3:
                    description_parts.append("nearby")
                elif distance < 0.6:
                    description_parts.append("at medium distance")
                else:
                    description_parts.append("far")
            
            enhanced_description = ' '.join(description_parts)
            
            # 添加技术信息
            tech_info = []
            if height_mm is not None:
                tech_info.append(f"h={height_mm:.1f}mm")
            if distance is not None:
                tech_info.append(f"d={distance*1000:.0f}mm")
            
            # 添加质量信息
            quality_score = self.quality_assessor.assess_feature_quality(features)
            tech_info.append(f"q={quality_score:.0f}%")
            
            if tech_info:
                enhanced_description += f" [{', '.join(tech_info)}]"
            
            return enhanced_description
            
        except Exception as e:
            print(f"[ENHANCED_PIPELINE] 描述生成失败: {e}")
            return f"{class_name}_{object_id}"
    
    def _save_reference_library(self, reference_library: Dict):
        """保存参考特征库"""
        try:
            # 创建可序列化的数据
            serializable_library = {}
            
            for obj_id, entry in reference_library.items():
                # 深拷贝并处理numpy数组
                serializable_entry = {
                    'features': self._sanitize_features_for_json(entry['features']),
                    'quality_score': float(entry['quality_score']),
                    'metadata': entry['metadata']
                }
                serializable_library[obj_id] = serializable_entry
            
            # 保存主要数据文件
            library_file = os.path.join(self.output_dir, "reference_library.json")
            with open(library_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_library, f, indent=2, ensure_ascii=False)
            
            # 保存摘要文件
            self._save_library_summary(reference_library)
            
            print(f"[ENHANCED_PIPELINE] 参考特征库已保存到: {library_file}")
            
        except Exception as e:
            print(f"[ENHANCED_PIPELINE] 保存参考特征库失败: {e}")
    
    def _sanitize_features_for_json(self, features: Dict) -> Dict:
        """清理特征数据用于JSON序列化"""
        sanitized = {}
        
        for feature_type, feature_data in features.items():
            if isinstance(feature_data, dict):
                sanitized[feature_type] = {}
                for key, value in feature_data.items():
                    if isinstance(value, np.ndarray):
                        sanitized[feature_type][key] = value.tolist()
                    elif isinstance(value, (np.integer, np.floating)):
                        sanitized[feature_type][key] = float(value)
                    elif isinstance(value, tuple):
                        sanitized[feature_type][key] = list(value)
                    else:
                        sanitized[feature_type][key] = value
            elif isinstance(feature_data, np.ndarray):
                sanitized[feature_type] = feature_data.tolist()
            elif isinstance(feature_data, (np.integer, np.floating)):
                sanitized[feature_type] = float(feature_data)
            else:
                sanitized[feature_type] = feature_data
        
        return sanitized
    
    def _save_library_summary(self, reference_library: Dict):
        """保存特征库摘要"""
        try:
            summary_file = os.path.join(self.output_dir, "library_summary.txt")
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("Reference Feature Library Summary\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"Total Objects: {len(reference_library)}\n")
                f.write(f"Creation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # 按类别分组
                by_class = {}
                for obj_id, entry in reference_library.items():
                    class_name = entry['metadata']['class_name']
                    if class_name not in by_class:
                        by_class[class_name] = []
                    by_class[class_name].append((obj_id, entry['quality_score']))
                
                f.write("Objects by Class:\n")
                f.write("-" * 30 + "\n")
                for class_name, objects in by_class.items():
                    avg_quality = np.mean([q for _, q in objects])
                    f.write(f"{class_name}: {len(objects)} objects (avg quality: {avg_quality:.1f}%)\n")
                    for obj_id, quality in objects:
                        f.write(f"  - {obj_id} (quality: {quality:.1f}%)\n")
                    f.write("\n")
            
            print(f"[ENHANCED_PIPELINE] 特征库摘要已保存到: {summary_file}")
            
        except Exception as e:
            print(f"[ENHANCED_PIPELINE] 保存摘要失败: {e}")

    
    def get_reference_library(self) -> Dict:
        """获取参考特征库"""
        return self.reference_library
    
    def get_output_dir(self) -> str:
        """获取输出目录"""
        return self.output_dir
    
    def select_tracking_targets(self) -> bool:
        """选择要追踪的目标"""
        if not hasattr(self, 'reference_library') or not self.reference_library:
            print("[ENHANCED_PIPELINE] 没有参考特征库数据，请先进行检测")
            return False
        
        objects = list(self.reference_library.values())
        
        print(f"\n{'='*50}")
        print("选择追踪目标")
        print(f"{'='*50}")
        
        print("\n检测到的对象:")
        for i, (obj_id, entry) in enumerate(self.reference_library.items(), 1):
            metadata = entry['metadata']
            quality = entry['quality_score']
            print(f"{i:2d}. {metadata['description']} (ID: {obj_id}, 置信度: {metadata['confidence']:.3f}, 质量: {quality:.1f}%)")
        
        print("\n请选择要追踪的对象:")
        print("格式: 输入数字，用逗号分隔 (例如: 1,3,5)")
        
        while True:
            try:
                user_input = input("\n您的选择: ").strip()
                
                if user_input.lower() == 'all':
                    self.selected_tracking_ids = list(self.reference_library.keys())
                    break
                
                indices = [int(x.strip()) for x in user_input.split(',')]
                selected_ids = []
                
                obj_list = list(self.reference_library.keys())
                for idx in indices:
                    if 1 <= idx <= len(obj_list):
                        selected_ids.append(obj_list[idx-1])
                    else:
                        print(f"警告: 索引 {idx} 超出范围")
                
                if selected_ids:
                    self.selected_tracking_ids = selected_ids
                    break
                else:
                    print("没有有效选择，请重试。")
                    
            except ValueError:
                print("输入格式错误，请输入数字，用逗号分隔。")
            except KeyboardInterrupt:
                print("\n选择已取消。")
                return False
        
        print(f"\n已选择的追踪目标:")
        for obj_id in self.selected_tracking_ids:
            entry = self.reference_library[obj_id]
            metadata = entry['metadata']
            print(f"  - {metadata['description']} (ID: {obj_id})")
        
        # 保存选择
        self._save_tracking_selection()
        
        return True

    def _save_tracking_selection(self):
        """保存追踪选择"""
        try:
            selection_file = os.path.join(self.output_dir, "tracking_selection.txt")
            
            with open(selection_file, 'w', encoding='utf-8') as f:
                f.write("选择的追踪目标:\n")
                f.write("=" * 50 + "\n")
                
                for obj_id in getattr(self, 'selected_tracking_ids', []):
                    if obj_id in self.reference_library:
                        entry = self.reference_library[obj_id]
                        metadata = entry['metadata']
                        f.write(f"- {metadata['description']} (ID: {obj_id})\n")
            
            print(f"[ENHANCED_PIPELINE] 追踪选择已保存到: {selection_file}")
            
        except Exception as e:
            print(f"[ENHANCED_PIPELINE] 保存追踪选择失败: {e}")

    def get_selected_tracking_ids(self) -> List[str]:
        """获取选择的追踪目标ID"""
        return getattr(self, 'selected_tracking_ids', [])
    
    def _display_and_publish_visualization(self, vis_image: np.ndarray, output_dir: str):
        """显示和发布可视化图像"""
        try:
            if vis_image is None:
                print("[DISPLAY] 可视化图像为空，跳过显示")
                return
            
            # 保存图像
            vis_file = os.path.join(output_dir, "detection_visualization.jpg")
            success = cv2.imwrite(vis_file, cv2.cvtColor(vis_image, cv2.COLOR_RGB2BGR))
            
            if success:
                print(f"[DISPLAY]  可视化图像已保存: {vis_file}")
            else:
                print(f"[DISPLAY]  可视化图像保存失败: {vis_file}")
                return
            
            # 🖼️ 尝试显示图像
            self._show_visualization_popup(vis_image)
            
            # 📡 发布ROS可视化消息
            self._publish_visualization_message(vis_image)
            
        except Exception as e:
            print(f"[DISPLAY] 显示和发布可视化失败: {e}")

    def _show_visualization_popup(self, vis_image: np.ndarray):
        """显示可视化弹窗"""
        try:
            import os
            
            # 检查显示环境
            display_mode = os.environ.get('VISION_AI_DISPLAY', 'auto')
            
            if display_mode == 'off':
                print("[DISPLAY] 显示功能已禁用")
                return
            
            # 尝试matplotlib显示
            try:
                import matplotlib
                matplotlib.use('TkAgg')  # 使用TkAgg后端
                import matplotlib.pyplot as plt
                
                plt.figure(figsize=(16, 12))
                plt.imshow(vis_image)
                plt.title('Enhanced Detection Results', fontsize=16, fontweight='bold')
                plt.axis('off')
                
                # 添加说明文字
                plt.figtext(0.5, 0.02, 
                        'Enhanced detection with 3D point cloud features. Numbers indicate object centers in 3D space.',
                        ha='center', fontsize=10, style='italic')
                
                plt.tight_layout()
                plt.show(block=False)  # 非阻塞显示
                plt.pause(0.1)
                print("[DISPLAY]  matplotlib弹窗显示成功")
                
            except Exception as e:
                print(f"[DISPLAY] matplotlib显示失败: {e}")
                
                # 尝试OpenCV显示
                try:
                    cv2.namedWindow('Enhanced Detection Results', cv2.WINDOW_NORMAL)
                    cv2.resizeWindow('Enhanced Detection Results', 1200, 800)
                    cv2.imshow('Enhanced Detection Results', cv2.cvtColor(vis_image, cv2.COLOR_RGB2BGR))
                    cv2.waitKey(1)  # 非阻塞
                    print("[DISPLAY]  OpenCV窗口显示成功")
                    
                except Exception as e2:
                    print(f"[DISPLAY] OpenCV显示也失败: {e2}")
                    print("[DISPLAY] 无法显示可视化窗口，仅保存文件")
            
        except Exception as e:
            print(f"[DISPLAY] 显示弹窗失败: {e}")

    def _publish_visualization_message(self, vis_image: np.ndarray):
        """发布ROS可视化消息"""
        try:
            # 这个方法应该在detection_node.py中调用
            # 这里只是预留接口
            print("[PUBLISH] 可视化消息发布接口预留")
            
        except Exception as e:
            print(f"[PUBLISH] 发布可视化消息失败: {e}")