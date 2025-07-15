# detection/detectors/yolo_detector.py
import cv2
import numpy as np
from ultralytics import YOLO
from typing import Tuple
from ..interfaces.detector_interface import ObjectDetector

class YOLODetector(ObjectDetector):
    """YOLO检测器实现"""
    
    def __init__(self, model_path: str, confidence_threshold: float = 0.5):
        """
        初始化YOLO检测器
        
        Args:
            model_path: YOLO模型文件路径
            confidence_threshold: 置信度阈值
        """
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        
        # 类别名称映射 (根据您的模型调整)
        self.class_names = {
            1: 'banana',
            2: 'carrot', 
            3: 'corn',
            4: 'lemon',
            5: 'greenlemon',
            6: 'strawberry',
            7: 'tomato',
            8: 'potato',
            9: 'redpepper'
        }
        
        print(f"[YOLO] 模型加载成功: {model_path}")
        print(f"[YOLO] 置信度阈值: {confidence_threshold}")
    
    def detect(self, image: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        检测图像中的目标
        
        Args:
            image: RGB图像 (H, W, 3)
            
        Returns:
            boxes: 检测框 (N, 4) [x1, y1, x2, y2]
            class_ids: 类别ID (N,)
            confidences: 置信度 (N,)
        """
        # 转换为BGR格式（YOLO期望的格式）
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 运行检测
        results = self.model(image_bgr)[0]
        
        # 提取结果
        boxes = results.boxes.xyxy.cpu().numpy()
        class_ids = results.boxes.cls.cpu().numpy().astype(int)
        confidences = results.boxes.conf.cpu().numpy()
        
        # 应用置信度阈值过滤
        valid_indices = confidences >= self.confidence_threshold
        boxes = boxes[valid_indices]
        class_ids = class_ids[valid_indices]
        confidences = confidences[valid_indices]
        
        print(f"[YOLO] 检测到 {len(boxes)} 个目标 (置信度 >= {self.confidence_threshold})")
        
        return boxes, class_ids, confidences
    
    def get_class_names(self) -> dict:
        """获取类别名称映射"""
        return self.class_names
    
    def set_confidence_threshold(self, threshold: float):
        """设置置信度阈值"""
        self.confidence_threshold = threshold
        print(f"[YOLO] 置信度阈值已更新为: {threshold}")