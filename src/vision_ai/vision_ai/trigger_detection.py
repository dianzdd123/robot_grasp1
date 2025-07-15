#!/usr/bin/env python3
# trigger_detection.py - 触发检测的简单脚本

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

def trigger_detection():
    """触发检测"""
    rclpy.init()
    
    node = Node('detection_trigger')
    
    # 创建发布者
    trigger_pub = node.create_publisher(String, '/stitching_complete', 10)
    
    # 等待发布者就绪
    time.sleep(1.0)
    
    # 发送触发消息
    scan_dir = '/home/qi/ros2_ws/scan_output_20250714_222550'
    
    msg = String()
    msg.data = scan_dir
    
    print(f'🚀 触发检测，扫描目录: {scan_dir}')
    trigger_pub.publish(msg)
    
    print('✅ 触发消息已发送')
    
    # 保持运行一段时间
    time.sleep(2.0)
    
    rclpy.shutdown()

if __name__ == '__main__':
    trigger_detection()