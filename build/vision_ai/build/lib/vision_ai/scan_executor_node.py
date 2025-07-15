#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from vision_ai_interfaces.srv import ExecuteScan, ProcessStitching
from vision_ai_interfaces.msg import ImageData
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image
from std_srvs.srv import Trigger, SetBool 
import cv2
import numpy as np
from cv_bridge import CvBridge
import time
import os
from datetime import datetime
import math
from std_msgs.msg import String
class ScanExecutorNode(Node):
    def __init__(self):
        super().__init__('scan_executor_node')
        
        # 状态管理
        self.current_scan_plan = None
        self.execution_active = False
        self.captured_images = []
        self.current_waypoint_index = 0
        
        # CV Bridge
        self.bridge = CvBridge()
        self.current_arm_position = None
        self.target_position = None
        self.movement_completed = False
        self.output_dir = None
        
        # 相机内参 (来自scan_planner_node)
        self.camera_intrinsics = {
            'fx': 912.694580078125,
            'fy': 910.309814453125,
            'cx': 640,  # 1280/2
            'cy': 360   # 720/2
        }
        
        # 创建服务
        self.execute_service = self.create_service(
            ExecuteScan, 
            'execute_scan', 
            self.execute_scan_callback
        )
        
        # 订阅者 - 机械臂位姿
        self.current_pose_sub = self.create_subscription(
            PoseStamped, 
            '/xarm/current_pose', 
            self.pose_callback, 
            10
        )
        
        # 订阅者 - 彩色图像
        self.color_image_sub = self.create_subscription(
            Image,
            '/camera/color/image_raw',
            self.color_image_callback,
            10
        )
        
        # 订阅者 - 深度图像
        self.depth_image_sub = self.create_subscription(
            Image,
            '/camera/depth/image_raw',
            self.depth_image_callback,
            10
        )
        
        # 发布者 - 发送目标位姿给机械臂
        self.target_pose_pub = self.create_publisher(
            PoseStamped,
            '/xarm/target_pose',
            10
        )
        
        # 服务客户端 - 机械臂控制
        self.arm_enable_client = self.create_client(
            SetBool, 
            '/xarm/enable'
        )
        
        # 存储最新图像
        self.latest_color_image = None
        self.latest_depth_image = None
        
        self.get_logger().info('扫描执行节点已启动 (支持深度图采集)')
        
        # 等待硬件服务
        self._wait_for_hardware_services()

    def _wait_for_hardware_services(self):
        """等待硬件服务可用"""
        self.get_logger().info('等待硬件服务...')
        
        # 等待机械臂服务
        if not self.arm_enable_client.wait_for_service(timeout_sec=15.0):
            self.get_logger().warn('机械臂使能服务连接超时，但继续运行')
        else:
            self.get_logger().info('机械臂使能服务已连接')
        
        self.get_logger().info('所有硬件服务已就绪')

    def execute_scan_callback(self, request, response):
        """执行扫描服务回调"""
        try:
            if self.execution_active:
                response.success = False
                response.message = "扫描执行中，请等待完成"
                return response
            
            # 存储扫描计划
            self.current_scan_plan = request.scan_plan
            
            # 创建输出目录
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            self.output_dir = f"scan_output_{timestamp}"
            os.makedirs(self.output_dir, exist_ok=True)
            
            self.get_logger().info(f'开始执行扫描: {len(self.current_scan_plan.waypoints)} 个路径点')
            self.get_logger().info(f'输出目录: {self.output_dir}')
            
            # 启动异步执行
            self.execution_active = True
            self.captured_images = []
            self.current_waypoint_index = 0
            
            # 创建定时器执行扫描序列
            self.scan_timer = self.create_timer(0.5, self.scan_sequence_step)
            
            response.success = True
            response.message = f"扫描开始执行，预计 {len(self.current_scan_plan.waypoints)} 个路径点"
            
        except Exception as e:
            response.success = False
            response.message = f"扫描执行失败: {str(e)}"
            self.get_logger().error(f'扫描执行错误: {e}')
        
        return response

    def color_image_callback(self, msg):
        """彩色图像回调"""
        self.latest_color_image = msg

    def depth_image_callback(self, msg):
        """深度图像回调"""
        self.latest_depth_image = msg

    def scan_sequence_step(self):
        """扫描序列的单步执行"""
        if not self.execution_active or not self.current_scan_plan:
            return
        
        # 检查是否完成所有路径点
        if self.current_waypoint_index >= len(self.current_scan_plan.waypoints):
            self._finish_scan_execution()
            return
        
        # 只有在不忙碌时才执行下一个waypoint
        if not getattr(self, 'waypoint_busy', False):
            waypoint = self.current_scan_plan.waypoints[self.current_waypoint_index]
            self.waypoint_busy = True
            self._execute_waypoint(waypoint)

    def _execute_waypoint(self, waypoint):
        """执行单个路径点 - 等待移动完成"""
        try:
            self.get_logger().info(f'🎯 执行路径点 {self.current_waypoint_index + 1}/{len(self.current_scan_plan.waypoints)}')
            
            # 存储目标位置用于检测到达
            self.target_position = [
                waypoint.pose.position.x,
                waypoint.pose.position.y, 
                waypoint.pose.position.z
            ]
            
            target_pose = PoseStamped()
            target_pose.header.stamp = self.get_clock().now().to_msg()
            target_pose.header.frame_id = "base_link"
            target_pose.pose = waypoint.pose
            
            self.target_pose_pub.publish(target_pose)
            
            # 开始移动完成检测
            self.waypoint_data = waypoint
            self.movement_start_time = time.time()
            self.movement_completed = False
            
            # 创建检测定时器，0.5秒检查一次
            self.movement_check_timer = self.create_timer(0.5, self.check_movement_completion)
            
        except Exception as e:
            self.get_logger().error(f'waypoint执行失败: {e}')
            self.waypoint_busy = False

    def check_movement_completion(self):
        """检查移动是否完成"""
        if not hasattr(self, 'target_position') or self.target_position is None:
            return
            
        # 超时检查（30秒）
        if time.time() - self.movement_start_time > 50:
            self.get_logger().warn('移动超时，强制继续')
            self._on_movement_completed()
            return
        
        # 检查是否到达目标位置
        if self.current_arm_position is not None:
            distance = math.sqrt(
                (self.current_arm_position[0] - self.target_position[0])**2 +
                (self.current_arm_position[1] - self.target_position[1])**2 +
                (self.current_arm_position[2] - self.target_position[2])**2
            )
            
            # 到达阈值：5mm
            if distance < 5.0:
                self.get_logger().info(f'✅ 到达目标位置，距离: {distance:.1f}mm')
                self._on_movement_completed()
            else:
                elapsed = time.time() - self.movement_start_time
                self.get_logger().info(f'🚀 移动中... 距离目标: {distance:.1f}mm, 用时: {elapsed:.1f}s')

    def _on_movement_completed(self):
        """移动完成处理"""
        # 停止检测定时器
        if hasattr(self, 'movement_check_timer'):
            self.movement_check_timer.destroy()
        
        self.movement_completed = True
        
        self.get_logger().info('移动完成，开始图像采集')
        self._capture_image_at_waypoint(self.waypoint_data)
        
        # 完成当前waypoint
        self.current_waypoint_index += 1
        self.waypoint_busy = False
        self.target_position = None

    def pose_callback(self, msg):
        """机械臂位姿回调 - 用于移动检测"""
        try:
            # 保存当前位置用于移动完成检测
            self.current_arm_position = [
                msg.pose.position.x,
                msg.pose.position.y, 
                msg.pose.position.z
            ]
        except Exception as e:
            self.get_logger().error(f'位姿回调错误: {e}')

    def _capture_image_at_waypoint(self, waypoint):
        """图像采集 - 包含深度图"""
        try:
            self.get_logger().info(f'📸 开始图像采集 (彩色+深度)')
            
            # 检查图像可用性
            if not self.latest_color_image or not self.latest_depth_image:
                self.get_logger().error('彩色或深度图像不可用')
                return
            
            self.current_waypoint_for_image = waypoint
            self.process_captured_images(self.latest_color_image, self.latest_depth_image)
                
        except Exception as e:
            self.get_logger().error(f'图像采集失败: {e}')

