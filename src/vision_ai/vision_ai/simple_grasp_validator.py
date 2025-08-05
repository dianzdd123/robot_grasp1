#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
import json
import time

class SimpleGraspValidator(Node):
    def __init__(self):
        super().__init__('simple_grasp_validator')
        
        # 订阅抓取触发信号
        self.grasp_trigger_sub = self.create_subscription(
            String, '/grasp_trigger', self.grasp_trigger_callback, 10
        )
        
# 发布夹爪控制
        self.gripper_pub = self.create_publisher(Int32, '/xarm/gripper_target', 10)
        
        self.get_logger().info('🤖 简单抓取验证系统启动')
    
    def grasp_trigger_callback(self, msg):
        """处理抓取触发信号"""
        try:
            grasp_data = json.loads(msg.data)
            
            self.get_logger().info('🎯 收到抓取触发信号!')
            self.get_logger().info(f'📁 抓取文件: {grasp_data["filename"]}')
            self.get_logger().info(f'📍 目标位置: {grasp_data["coordinate"]}')
            self.get_logger().info(f'🎯 目标ID: {grasp_data["target_id"]}')
            
            # 执行简单的夹爪动作验证
            self.execute_simple_grasp_validation()
            
        except Exception as e:
            self.get_logger().error(f'处理抓取信号失败: {e}')
    
    def execute_simple_grasp_validation(self):
        """执行简单的抓取验证动作"""
        self.get_logger().info('🔧 开始抓取验证序列')
        
        # 1. 张开夹爪
        self.get_logger().info('📐 步骤1: 张开夹爪 (800)')
        self.publish_gripper_command(800)
        time.sleep(2)
        
        # 2. 关闭夹爪
        self.get_logger().info('🤏 步骤2: 关闭夹爪 (200)')
        self.publish_gripper_command(200)
        time.sleep(2)
        
        # 3. 稍微松开
        self.get_logger().info('📐 步骤3: 稍微松开 (400)')
        self.publish_gripper_command(400)
        time.sleep(2)
        
        # 4. 再次关闭
        self.get_logger().info('🤏 步骤4: 再次关闭 (250)')
        self.publish_gripper_command(250)
        time.sleep(1)
        
        # 5. 最终张开
        self.get_logger().info('📐 步骤5: 最终张开 (600)')
        self.publish_gripper_command(600)
        
        self.get_logger().info('✅ 抓取验证序列完成 - Track系统信号传递正常!')
    
    def publish_gripper_command(self, position: int):
        """发布夹爪位置命令"""
        msg = Int32()
        msg.data = position
        self.gripper_pub.publish(msg)
        self.get_logger().info(f'📤 发布夹爪命令: {position}')

def main(args=None):
    rclpy.init(args=args)
    node = SimpleGraspValidator()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('\n🛑 抓取验证系统被用户中断')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()