#!/usr/bin/env python3
"""
Real-time Detector for Tracking System
实时检测器 - YOLO + SAM2 + 特征提取
"""

import cv2
import numpy as np
import torch
from ultralytics import YOLO
import time
from typing import List, Dict, Any, Tuple, Optional
import os

# SAM2 imports
try:
    from sam2.build_sam import build_sam2
    from sam2.sam2_image_predictor import SAM2ImagePredictor
    SAM2_AVAILABLE = True
except ImportError:
    print("[REALTIME_DETECTOR] SAM2 not available, using fallback")
    SAM2_AVAILABLE = False

from ..utils.config import TrackingConfig, DetectionResult


class RealtimeDetector:
    """实时检测器 - 集成YOLO和SAM2"""
    
    def __init__(self, config: TrackingConfig, logger=None):
        """
        初始化实时检测器
        
        Args:
            config: 追踪配置
            logger: 日志记录器
        """
        self.config = config
        self.logger = logger
        
        # 模型配置
        self.yolo_config = config.yolo_config
        self.sam2_config = config.sam2_config
        self.feature_config = config.feature_config
        self.camera_config = config.camera_config
        
        # 检测参数
        self.confidence_threshold = self.yolo_config.get('confidence_threshold', 0.7)
        self.iou_threshold = self.yolo_config.get('iou_threshold', 0.5)
        
        # 初始化模型
        self.yolo_model = None
        self.sam2_predictor = None
        
        # 设备配置
        self.device = self._setup_device()
        
        # 类别名称
        self.class_names = config.class_names
        
        # 初始化模型
        self._initialize_models()
        
        self._log_info("🔍 实时检测器初始化完成")
    
    def _setup_device(self):
        """设置计算设备"""
        if torch.cuda.is_available():
            device = 'cuda'
            self._log_info(f"🚀 使用GPU: {torch.cuda.get_device_name(0)}")
        else:
            device = 'cpu'
            self._log_info("💻 使用CPU")
        return device
    
    def _initialize_models(self):
        """初始化所有模型"""
        try:
            # 初始化YOLO
            self._initialize_yolo()
            
            # 初始化SAM2
            if SAM2_AVAILABLE:
                self._initialize_sam2()
            else:
                self._log_warn("⚠️ SAM2不可用，将使用YOLO边界框作为mask")
            
            self._log_info("✅ 所有模型初始化完成")
            
        except Exception as e:
            self._log_error(f"❌ 模型初始化失败: {e}")
            raise
    
    def _initialize_yolo(self):
        """初始化YOLO模型"""
        try:
            model_path = self.yolo_config.get('model_path')
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"YOLO模型文件不存在: {model_path}")
            
            self.yolo_model = YOLO(model_path)
            self.yolo_model.to(self.device)
            
            self._log_info(f"✅ YOLO模型加载成功: {os.path.basename(model_path)}")
            
        except Exception as e:
            self._log_error(f"❌ YOLO模型初始化失败: {e}")
            raise
    
    def _initialize_sam2(self):
        """初始化SAM2模型"""
        if not SAM2_AVAILABLE:
            return
        
        try:
            checkpoint_path = self.sam2_config.get('checkpoint')
            config_name = self.sam2_config.get('config', 'sam2_hiera_l.yaml')
            
            if not os.path.exists(checkpoint_path):
                raise FileNotFoundError(f"SAM2模型文件不存在: {checkpoint_path}")
            
            # 构建SAM2模型
            sam2_model = build_sam2(config_name, checkpoint_path, device=self.device)
            self.sam2_predictor = SAM2ImagePredictor(sam2_model)
            
            self._log_info(f"✅ SAM2模型加载成功: {os.path.basename(checkpoint_path)}")
            
        except Exception as e:
            self._log_error(f"❌ SAM2模型初始化失败: {e}")
            self.sam2_predictor = None
    
    def detect_and_segment(self, image: np.ndarray, depth_image: np.ndarray = None) -> List[DetectionResult]:
        """
        检测和分割对象
        
        Args:
            image: 输入图像 (H, W, 3) - BGR或RGB格式
            depth_image: 深度图像 (H, W)
        
        Returns:
            检测结果列表
        """
        try:
            # 检查图像格式并统一为RGB
            if len(image.shape) != 3 or image.shape[2] != 3:
                self._log_error(f"❌ 无效图像格式: {image.shape}")
                return []
            
            input_image = image
            
            # YOLO检测
            yolo_results = self._run_yolo_detection(input_image)
            if not yolo_results:
                self._log_debug("❌ YOLO未检测到任何对象")
                return []
            
            self._log_debug(f"🔍 YOLO检测到 {len(yolo_results)} 个对象")
            
            # SAM2分割
            detection_results = []
            for yolo_result in yolo_results:
                detection_result = self._process_single_detection(
                    input_image, depth_image, yolo_result
                )
                if detection_result:
                    detection_results.append(detection_result)
            
            self._log_debug(f"✅ 完成检测和分割，共 {len(detection_results)} 个有效结果")
            return detection_results
            
        except Exception as e:
            self._log_error(f"❌ 检测和分割失败: {e}")
            import traceback
            self._log_error(f"详细错误: {traceback.format_exc()}")
            return []
    
    def _run_yolo_detection(self, input_image: np.ndarray) -> List[Dict]:
        """运行YOLO检测"""
        try:
            self._log_debug(f"🔍 开始YOLO检测: 图像尺寸={input_image.shape}, 置信度阈值={self.confidence_threshold}")
            
            # YOLO推理
            results = self.yolo_model(
                input_image,
                conf=self.confidence_threshold,
                iou=self.iou_threshold,
                verbose=False
            )
            
            if not results or len(results) == 0:
                self._log_debug("❌ YOLO返回空结果")
                return []
            
            # 解析结果
            detections = []
            result = results[0]  # 单图像
            
            if result.boxes is None or len(result.boxes) == 0:
                self._log_debug("❌ YOLO未检测到边界框")
                return []
            
            self._log_debug(f"🔍 YOLO原始检测: {len(result.boxes)} 个边界框")
            
            for i, box in enumerate(result.boxes):
                # 获取边界框
                xyxy = box.xyxy[0].cpu().numpy()  # [x1, y1, x2, y2]
                confidence = float(box.conf[0].cpu().numpy())
                class_id = int(box.cls[0].cpu().numpy())
                
                self._log_debug(f"  检测 {i}: class_id={class_id}, confidence={confidence:.3f}, bbox={xyxy}")
                
                # 过滤低置信度检测
                if confidence < self.confidence_threshold:
                    self._log_debug(f"  ❌ 置信度过低，跳过: {confidence:.3f} < {self.confidence_threshold}")
                    continue
                
                # 获取类别名称
                class_name = self.class_names.get(class_id, f'class_{class_id}')
                
                detections.append({
                    'bbox': xyxy,
                    'confidence': confidence,
                    'class_id': class_id,
                    'class_name': class_name
                })
                
                self._log_debug(f"  ✅ 有效检测: {class_name} (class_id={class_id}, conf={confidence:.3f})")
            
            self._log_debug(f"🎯 最终有效检测: {len(detections)} 个对象")
            return detections
            
        except Exception as e:
            self._log_error(f"❌ YOLO检测失败: {e}")
            import traceback
            self._log_error(f"详细错误: {traceback.format_exc()}")
            return []
    
    def _process_single_detection(self, input_image: np.ndarray, depth_image: np.ndarray, 
                                yolo_result: Dict) -> Optional[DetectionResult]:
        """处理单个检测结果"""
        try:
            bbox = yolo_result['bbox']
            class_id = yolo_result['class_id']
            class_name = yolo_result['class_name']
            confidence = yolo_result['confidence']
            
            # 生成临时object_id（后续由ID匹配器分配真实ID）
            temp_object_id = f"temp_{class_name}_{int(time.time()*1000)%10000}"
            
            # SAM2分割
            mask = self._run_sam2_segmentation(input_image, bbox)
            
            if mask is None:
                self._log_warn(f"⚠️ SAM2分割失败，使用bbox作为mask")
                mask = self._create_bbox_mask(bbox, input_image.shape[:2])
            
            # 计算质心
            centroid_2d = self._calculate_centroid_2d(mask)
            centroid_3d = self._calculate_centroid_3d(centroid_2d, depth_image)
            
            # 提取特征
            features = self._extract_features(input_image, mask, bbox)
            
            # 创建检测结果
            detection_result = DetectionResult(
                object_id=temp_object_id,
                class_id=class_id,
                class_name=class_name,
                bounding_box=bbox.tolist(),
                mask=mask,
                centroid_2d=centroid_2d,
                centroid_3d=centroid_3d,
                confidence=confidence,
                features=features
            )
            
            return detection_result
            
        except Exception as e:
            self._log_error(f"❌ 处理检测结果失败: {e}")
            return None
    
    def _run_sam2_segmentation(self, input_image: np.ndarray, bbox: np.ndarray) -> Optional[np.ndarray]:
        """运行SAM2分割"""
        if not self.sam2_predictor:
            return None
        
        try:
            # 设置图像
            self.sam2_predictor.set_image(input_image)
            
            # 使用bbox作为prompt
            input_box = bbox.reshape(1, 4)  # [x1, y1, x2, y2]
            
            # 预测mask
            masks, scores, _ = self.sam2_predictor.predict(
                point_coords=None,
                point_labels=None,
                box=input_box,
                multimask_output=False
            )
            
            if len(masks) > 0:
                # 选择得分最高的mask
                best_mask = masks[0]  # (H, W)
                return best_mask.astype(np.uint8) * 255
            
            return None
            
        except Exception as e:
            self._log_error(f"❌ SAM2分割失败: {e}")
            return None
    
    def _create_bbox_mask(self, bbox: np.ndarray, image_shape: Tuple[int, int]) -> np.ndarray:
        """从边界框创建mask"""
        mask = np.zeros(image_shape, dtype=np.uint8)
        x1, y1, x2, y2 = bbox.astype(int)
        
        # 确保坐标在图像范围内
        x1 = max(0, min(x1, image_shape[1] - 1))
        y1 = max(0, min(y1, image_shape[0] - 1))
        x2 = max(0, min(x2, image_shape[1] - 1))
        y2 = max(0, min(y2, image_shape[0] - 1))
        
        mask[y1:y2, x1:x2] = 255
        return mask
    
    def _calculate_centroid_2d(self, mask: np.ndarray) -> Tuple[float, float]:
        """计算2D质心"""
        try:
            # 找到mask中的非零像素
            y_coords, x_coords = np.where(mask > 0)
            
            if len(x_coords) == 0:
                return (0.0, 0.0)
            
            # 计算质心
            centroid_x = float(np.mean(x_coords))
            centroid_y = float(np.mean(y_coords))
            
            return (centroid_x, centroid_y)
            
        except Exception as e:
            self._log_error(f"❌ 计算2D质心失败: {e}")
            return (0.0, 0.0)
    
    def _calculate_centroid_3d(self, centroid_2d: Tuple[float, float], 
                              depth_image: np.ndarray = None) -> Tuple[float, float, float]:
        """计算3D质心"""
        try:
            if depth_image is None:
                return (centroid_2d[0], centroid_2d[1], 0.0)
            
            x_pixel, y_pixel = int(centroid_2d[0]), int(centroid_2d[1])
            
            # 确保像素坐标在图像范围内
            h, w = depth_image.shape
            x_pixel = max(0, min(x_pixel, w - 1))
            y_pixel = max(0, min(y_pixel, h - 1))
            
            # 获取深度值
            depth_value = depth_image[y_pixel, x_pixel]
            
            if depth_value == 0:
                # 如果深度值为0，使用周围像素的平均深度
                window_size = 5
                y_start = max(0, y_pixel - window_size)
                y_end = min(h, y_pixel + window_size + 1)
                x_start = max(0, x_pixel - window_size)
                x_end = min(w, x_pixel + window_size + 1)
                
                depth_window = depth_image[y_start:y_end, x_start:x_end]
                valid_depths = depth_window[depth_window > 0]
                
                if len(valid_depths) > 0:
                    depth_value = np.mean(valid_depths)
                else:
                    depth_value = 300.0  # 默认深度值（毫米）
            
            # 深度值转换（根据相机配置）
            depth_scale = self.camera_config.get('depth_scale', 0.001)
            depth_mm = depth_value * depth_scale * 1000  # 转换为毫米
            
            # 像素坐标转相机坐标
            intrinsics = self.camera_config.get('intrinsics', {})
            fx = intrinsics.get('fx', 640.0)
            fy = intrinsics.get('fy', 640.0)
            cx = intrinsics.get('cx', 320.0)
            cy = intrinsics.get('cy', 240.0)
            
            # 计算相机坐标系下的3D坐标
            x_camera = (x_pixel - cx) * depth_mm / fx
            y_camera = (y_pixel - cy) * depth_mm / fy
            z_camera = depth_mm
            
            return (x_camera, y_camera, z_camera)
            
        except Exception as e:
            self._log_error(f"❌ 计算3D质心失败: {e}")
            return (centroid_2d[0], centroid_2d[1], 300.0)
    
    def _extract_features(self, input_image: np.ndarray, mask: np.ndarray, 
                         bbox: np.ndarray) -> Dict[str, Any]:
        """提取对象特征"""
        try:
            features = {}
            
            # 颜色特征
            features['color'] = self._extract_color_features(input_image, mask)
            
            # 形状特征
            features['shape'] = self._extract_shape_features(mask)
            
            # 空间特征
            features['spatial'] = self._extract_spatial_features(bbox, mask)
            
            return features
            
        except Exception as e:
            self._log_error(f"❌ 特征提取失败: {e}")
            return {}
    
    def _extract_color_features(self, input_image: np.ndarray, mask: np.ndarray) -> Dict[str, Any]:
        """提取颜色特征"""
        try:
            # 获取mask区域的像素
            masked_pixels = input_image[mask > 0]
            
            if len(masked_pixels) == 0:
                return {'histogram': [], 'mean_color': [0, 0, 0], 'dominant_color': [0, 0, 0]}
            
            # 计算颜色直方图
            bins = self.feature_config.get('color', {}).get('histogram_bins', 64)
            
            # 分别计算RGB三个通道的直方图
            hist_r = np.histogram(masked_pixels[:, 0], bins=bins, range=(0, 256))[0]
            hist_g = np.histogram(masked_pixels[:, 1], bins=bins, range=(0, 256))[0]
            hist_b = np.histogram(masked_pixels[:, 2], bins=bins, range=(0, 256))[0]
            
            # 归一化直方图
            total_pixels = len(masked_pixels)
            hist_r = hist_r.astype(float) / total_pixels
            hist_g = hist_g.astype(float) / total_pixels
            hist_b = hist_b.astype(float) / total_pixels
            
            # 合并三个通道的直方图
            combined_histogram = np.concatenate([hist_r, hist_g, hist_b]).tolist()
            
            # 计算平均颜色
            mean_color = np.mean(masked_pixels, axis=0).tolist()
            
            # 计算主导颜色（最频繁的颜色）
            dominant_color = np.median(masked_pixels, axis=0).astype(int).tolist()
            
            return {
                'histogram': combined_histogram,
                'mean_color': mean_color,
                'dominant_color': dominant_color
            }
            
        except Exception as e:
            self._log_error(f"❌ 颜色特征提取失败: {e}")
            return {'histogram': [], 'mean_color': [0, 0, 0], 'dominant_color': [0, 0, 0]}
    
    def _extract_shape_features(self, mask: np.ndarray) -> Dict[str, Any]:
        """提取形状特征"""
        try:
            # 找到轮廓
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return self._get_default_shape_features()
            
            # 选择最大轮廓
            largest_contour = max(contours, key=cv2.contourArea)
            
            # 计算基本形状属性
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            # 计算Hu矩
            moments = cv2.moments(largest_contour)
            if moments['m00'] != 0:
                hu_moments = cv2.HuMoments(moments).flatten()
                # 对数变换，使Hu矩更稳定
                hu_moments = [-np.sign(h) * np.log10(abs(h) + 1e-10) for h in hu_moments]
            else:
                hu_moments = [0.0] * 7
            
            # 只使用前3个Hu矩（根据配置）
            hu_count = self.feature_config.get('shape', {}).get('hu_moments_count', 3)
            hu_moments = hu_moments[:hu_count]
            
            # 计算最小外接矩形
            if len(largest_contour) >= 5:
                min_area_rect = cv2.minAreaRect(largest_contour)
                center, (width, height), angle = min_area_rect
                
                # 计算长宽比
                aspect_ratio = max(width, height) / (min(width, height) + 1e-10)
                
                # 计算圆形度
                circularity = 4 * np.pi * area / (perimeter * perimeter + 1e-10)
                
                # 计算凸包和凸性
                hull = cv2.convexHull(largest_contour)
                hull_area = cv2.contourArea(hull)
                solidity = area / (hull_area + 1e-10)
                
            else:
                center = (0, 0)
                width = height = 0
                angle = 0
                aspect_ratio = 1.0
                circularity = 0.0
                solidity = 1.0
            
            return {
                'hu_moments': hu_moments,
                'area': float(area),
                'perimeter': float(perimeter),
                'aspect_ratio': float(aspect_ratio),
                'circularity': float(circularity),
                'solidity': float(solidity),
                'min_area_rect': {
                    'center': [float(center[0]), float(center[1])],
                    'size': [float(width), float(height)],
                    'angle': float(angle)
                }
            }
            
        except Exception as e:
            self._log_error(f"❌ 形状特征提取失败: {e}")
            return self._get_default_shape_features()
    
    def _get_default_shape_features(self) -> Dict[str, Any]:
        """获取默认形状特征"""
        hu_count = self.feature_config.get('shape', {}).get('hu_moments_count', 3)
        return {
            'hu_moments': [0.0] * hu_count,
            'area': 0.0,
            'perimeter': 0.0,
            'aspect_ratio': 1.0,
            'circularity': 0.0,
            'solidity': 1.0,
            'min_area_rect': {
                'center': [0.0, 0.0],
                'size': [0.0, 0.0],
                'angle': 0.0
            }
        }
    
    def _extract_spatial_features(self, bbox: np.ndarray, mask: np.ndarray) -> Dict[str, Any]:
        """提取空间特征"""
        try:
            x1, y1, x2, y2 = bbox
            
            # 边界框特征
            bbox_width = x2 - x1
            bbox_height = y2 - y1
            bbox_area = bbox_width * bbox_height
            
            # Mask特征
            mask_area = np.sum(mask > 0)
            mask_coverage = mask_area / (bbox_area + 1e-10)
            
            # 质心
            centroid = self._calculate_centroid_2d(mask)
            
            return {
                'bbox_area': float(bbox_area),
                'mask_area': float(mask_area),
                'mask_coverage': float(mask_coverage),
                'centroid_2d': centroid,
                'bbox_width': float(bbox_width),
                'bbox_height': float(bbox_height)
            }
            
        except Exception as e:
            self._log_error(f"❌ 空间特征提取失败: {e}")
            return {
                'bbox_area': 0.0,
                'mask_area': 0.0,
                'mask_coverage': 0.0,
                'centroid_2d': (0.0, 0.0),
                'bbox_width': 0.0,
                'bbox_height': 0.0
            }
    
    def run_lightweight_detection(self, input_image: np.ndarray, target_class_id: int) -> List[DetectionResult]:
        """
        运行轻量级检测（仅YOLO，不使用SAM2）
        
        Args:
            input_image: RGB图像
            target_class_id: 目标类别ID
        
        Returns:
            检测结果列表
        """
        try:
            # YOLO检测
            yolo_results = self._run_yolo_detection(input_image)
            
            # 过滤出目标类别
            target_detections = [
                result for result in yolo_results 
                if result['class_id'] == target_class_id
            ]
            
            if not target_detections:
                return []
            
            # 转换为DetectionResult（使用bbox作为mask）
            detection_results = []
            for yolo_result in target_detections:
                bbox = yolo_result['bbox']
                mask = self._create_bbox_mask(bbox, input_image.shape[:2])
                
                # 生成临时object_id
                temp_object_id = f"lightweight_{yolo_result['class_name']}_{int(time.time()*1000)%10000}"
                
                detection_result = DetectionResult(
                    object_id=temp_object_id,
                    class_id=yolo_result['class_id'],
                    class_name=yolo_result['class_name'],
                    bounding_box=bbox.tolist(),
                    mask=mask,
                    centroid_2d=self._calculate_centroid_2d(mask),
                    centroid_3d=(0.0, 0.0, 0.0),  # 轻量级模式不计算3D
                    confidence=yolo_result['confidence'],
                    features={}  # 轻量级模式不提取详细特征
                )
                
                detection_results.append(detection_result)
            
            self._log_debug(f"🚀 轻量级检测完成，找到 {len(detection_results)} 个目标类别对象")
            return detection_results
            
        except Exception as e:
            self._log_error(f"❌ 轻量级检测失败: {e}")
            return []
    
    def get_class_detection_count(self, input_image: np.ndarray, class_id: int) -> int:
        """
        获取指定类别的检测数量
        
        Args:
            input_image: RGB图像
            class_id: 类别ID
        
        Returns:
            检测数量
        """
        try:
            yolo_results = self._run_yolo_detection(input_image)
            count = sum(1 for result in yolo_results if result['class_id'] == class_id)
            return count
            
        except Exception as e:
            self._log_error(f"❌ 获取类别检测数量失败: {e}")
            return 0
    
    def visualize_detections(self, input_image: np.ndarray, 
                           detection_results: List[DetectionResult]) -> np.ndarray:
        """
        可视化检测结果
        
        Args:
            input_image: 原始RGB图像
            detection_results: 检测结果列表
        
        Returns:
            可视化图像
        """
        try:
            vis_image = input_image.copy()
            
            for detection in detection_results:
                # 绘制边界框
                bbox = detection.bounding_box
                x1, y1, x2, y2 = map(int, bbox)
                
                # 根据置信度选择颜色
                if detection.confidence > 0.8:
                    color = (0, 255, 0)  # 绿色 - 高置信度
                elif detection.confidence > 0.6:
                    color = (255, 255, 0)  # 黄色 - 中等置信度
                else:
                    color = (255, 0, 0)  # 红色 - 低置信度
                
                # 绘制边界框
                cv2.rectangle(vis_image, (x1, y1), (x2, y2), color, 2)
                
                # 绘制标签
                label = f"{detection.class_name}: {detection.confidence:.2f}"
                if hasattr(detection, 'match_confidence') and detection.match_confidence > 0:
                    label += f" (ID: {detection.match_confidence:.2f})"
                
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                cv2.rectangle(vis_image, (x1, y1 - label_size[1] - 10), 
                             (x1 + label_size[0], y1), color, -1)
                cv2.putText(vis_image, label, (x1, y1 - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # 绘制质心
                cx, cy = map(int, detection.centroid_2d)
                cv2.circle(vis_image, (cx, cy), 5, color, -1)
                
                # 绘制mask轮廓（如果有）
                if detection.mask is not None:
                    contours, _ = cv2.findContours(detection.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cv2.drawContours(vis_image, contours, -1, color, 2)
            
            return vis_image
            
        except Exception as e:
            self._log_error(f"❌ 可视化失败: {e}")
            return input_image
    
    def get_model_info(self) -> Dict[str, Any]:
        """获取模型信息"""
        return {
            'yolo_model_path': self.yolo_config.get('model_path', ''),
            'sam2_available': SAM2_AVAILABLE and self.sam2_predictor is not None,
            'sam2_checkpoint': self.sam2_config.get('checkpoint', ''),
            'device': self.device,
            'confidence_threshold': self.confidence_threshold,
            'iou_threshold': self.iou_threshold,
            'class_count': len(self.class_names)
        }
    
    # ============ 日志方法 ============
    
    def _log_info(self, message: str):
        """记录信息日志"""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[REALTIME_DETECTOR] {message}")
    
    def _log_debug(self, message: str):
        """记录调试日志"""
        if self.logger:
            self.logger.debug(message)
        else:
            print(f"[REALTIME_DETECTOR] DEBUG: {message}")
    
    def _log_warn(self, message: str):
        """记录警告日志"""
        if self.logger:
            self.logger.warn(message)
        else:
            print(f"[REALTIME_DETECTOR] WARNING: {message}")
    
    def _log_error(self, message: str):
        """记录错误日志"""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"[REALTIME_DETECTOR] ERROR: {message}")


if __name__ == "__main__":
    # 测试实时检测器
    from ..utils.config import create_tracking_config
    
    config = create_tracking_config()
    detector = RealtimeDetector(config)
    
    print("🧪 测试实时检测器...")
    print("模型信息:", detector.get_model_info())
    
    # 创建测试图像
    test_image = np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)
    
    # 测试检测
    results = detector.detect_and_segment(test_image)
    print(f"检测结果数量: {len(results)}")
    
    # 测试轻量级检测
    lightweight_results = detector.run_lightweight_detection(test_image, 4)
    print(f"轻量级检测结果数量: {len(lightweight_results)}")