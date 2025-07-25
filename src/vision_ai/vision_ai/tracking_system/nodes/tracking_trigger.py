#!/usr/bin/env python3
"""
追踪测试触发器
用于独立测试追踪系统
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import sys
import time

class TrackingTrigger(Node):
    """追踪测试触发器"""
    
    def __init__(self):
        super().__init__('tracking_trigger')
        
        # 创建发布者
        self.detection_complete_pub = self.create_publisher(
            String,
            '/detection_complete',
            10
        )
        
        self.get_logger().info('🔧 Tracking Trigger Node initialized')
    
    def trigger_tracking(self, scan_directory: str):
        """触发追踪"""
        self.get_logger().info(f'🚀 Triggering tracking for: {scan_directory}')
        
        # 等待一秒确保节点启动完成
        time.sleep(1.0)
        
        # 发送检测完成信号
        detection_complete_msg = String()
        detection_complete_data = {
            'scan_directory': scan_directory,
            'timestamp': time.time(),
            'trigger_source': 'manual_trigger'
        }
        detection_complete_msg.data = json.dumps(detection_complete_data)
        
        self.detection_complete_pub.publish(detection_complete_msg)
        
        self.get_logger().info('✅ Detection complete signal sent')
        self.get_logger().info('📡 Tracking should start automatically...')

def main(args=None):
    rclpy.init(args=args)
    
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("Usage: ros2 run vision_ai tracking_trigger <scan_directory>")
        print("Example: ros2 run vision_ai tracking_trigger /home/qi/ros2_ws/scan_output_20250718_153215")
        return
    
    scan_directory = sys.argv[1]
    
    try:
        trigger_node = TrackingTrigger()
        
        # 触发追踪
        trigger_node.trigger_tracking(scan_directory)
        
        # 短暂运行后退出
        rclpy.spin_once(trigger_node, timeout_sec=2.0)
        
        trigger_node.get_logger().info('🎯 Trigger complete - you can now monitor the tracking node')
        
    except KeyboardInterrupt:
        trigger_node.get_logger().info('Trigger interrupted')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if 'trigger_node' in locals():
            trigger_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()