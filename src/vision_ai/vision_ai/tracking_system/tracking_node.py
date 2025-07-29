#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
import json
import os
from datetime import datetime

# 导入Track模块
from .enhanced_tracker import EnhancedTracker

class TrackingNode(Node):
    def __init__(self):
        super().__init__('tracking_node')
        
        # 初始化增强追踪器
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'tracking_config.json')
        self.tracker = EnhancedTracker(config_path)
        
        # ROS接口
        self.detection_complete_sub = self.create_subscription(
            String, '/detection_complete', self.detection_complete_callback, 10
        )
        
        self.tracking_result_pub = self.create_publisher(
            String, '/tracking_result', 10
        )
        
        self.get_logger().info('🎯 Track节点启动完成')
    
    def detection_complete_callback(self, msg):
        """接收Detect完成信号并开始追踪"""
        try:
            data = json.loads(msg.data)
            
            # 检查是否是增强检测结果
            if data.get('enhanced_detection', False):
                reference_library_file = data.get('reference_library_file')
                
                if reference_library_file and os.path.exists(reference_library_file):
                    # 加载参考特征库
                    success = self.tracker.load_reference_features(reference_library_file)
                    
                    if success:
                        self.get_logger().info('✅ 参考特征库加载成功，准备开始追踪')
                        # 这里可以开始目标选择或自动追踪流程
                    else:
                        self.get_logger().error('❌ 参考特征库加载失败')
                else:
                    self.get_logger().warn('⚠️ 参考特征库文件不存在')
            else:
                self.get_logger().info('📍 接收到普通检测结果，跳过增强追踪')
                
        except Exception as e:
            self.get_logger().error(f'处理检测完成信号失败: {e}')

def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = TrackingNode()
        node.get_logger().info('🎯 Track节点运行中...')
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('🛑 Track节点被用户中断')
    except Exception as e:
        print(f'❌ Track节点运行错误: {e}')
    finally:
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()