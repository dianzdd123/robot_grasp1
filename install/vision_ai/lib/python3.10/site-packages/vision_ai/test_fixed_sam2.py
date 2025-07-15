#!/usr/bin/env python3
# 测试修复后的SAM2分割器

import numpy as np
import torch
import os
import sys

# 添加项目路径
sys.path.append('/home/qi/ros2_ws/src/vision_ai/vision_ai')

def test_fixed_sam2():
    print("测试修复后的SAM2分割器...")
    
    try:
        # 导入修复后的分割器
        from vision_ai.vision_ai.detection.detectors.sam2_segmentor import SAM2Segmentor
        
        # 模型路径
        checkpoint_path = "/home/qi/ros2_ws/src/vision_ai/models/sam2/sam2_hiera_large.pt"
        
        # 测试不同的配置方法
        config_options = [
            "sam2_hiera_l",           # 配置名称
            "sam2_hiera_l.yaml",      # 配置文件名
            "hiera_l",                # 简化名称
        ]
        
        for config_name in config_options:
            try:
                print(f"\n尝试配置: {config_name}")
                segmentor = SAM2Segmentor(
                    checkpoint_path=checkpoint_path,
                    config_name=config_name,
                    device="cuda" if torch.cuda.is_available() else "cpu"
                )
                
                # 测试基本功能
                test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
                test_boxes = np.array([[100, 100, 200, 200], [300, 300, 400, 400]])
                
                masks = segmentor.segment(test_image, test_boxes)
                
                if len(masks) == 2:
                    print(f"✅ 成功！配置 '{config_name}' 工作正常")
                    return True, config_name
                    
            except Exception as e:
                print(f"❌ 配置 '{config_name}' 失败: {e}")
                continue
        
        print("❌ 所有配置方法都失败了")
        return False, None
        
    except Exception as e:
        print(f"❌ 导入或初始化失败: {e}")
        return False, None

if __name__ == "__main__":
    # 测试修复后的SAM2
    success, working_config = test_fixed_sam2()
    
    if success:
        print(f"\n🎉 SAM2修复成功！使用配置: {working_config}")
        print("可以继续进行下一步开发")
    else:
        print("\n⚠️ SAM2修复失败，尝试备选方案...")