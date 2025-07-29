#!/usr/bin/env python3
# enhanced_trigger_detection.py - 触发增强检测的脚本

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time
import os
import json
from pathlib import Path

class EnhancedDetectionTrigger(Node):
    def __init__(self):
        super().__init__('enhanced_detection_trigger')
        
        # 创建发布者
        self.trigger_pub = self.create_publisher(String, '/stitching_complete', 10)
        
        # 创建订阅者监听检测完成信号
        self.completion_sub = self.create_subscription(
            String, '/detection_complete', self.detection_complete_callback, 10
        )
        
        # 创建订阅者监听检测结果
        self.result_sub = self.create_subscription(
            String, '/detection_result', self.detection_result_callback, 10
        )
        
        self.detection_triggered = False
        self.detection_completed = False
        
    def detection_complete_callback(self, msg):
        """检测完成回调"""
        try:
            data = json.loads(msg.data)
            
            print(f"\n🎉 检测完成!")
            print(f"📊 检测状态: {data.get('status', 'unknown')}")
            print(f"🎯 检测到目标数: {data.get('detection_count', 0)}")
            print(f"📁 扫描目录: {data.get('scan_directory', 'unknown')}")
            
            # 检查是否使用了增强检测
            if data.get('enhanced_detection', False):
                print("✨ 使用了增强检测功能!")
                
                if 'feature_quality_stats' in data:
                    stats = data['feature_quality_stats']
                    print(f"📈 特征质量统计:")
                    print(f"  - 平均质量: {stats.get('mean_quality', 0):.1f}%")
                    print(f"  - 质量范围: {stats.get('min_quality', 0):.1f}% - {stats.get('max_quality', 0):.1f}%")
                
                if 'adaptive_learning_stats' in data:
                    adaptive = data['adaptive_learning_stats']
                    if adaptive.get('enabled', False):
                        print(f"🧠 自适应学习:")
                        print(f"  - 总匹配次数: {adaptive.get('total_matches', 0)}")
                        print(f"  - 成功率: {adaptive.get('success_rate', 0):.1%}")
            else:
                print("⚠️ 使用了传统检测")
            
            # 显示文件信息
            if 'reference_features_path' in data:
                print(f"📂 参考特征库路径: {data['reference_features_path']}")
            
            self.detection_completed = True
            
        except Exception as e:
            print(f"❌ 处理检测完成信号失败: {e}")
    
    def detection_result_callback(self, msg):
        """检测结果回调"""
        try:
            data = json.loads(msg.data)
            
            print(f"\n📋 检测结果详情:")
            print(f"🔍 处理时间: {data.get('processing_time', 0):.2f}秒")
            print(f"📊 检测到 {data.get('detection_count', 0)} 个对象:")
            
            for i, obj in enumerate(data.get('objects', []), 1):
                obj_id = obj.get('object_id', 'unknown')
                class_name = obj.get('class_name', 'unknown')
                confidence = obj.get('confidence', 0)
                quality = obj.get('quality_score', 0)
                
                print(f"  {i}. {obj_id} ({class_name})")
                print(f"     - 检测置信度: {confidence:.3f}")
                
                if quality > 0:
                    print(f"     - 特征质量: {quality:.1f}%")
                
                # 显示3D坐标信息
                if 'features' in obj and 'spatial' in obj['features']:
                    spatial = obj['features']['spatial']
                    if 'world_coordinates' in spatial:
                        coords = spatial['world_coordinates']
                        print(f"     - 世界坐标: ({coords[0]:.1f}, {coords[1]:.1f}, {coords[2]:.1f})mm")
                
                # 显示抓夹信息
                if 'features' in obj and 'grasp_info' in obj['features']:
                    grasp = obj['features']['grasp_info']
                    width = grasp.get('recommended_width', 0)
                    print(f"     - 推荐抓夹宽度: {width}mm")
            
            # 检查是否使用了增强特征
            if data.get('enhanced_features', False):
                print("✨ 使用了增强3D点云特征")
            
        except Exception as e:
            print(f"❌ 处理检测结果失败: {e}")
    
    def trigger_detection(self, scan_dir):
        """触发检测"""
        print(f"🚀 准备触发增强检测...")
        print(f"📁 扫描目录: {scan_dir}")
        
        # 检查扫描目录
        if not os.path.exists(scan_dir):
            print(f"❌ 扫描目录不存在: {scan_dir}")
            return False
        
        # 检查是否有必要的文件
        required_files = []
        for file in os.listdir(scan_dir):
            if file.startswith('final_') and file.endswith('.jpg'):
                required_files.append(f"融合图像: {file}")
            elif file.startswith('color_waypoint_') and file.endswith('.jpg'):
                required_files.append(f"waypoint图像: {file}")
        
        if required_files:
            print("✅ 找到扫描文件:")
            for file in required_files[:3]:  # 只显示前3个
                print(f"  - {file}")
            if len(required_files) > 3:
                print(f"  - ... 还有 {len(required_files)-3} 个文件")
        else:
            print("⚠️ 未找到预期的图像文件，但继续尝试...")
        
        # 等待发布者就绪
        print("⏳ 等待ROS发布者就绪...")
        time.sleep(1.0)
        
        # 发送触发消息
        msg = String()
        msg.data = scan_dir
        
        print("📤 发送增强检测触发消息...")
        self.trigger_pub.publish(msg)
        
        self.detection_triggered = True
        print("✅ 触发消息已发送")
        
        return True
    
    def wait_for_completion(self, timeout=30):
        """等待检测完成"""
        print(f"⏳ 等待检测完成 (超时: {timeout}秒)...")
        
        start_time = time.time()
        rate = self.create_rate(10)  # 10Hz
        
        while rclpy.ok() and not self.detection_completed:
            current_time = time.time()
            elapsed = current_time - start_time
            
            if elapsed > timeout:
                print(f"⏰ 等待超时 ({timeout}秒)")
                return False
            
            # 显示进度
            remaining = timeout - elapsed
            if int(elapsed) % 5 == 0:  # 每5秒显示一次
                print(f"⏳ 等待中... (剩余 {remaining:.0f}秒)")
            
            rclpy.spin_once(self, timeout_sec=0.1)
            rate.sleep()
        
        return self.detection_completed

def main():
    print("🔧 增强检测触发工具")
    print("=" * 50)
    
    # 获取扫描目录
    default_scan_dir = '/home/qi/ros2_ws/scan_output_20250727_181333'
    
    print(f"📁 默认扫描目录: {default_scan_dir}")
    scan_dir = input(f"请输入扫描目录路径 (回车使用默认): ").strip()
    
    if not scan_dir:
        scan_dir = default_scan_dir
    
    # 初始化ROS
    rclpy.init()
    
    try:
        # 创建触发节点
        trigger_node = EnhancedDetectionTrigger()
        
        # 触发检测
        if trigger_node.trigger_detection(scan_dir):
            # 等待检测完成
            success = trigger_node.wait_for_completion(timeout=60)
            
            if success:
                print("\n🎉 增强检测测试完成!")
                print("📋 请检查生成的文件:")
                print("  - enhanced_detection_results.json")
                print("  - reference_library.json")
                print("  - detection_visualization.jpg")
            else:
                print("\n⏰ 检测超时或失败")
                print("💡 请检查detection_node是否正在运行")
                print("💡 可以手动运行: ros2 run vision_ai detection_node")
        else:
            print("❌ 触发检测失败")
    
    except KeyboardInterrupt:
        print("\n🛑 用户中断")
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()