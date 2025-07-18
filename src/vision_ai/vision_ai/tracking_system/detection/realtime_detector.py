#!/usr/bin/env python3
"""
实时检测器
负责YOLO+SAM2的实时检测和分割
"""

import cv2
import numpy as np
import time
from typing import List, Dict, Optional, Tuple, Any
from ..utils.config import get_config
from ..utils.data_structures import DetectionResult, CameraFrame

class RealtimeDetector:
    """实时检测器"""
    
    def __init__(self, logger=None):
        self.config = get_config()
        self.logger = logger
        
        # 检测组件（暂时用print代替实际实现）
        self.yolo_model = None
        self.sam2_model = None
        
        # 性能统计
        self.detection_count = 0
        self.total_detection_time = 0.0
        self.last_detection_time = 0.0
        
        # 检测缓存
        self.detection_cache = {}
        self.cache_timeout = 0.1  # 100ms缓存
        
        self._log_info("Realtime detector initialized")
    
    def initialize_models(self) -> bool:
        """初始化检测模型"""
        self._log_info("Initializing YOLO and SAM2 models...")
        
        # TODO: 实际的模型初始化
        # self.yolo_model = load_yolo_model(self.config.yolo_config['model_path'])
        # self.sam2_model = load_sam2_model(self.config.sam2_config['model_path'])
        
        self._log_info("✅ Models initialized (simulated)")
        return True
    
    def detect_objects(self, frame: CameraFrame) -> List[DetectionResult]:
        """检测对象（完整流程：YOLO + SAM2）"""
        if not frame.is_valid():
            self._log_error("Invalid camera frame")
            return []
        
        start_time = time.time()
        
        # 1. YOLO检测
        yolo_results = self._run_yolo_detection(frame.color_image)
        if not yolo_results:
            self._log_info("No YOLO detections")
            return []
        
        # 2. SAM2分割
        sam2_results = self._run_sam2_segmentation(frame.color_image, yolo_results)
        
        # 3. 特征提取
        detections = self._extract_features(frame, sam2_results)
        
        # 4. 更新统计
        detection_time = time.time() - start_time
        self.detection_count += 1
        self.total_detection_time += detection_time
        self.last_detection_time = time.time()
        
        self._log_info(f"Detected {len(detections)} objects in {detection_time:.3f}s")
        
        return detections
    
    def detect_objects_lightweight(self, frame: CameraFrame, target_class_id: int) -> List[DetectionResult]:
        """轻量级检测（仅YOLO）"""
        if not frame.is_valid():
            return []
        
        start_time = time.time()
        
        # 1. YOLO检测
        yolo_results = self._run_yolo_detection(frame.color_image)
        
        # 2. 过滤目标类别
        filtered_results = []
        for result in yolo_results:
            if result['class_id'] == target_class_id:
                filtered_results.append(result)
        
        # 3. 创建轻量级检测结果
        detections = []
        for result in filtered_results:
            detection = DetectionResult(
                object_id=f"lightweight_{result['class_id']}_{len(detections)}",
                class_id=result['class_id'],
                class_name=self.config.get_class_name(result['class_id']),
                confidence=result['confidence'],
                bounding_box=result['bbox'],
                centroid_2d=self._calculate_bbox_center(result['bbox']),
                timestamp=time.time()
            )
            detections.append(detection)
        
        detection_time = time.time() - start_time
        self._log_info(f"Lightweight detection: {len(detections)} objects in {detection_time:.3f}s")
        
        return detections
    
    def _run_yolo_detection(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """运行YOLO检测"""
        self._log_info("Running YOLO detection...")
        
        # TODO: 实际的YOLO检测
        # results = self.yolo_model.predict(image)
        # return self._parse_yolo_results(results)
        
        # 模拟YOLO检测结果
        h, w = image.shape[:2]
        mock_results = [
            {
                'class_id': 4,  # lemon
                'confidence': 0.9,
                'bbox': [w//4, h//4, w//2, h//2]
            },
            {
                'class_id': 3,  # corn
                'confidence': 0.8,
                'bbox': [w//2, h//6, 3*w//4, h//3]
            }
        ]
        
        self._log_info(f"YOLO detected {len(mock_results)} objects")
        return mock_results
    
    def _run_sam2_segmentation(self, image: np.ndarray, yolo_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """运行SAM2分割"""
        self._log_info("Running SAM2 segmentation...")
        
        # TODO: 实际的SAM2分割
        # masks = self.sam2_model.segment(image, yolo_results)
        # return self._parse_sam2_results(masks, yolo_results)
        
        # 模拟SAM2分割结果
        sam2_results = []
        for i, yolo_result in enumerate(yolo_results):
            bbox = yolo_result['bbox']
            x1, y1, x2, y2 = bbox
            
            # 创建模拟mask
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            mask[y1:y2, x1:x2] = 255
            
            sam2_result = {
                'class_id': yolo_result['class_id'],
                'confidence': yolo_result['confidence'],
                'bbox': bbox,
                'mask': mask,
                'mask_area': np.sum(mask > 0)
            }
            sam2_results.append(sam2_result)
        
        self._log_info(f"SAM2 segmented {len(sam2_results)} objects")
        return sam2_results
    
    def _extract_features(self, frame: CameraFrame, sam2_results: List[Dict[str, Any]]) -> List[DetectionResult]:
        """提取特征"""
        self._log_info("Extracting features...")
        
        detections = []
        for i, result in enumerate(sam2_results):
            # 基本信息
            object_id = f"detected_{result['class_id']}_{i}"
            class_name = self.config.get_class_name(result['class_id'])
            
            # 计算质心
            centroid_2d = self._calculate_mask_centroid(result['mask'])
            centroid_3d = self._calculate_3d_centroid(frame, centroid_2d)
            
            # 提取特征
            features = self._extract_object_features(frame.color_image, result['mask'])
            
            # 创建检测结果
            detection = DetectionResult(
                object_id=object_id,
                class_id=result['class_id'],
                class_name=class_name,
                confidence=result['confidence'],
                bounding_box=result['bbox'],
                centroid_2d=centroid_2d,
                centroid_3d=centroid_3d,
                mask=result['mask'],
                mask_area=result['mask_area'],
                features=features,
                timestamp=time.time()
            )
            
            detections.append(detection)
        
        return detections
    
    def _extract_object_features(self, image: np.ndarray, mask: np.ndarray) -> Dict[str, Any]:
        """提取对象特征"""
        features = {}
        
        # 1. 颜色特征
        features['color'] = self._extract_color_features(image, mask)
        
        # 2. 形状特征
        features['shape'] = self._extract_shape_features(mask)
        
        # 3. 空间特征
        features['spatial'] = self._extract_spatial_features(mask)
        
        return features
    
    def _extract_color_features(self, image: np.ndarray, mask: np.ndarray) -> Dict[str, Any]:
        """提取颜色特征"""
        color_features = {}
        
        # 获取掩码区域的像素
        masked_pixels = image[mask > 0]
        
        if len(masked_pixels) > 0:
            # 计算颜色直方图
            hist_b = cv2.calcHist([masked_pixels[:, 0]], [0], None, [64], [0, 256])
            hist_g = cv2.calcHist([masked_pixels[:, 1]], [0], None, [64], [0, 256])
            hist_r = cv2.calcHist([masked_pixels[:, 2]], [0], None, [64], [0, 256])
            
            # 归一化直方图
            hist_b = hist_b.flatten() / (np.sum(hist_b) + 1e-6)
            hist_g = hist_g.flatten() / (np.sum(hist_g) + 1e-6)
            hist_r = hist_r.flatten() / (np.sum(hist_r) + 1e-6)
            
            # 合并为RGB直方图
            color_features['histogram'] = np.concatenate([hist_r, hist_g, hist_b]).tolist()
            
            # 计算颜色统计
            color_features['mean_color'] = np.mean(masked_pixels, axis=0).tolist()
            color_features['std_color'] = np.std(masked_pixels, axis=0).tolist()
            
            # 主要颜色
            color_features['dominant_color'] = np.median(masked_pixels, axis=0).astype(int).tolist()
        else:
            # 空mask的默认值
            color_features['histogram'] = [0.0] * 192  # 64*3
            color_features['mean_color'] = [0.0, 0.0, 0.0]
            color_features['std_color'] = [0.0, 0.0, 0.0]
            color_features['dominant_color'] = [0, 0, 0]
        
        return color_features
    
    def _extract_shape_features(self, mask: np.ndarray) -> Dict[str, Any]:
        """提取形状特征"""
        shape_features = {}
        
        # 查找轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # 选择最大轮廓
            main_contour = max(contours, key=cv2.contourArea)
            
            # 计算Hu矩
            moments = cv2.moments(main_contour)
            if moments['m00'] != 0:
                hu_moments = cv2.HuMoments(moments).flatten()
                # 对数变换
                hu_moments = [-np.sign(h) * np.log10(abs(h) + 1e-10) for h in hu_moments]
                shape_features['hu_moments'] = hu_moments
            else:
                shape_features['hu_moments'] = [0.0] * 7
            
            # 基本形状参数
            area = cv2.contourArea(main_contour)
            perimeter = cv2.arcLength(main_contour, True)
            
            shape_features['area'] = float(area)
            shape_features['perimeter'] = float(perimeter)
            
            # 圆度
            if perimeter > 0:
                shape_features['circularity'] = 4 * np.pi * area / (perimeter * perimeter)
            else:
                shape_features['circularity'] = 0.0
            
            # 边界框
            x, y, w, h = cv2.boundingRect(main_contour)
            shape_features['aspect_ratio'] = float(w) / float(h) if h > 0 else 0.0
            
            # 最小外接矩形
            rect = cv2.minAreaRect(main_contour)
            shape_features['min_rect_angle'] = float(rect[2])
            shape_features['min_rect_area'] = float(rect[1][0] * rect[1][1])
            
        else:
            # 没有轮廓的默认值
            shape_features['hu_moments'] = [0.0] * 7
            shape_features['area'] = 0.0
            shape_features['perimeter'] = 0.0
            shape_features['circularity'] = 0.0
            shape_features['aspect_ratio'] = 0.0
            shape_features['min_rect_angle'] = 0.0
            shape_features['min_rect_area'] = 0.0
        
        return shape_features
    
    def _extract_spatial_features(self, mask: np.ndarray) -> Dict[str, Any]:
        """提取空间特征"""
        spatial_features = {}
        
        # 计算质心
        centroid = self._calculate_mask_centroid(mask)
        spatial_features['centroid_2d'] = centroid
        
        # 计算边界框
        y_indices, x_indices = np.where(mask > 0)
        if len(x_indices) > 0:
            spatial_features['bbox'] = [
                float(np.min(x_indices)),
                float(np.min(y_indices)),
                float(np.max(x_indices)),
                float(np.max(y_indices))
            ]
        else:
            spatial_features['bbox'] = [0.0, 0.0, 0.0, 0.0]
        
        return spatial_features
    
    def _calculate_bbox_center(self, bbox: List[float]) -> Tuple[float, float]:
        """计算边界框中心"""
        if len(bbox) != 4:
            return (0.0, 0.0)
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2, (y1 + y2) / 2)
    
    def _calculate_mask_centroid(self, mask: np.ndarray) -> Tuple[float, float]:
        """计算mask质心"""
        y_indices, x_indices = np.where(mask > 0)
        if len(x_indices) > 0:
            centroid_x = float(np.mean(x_indices))
            centroid_y = float(np.mean(y_indices))
            return (centroid_x, centroid_y)
        return (0.0, 0.0)
    
    def _calculate_3d_centroid(self, frame: CameraFrame, centroid_2d: Tuple[float, float]) -> Optional[Tuple[float, float, float]]:
        """计算3D质心"""
        if frame.depth_image is None:
            return None
        
        # TODO: 实际的3D质心计算
        # 需要相机内参和深度信息
        self._log_info("TODO: Implement 3D centroid calculation")
        return None
    
    def get_detection_stats(self) -> Dict[str, Any]:
        """获取检测统计"""
        avg_time = self.total_detection_time / max(1, self.detection_count)
        fps = 1.0 / avg_time if avg_time > 0 else 0.0
        
        return {
            'detection_count': self.detection_count,
            'total_detection_time': self.total_detection_time,
            'average_detection_time': avg_time,
            'detection_fps': fps,
            'last_detection_time': self.last_detection_time
        }
    
    def reset_stats(self) -> None:
        """重置统计"""
        self.detection_count = 0
        self.total_detection_time = 0.0
        self.last_detection_time = 0.0
    
    def _log_info(self, message: str) -> None:
        """记录信息日志"""
        if self.logger:
            self.logger.info(f"[RealtimeDetector] {message}")
        else:
            print(f"[INFO] [RealtimeDetector] {message}")
    
    def _log_error(self, message: str) -> None:
        """记录错误日志"""
        if self.logger:
            self.logger.error(f"[RealtimeDetector] {message}")
        else:
            print(f"[ERROR] [RealtimeDetector] {message}")

# 测试检测器
if __name__ == "__main__":
    # 创建测试图像
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    test_frame = CameraFrame(timestamp=time.time(), color_image=test_image)
    
    # 创建检测器
    detector = RealtimeDetector()
    detector.initialize_models()
    
    # 测试完整检测
    print("Testing full detection...")
    detections = detector.detect_objects(test_frame)
    print(f"Full detection results: {len(detections)} objects")
    
    # 测试轻量级检测
    print("\nTesting lightweight detection...")
    lightweight_detections = detector.detect_objects_lightweight(test_frame, target_class_id=4)
    print(f"Lightweight detection results: {len(lightweight_detections)} objects")
    
    # 打印统计
    print(f"\nDetection stats: {detector.get_detection_stats()}")
    
    print("\n✅ Realtime detector test completed")