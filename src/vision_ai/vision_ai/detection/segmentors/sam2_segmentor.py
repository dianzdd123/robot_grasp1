# detection/segmentors/sam2_segmentor.py
import numpy as np
import torch
from typing import List
from ..interfaces.segmentor_interface import ObjectSegmentor

class SAM2Segmentor(ObjectSegmentor):
    """SAM2分割器实现"""
    
    def __init__(self, checkpoint_path: str, config_name: str = "sam2_hiera_l.yaml", device: str = "cuda"):
        """
        初始化SAM2分割器
        
        Args:
            checkpoint_path: SAM2模型检查点路径
            config_name: SAM2配置文件名称 (例如: "sam2_hiera_l.yaml")
            device: 设备 ("cuda" 或 "cpu")
        """
        self.device = device if torch.cuda.is_available() else "cpu"
        self.checkpoint_path = checkpoint_path
        self.config_name = config_name
        
        try:
            from sam2.build_sam import build_sam2
            from sam2.sam2_image_predictor import SAM2ImagePredictor
            
            # 构建SAM2模型 - 使用配置名称而非路径
            self.model = build_sam2(config_name, checkpoint_path, device=self.device)
            self.predictor = SAM2ImagePredictor(self.model)
            
            print(f"[SAM2] 模型加载成功")
            print(f"[SAM2] 设备: {self.device}")
            print(f"[SAM2] 配置: {config_name}")
            print(f"[SAM2] 检查点: {checkpoint_path}")
            
        except ImportError as e:
            raise ImportError(
                "无法导入SAM2库。请确保已安装：\n"
                "pip install git+https://github.com/facebookresearch/segment-anything-2.git"
            ) from e
        except Exception as e:
            raise RuntimeError(f"SAM2模型加载失败: {e}") from e
    
    def set_image(self, image: np.ndarray):
        """
        设置当前处理的图像
        
        Args:
            image: RGB图像 (H, W, 3)
        """
        self.predictor.set_image(image)
    
    def segment(self, image: np.ndarray, boxes: np.ndarray) -> List[np.ndarray]:
        """
        对检测到的目标进行分割
        
        Args:
            image: RGB图像 (H, W, 3)
            boxes: 检测框 (N, 4) [x1, y1, x2, y2]
            
        Returns:
            masks: 分割掩码列表，每个掩码为 (H, W) 的boolean数组
        """
        if len(boxes) == 0:
            return []
        
        # 设置图像
        self.set_image(image)
        
        masks = []
        for i, box in enumerate(boxes):
            try:
                x1, y1, x2, y2 = box.astype(int)
                input_box = np.array([x1, y1, x2, y2])
                
                # 运行SAM2预测
                mask, _, _ = self.predictor.predict(
                    box=input_box, 
                    multimask_output=False
                )
                
                # 添加到结果列表
                masks.append(mask[0])  # mask[0] 是最佳掩码
                
            except Exception as e:
                print(f"[SAM2] 第 {i} 个目标分割失败: {e}")
                # 创建空掩码作为后备
                empty_mask = np.zeros((image.shape[0], image.shape[1]), dtype=bool)
                masks.append(empty_mask)
        
        print(f"[SAM2] 完成 {len(masks)} 个目标的分割")
        return masks
    
    def segment_single(self, image: np.ndarray, box: np.ndarray) -> np.ndarray:
        """
        分割单个目标 (便利方法)
        
        Args:
            image: RGB图像 (H, W, 3)
            box: 单个检测框 (4,) [x1, y1, x2, y2]
            
        Returns:
            mask: 分割掩码 (H, W) boolean数组
        """
        masks = self.segment(image, box.reshape(1, -1))
        return masks[0] if masks else np.zeros((image.shape[0], image.shape[1]), dtype=bool)