# scan_executor_node.py 中图像处理部分的修复

    def process_captured_images(self, color_msg, depth_msg):
            """处理采集的彩色和深度图像 - 修复cv_bridge错误"""
            try:
                # 修复：安全的图像转换
                try:
                    # 对于bgr8编码，直接转换后再变换颜色
                    color_cv_image = self.bridge.imgmsg_to_cv2(color_msg, desired_encoding="passthrough")
                    
                    # 检查图像通道和转换
                    if len(color_cv_image.shape) == 3 and color_cv_image.shape[2] == 3:
                        # BGR -> RGB
                        color_rgb = cv2.cvtColor(color_cv_image, cv2.COLOR_BGR2RGB)
                    else:
                        self.get_logger().error(f'不支持的图像格式: {color_cv_image.shape}')
                        return
                        
                    self.get_logger().info(f'彩色图像转换成功: {color_rgb.shape}')
                        
                except Exception as color_error:
                    self.get_logger().error(f'彩色图像转换失败: {color_error}')
                    # 备用方案：尝试不同的转换方式
                    try:
                        color_cv_image = self.bridge.imgmsg_to_cv2(color_msg)
                        color_rgb = cv2.cvtColor(color_cv_image, cv2.COLOR_BGR2RGB)
                        self.get_logger().info('使用备用方案转换彩色图像成功')
                    except:
                        self.get_logger().error('所有彩色图像转换方案都失败')
                        return
                
                try:
                    # 转换深度图像
                    depth_raw = self.bridge.imgmsg_to_cv2(depth_msg, desired_encoding="passthrough")
                    
                    # 确保深度图像是正确的格式
                    if depth_raw.dtype != np.uint16:
                        depth_raw = depth_raw.astype(np.uint16)
                        
                    self.get_logger().info(f'深度图像转换成功: {depth_raw.shape}')
                    
                except Exception as depth_error:
                    self.get_logger().error(f'深度图像转换失败: {depth_error}')
                    return
                
                # 确保数据有效
                if color_rgb is None or color_rgb.size == 0:
                    self.get_logger().error('彩色图像数据无效')
                    return
                    
                if depth_raw is None or depth_raw.size == 0:
                    self.get_logger().error('深度图像数据无效')
                    return
                
                # 创建深度热度图用于保存
                depth_normalized = cv2.normalize(depth_raw, None, 0, 255, cv2.NORM_MINMAX)
                depth_heatmap = cv2.applyColorMap(depth_normalized.astype(np.uint8), cv2.COLORMAP_JET)
                
                # 保存图像文件
                color_filename = os.path.join(self.output_dir, f"color_waypoint_{self.current_waypoint_index+1:03d}.jpg")
                depth_heatmap_filename = os.path.join(self.output_dir, f"depth_heatmap_waypoint_{self.current_waypoint_index+1:03d}.jpg")
                depth_raw_filename = os.path.join(self.output_dir, f"depth_raw_waypoint_{self.current_waypoint_index+1:03d}.npy")
                
                # 保存时使用BGR格式（OpenCV标准）
                cv2.imwrite(color_filename, cv2.cvtColor(color_rgb, cv2.COLOR_RGB2BGR))
                cv2.imwrite(depth_heatmap_filename, depth_heatmap)
                np.save(depth_raw_filename, depth_raw)
                
                # 构建waypoint位姿信息
                waypoint_pose_6d = {
                    'x': self.current_waypoint_for_image.pose.position.x,
                    'y': self.current_waypoint_for_image.pose.position.y, 
                    'z': self.current_waypoint_for_image.pose.position.z,
                    'qx': self.current_waypoint_for_image.pose.orientation.x,
                    'qy': self.current_waypoint_for_image.pose.orientation.y,
                    'qz': self.current_waypoint_for_image.pose.orientation.z,
                    'qw': self.current_waypoint_for_image.pose.orientation.w
                }
                
                # 存储增强的图像数据
                image_data = {
                    'waypoint_index': self.current_waypoint_index,
                    'waypoint': self.current_waypoint_for_image,
                    'color_filename': color_filename,
                    'depth_heatmap_filename': depth_heatmap_filename,
                    'depth_raw_filename': depth_raw_filename,
                    'timestamp': self.get_clock().now().to_msg(),
                    
                    # 图像数据
                    'color_image': color_rgb,
                    'depth_raw': depth_raw,
                    'depth_heatmap': cv2.cvtColor(depth_heatmap, cv2.COLOR_BGR2RGB),
                    
                    # 相机和几何信息
                    'camera_intrinsics': self.camera_intrinsics,
                    'object_height': self.current_scan_plan.object_height,
                    'scan_height': self.current_scan_plan.scan_height,
                    'scan_area_corners': [
                        {'x': p.x, 'y': p.y} for p in self.current_scan_plan.scan_region
                    ],
                    
                    # waypoint完整6D位姿
                    'waypoint_pose_6d': waypoint_pose_6d
                }
                
                self.captured_images.append(image_data)
                
                self.get_logger().info(f'✅ 图像已保存: waypoint_{self.current_waypoint_index+1:03d} (彩色+深度)')
                self.get_logger().info(f'📁 彩色: {color_filename}')
                self.get_logger().info(f'🔥 深度热度图: {depth_heatmap_filename}')
                self.get_logger().info(f'🗂️  原始深度: {depth_raw_filename}')
                
            except Exception as e:
                self.get_logger().error(f'图像处理失败: {e}')
                import traceback
                traceback.print_exc()

    def _calculate_grid_layout(self):
        """计算网格布局信息"""
        try:
            if not self.current_scan_plan.waypoints:
                return None
            
            # 提取所有waypoint位置
            positions = []
            for wp in self.current_scan_plan.waypoints:
                positions.append((wp.pose.position.x, wp.pose.position.y))
            
            positions = np.array(positions)
            
            # 分析网格结构
            unique_x = np.unique(np.round(positions[:, 0], 1))
            unique_y = np.unique(np.round(positions[:, 1], 1))
            
            grid_layout = {
                'num_rows': len(unique_x),
                'num_cols': len(unique_y),
                'x_positions': sorted(unique_x.tolist()),
                'y_positions': sorted(unique_y.tolist()),
                'is_regular_grid': len(positions) == len(unique_x) * len(unique_y),
                'total_waypoints': len(self.current_scan_plan.waypoints)
            }
            
            # 分析蛇形模式
            if grid_layout['is_regular_grid']:
                grid_layout['snake_pattern'] = True
                grid_layout['current_grid_pos'] = self._find_grid_position(
                    self.current_waypoint_for_image.pose.position.x,
                    self.current_waypoint_for_image.pose.position.y,
                    grid_layout
                )
            
            return grid_layout
            
        except Exception as e:
            self.get_logger().error(f'网格布局计算失败: {e}')
            return None

    def _find_grid_position(self, x, y, grid_layout):
        """找到当前waypoint在网格中的位置"""
        try:
            # 找到最接近的网格位置
            x_idx = None
            y_idx = None
            
            min_x_dist = float('inf')
            for i, grid_x in enumerate(grid_layout['x_positions']):
                dist = abs(x - grid_x)
                if dist < min_x_dist:
                    min_x_dist = dist
                    x_idx = i
            
            min_y_dist = float('inf')
            for i, grid_y in enumerate(grid_layout['y_positions']):
                dist = abs(y - grid_y)
                if dist < min_y_dist:
                    min_y_dist = dist
                    y_idx = i
            
            return (x_idx, y_idx) if x_idx is not None and y_idx is not None else None
            
        except Exception as e:
            self.get_logger().error(f'网格位置计算失败: {e}')
            return None

    def _calculate_overlap_info(self):
        """计算重叠信息"""
        try:
            # 计算FOV实际覆盖尺寸
            scan_height = self.current_scan_plan.scan_height
            object_height = self.current_scan_plan.object_height
            effective_height = scan_height - object_height
            
            # 相机FOV (从scan_planner获取)
            fx, fy = self.camera_intrinsics['fx'], self.camera_intrinsics['fy']
            camera_width, camera_height = 1280, 720
            
            fov_h = 2 * math.atan(camera_width / (2 * fx))
            fov_v = 2 * math.atan(camera_height / (2 * fy))
            
            # 实际覆盖尺寸
            fov_coverage_width = 2 * effective_height * math.tan(fov_h / 2)
            fov_coverage_height = 2 * effective_height * math.tan(fov_v / 2)
            
            overlap_info = {
                'effective_height': effective_height,
                'fov_coverage_width_mm': fov_coverage_width,
                'fov_coverage_height_mm': fov_coverage_height,
                'fov_h_degrees': math.degrees(fov_h),
                'fov_v_degrees': math.degrees(fov_v)
            }
            
            # 如果有相邻waypoint，计算实际重叠率
            current_pos = (
                self.current_waypoint_for_image.pose.position.x,
                self.current_waypoint_for_image.pose.position.y
            )
            
            adjacent_overlaps = []
            for wp in self.current_scan_plan.waypoints:
                wp_pos = (wp.pose.position.x, wp.pose.position.y)
                if wp_pos != current_pos:
                    distance = math.sqrt((wp_pos[0] - current_pos[0])**2 + (wp_pos[1] - current_pos[1])**2)
                    
                    # 计算重叠率（简化版）
                    if distance < fov_coverage_width:
                        x_overlap = max(0, fov_coverage_width - abs(wp_pos[1] - current_pos[1]))
                        overlap_ratio_x = x_overlap / fov_coverage_width
                        adjacent_overlaps.append({
                            'waypoint_pos': wp_pos,
                            'distance': distance,
                            'overlap_ratio_x': overlap_ratio_x
                        })
            
            overlap_info['adjacent_overlaps'] = adjacent_overlaps
            
            return overlap_info
            
        except Exception as e:
            self.get_logger().error(f'重叠信息计算失败: {e}')
            return None

    def _finish_scan_execution(self):
        """完成扫描执行"""
        try:
            # 停止扫描定时器
            if hasattr(self, 'scan_timer'):
                self.scan_timer.destroy()
            
            self.execution_active = False
            
            self.get_logger().info(f'扫描执行完成！')
            self.get_logger().info(f'采集图像数量: {len(self.captured_images)}')
            self.get_logger().info(f'输出目录: {self.output_dir}')
            
            # 🆕 修复：无论单点还是多点，都通过拼接服务处理
            self._start_stitching_process()
                
        except Exception as e:
            self.get_logger().error(f'扫描完成处理失败: {e}')

    def _start_stitching_process(self):
        """启动拼接处理 - 适配重构后的Smart Stitcher"""
        try:
            # 🆕 移除单点判断，让所有情况都通过拼接服务
            self.get_logger().info('开始智能图像拼接处理...')
            
            # 创建拼接服务客户端
            stitch_client = self.create_client(ProcessStitching, 'process_stitching')
            
            if not stitch_client.wait_for_service(timeout_sec=5.0):
                self.get_logger().error('拼接服务不可用')
                # 🆕 备用方案：如果拼接服务不可用，直接触发检测
                self._trigger_detection_for_fallback()
                return
            
            # 准备拼接请求
            request = ProcessStitching.Request()
            request.scan_plan = self.current_scan_plan
            request.output_directory = self.output_dir
            
            # 🆕 改进的图像数据准备
            for img_data in self.captured_images:
                image_msg = ImageData()
                
                # 使用完整的文件路径
                image_msg.filename = img_data.get('color_filename', f'waypoint_{img_data["waypoint_index"]}')
                image_msg.timestamp = img_data['timestamp']
                image_msg.waypoint = img_data['waypoint']
                
                # 转换图像为ROS消息
                img_rgb = img_data['color_image']
                img_msg = self.bridge.cv2_to_imgmsg(img_rgb, "rgb8")
                image_msg.image = img_msg
                
                request.image_data.append(image_msg)
                
                # 记录调试信息
                scan_type = "single_point" if len(self.captured_images) == 1 else "多点"
                self.get_logger().info(f'准备{scan_type}图像数据: waypoint_{img_data["waypoint_index"]}')
                self.get_logger().info(f'  - 彩色文件: {img_data.get("color_filename", "N/A")}')
                self.get_logger().info(f'  - 深度文件: {img_data.get("depth_raw_filename", "N/A")}')
            
            scan_type = "单点扫描" if len(self.captured_images) == 1 else "multi_point"
            self.get_logger().info(f'📤 发送{scan_type}数据到拼接服务: {len(request.image_data)} 张图像')
            
            # 异步调用拼接服务
            future = stitch_client.call_async(request)
            future.add_done_callback(self.stitching_response_callback)
            
        except Exception as e:
            self.get_logger().error(f'拼接处理启动失败: {e}')
            import traceback
            traceback.print_exc()
            # 🆕 出错时的备用方案
            self._trigger_detection_for_fallback()


    def stitching_response_callback(self, future):
        """拼接服务响应回调"""
        try:
            response = future.result()
            if response.success:
                self.get_logger().info(f'拼接完成: {response.message}')
                self.get_logger().info(f'结果文件: {response.result.output_path}')
            else:
                self.get_logger().error(f'拼接失败: {response.message}')
        except Exception as e:
            self.get_logger().error(f'拼接响应处理失败: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = ScanExecutorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()