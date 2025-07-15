#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from vision_ai_interfaces.srv import ProcessStitching
from vision_ai_interfaces.msg import StitchResult, ImageData
from sensor_msgs.msg import Image
import cv2
import numpy as np
import math
import os
from datetime import datetime
from cv_bridge import CvBridge
from std_msgs.msg import String
class SmartStitcherNode(Node):
    def __init__(self):
        super().__init__('smart_stitcher_node')
        
        # 创建服务
        self.stitch_service = self.create_service(
            ProcessStitching,
            'process_stitching', 
            self.stitch_callback
        )
        
        self.stitching_complete_pub = self.create_publisher(
            String,
            '/stitching_complete',
            10
        )
        
        # 🆕 发布者 - 发布最终参考图像
        self.reference_image_pub = self.create_publisher(
            Image,
            '/reference_image',
            10
        )
        
        # 🆕 发布者 - 发布参考深度信息
        self.reference_depth_pub = self.create_publisher(
            Image,
            '/reference_depth',
            10
        )

        self.bridge = CvBridge()
        
        # 相机参数
        self.camera_width = 1280
        self.camera_height = 720
        self.fx = 912.694580078125
        self.fy = 910.309814453125
        self.cx = 640
        self.cy = 360
        
        # FOV计算
        self.fov_h = 2 * math.atan(self.camera_width / (2 * self.fx))
        self.fov_v = 2 * math.atan(self.camera_height / (2 * self.fy))
        
        self.get_logger().info('智能拼接节点已启动 (双轴优化版)')
        self.get_logger().info(f'FOV: {math.degrees(self.fov_h):.1f}° × {math.degrees(self.fov_v):.1f}°')

    def stitch_callback(self, request, response):
        """处理拼接请求"""
        try:
            self.get_logger().info(f'收到拼接请求: {len(request.image_data)} 张图像')
            
            # 转换输入数据
            image_data = self._convert_input_data(request.image_data)
            scan_plan = request.scan_plan
            
            if not image_data:
                response.success = False
                response.message = "图像数据转换失败"
                return response
            
            # 根据策略选择处理模式
            if scan_plan.strategy == "single_point" or len(image_data) == 1:
                result_path, method = self._process_single_point(image_data[0], scan_plan, request.output_directory)
            else:
                result_path, method = self._process_multi_point_dual_axis(image_data, scan_plan, request.output_directory)
            
            if result_path:
                response.success = True
                response.message = f"拼接成功: {method}"
                response.result = StitchResult()
                
                response.result.method = method
                response.result.output_path = result_path
                response.result.input_images = len(request.image_data)
            else:
                response.success = False
                response.message = "拼接失败"
                
        except Exception as e:
            response.success = False
            response.message = f"拼接处理失败: {str(e)}"
            self.get_logger().error(f'拼接错误: {e}')
            import traceback
            traceback.print_exc()
        
        return response

    def _convert_input_data(self, ros_image_data):
        """转换ROS图像数据为内部格式 - 修复cv_bridge问题"""
        converted_data = []

        for img_data in ros_image_data:
            try:
                # 🆕 修复：安全的图像转换，绕过cv_bridge问题
                self.get_logger().info(f'🎨 调试Waypoint {img_data.waypoint.waypoint_index} 图像转换...')
                try:
                    # 尝试使用passthrough避免格式转换问题
                     # 获取原始ROS图像信息
                    ros_image = img_data.image
                    self.get_logger().info(f'原始ROS图像: {ros_image.width}x{ros_image.height}, 编码: {ros_image.encoding}')
                    
                    # 尝试passthrough模式
                    color_cv_raw = self.bridge.imgmsg_to_cv2(img_data.image, desired_encoding="passthrough")
                    self.get_logger().info(f'passthrough转换后: {color_cv_raw.shape}, dtype: {color_cv_raw.dtype}')
                    
                    # 🆕 检查原始像素值（用于调试颜色）
                    if len(color_cv_raw.shape) == 3:
                        # 取图像中心点的像素值作为调试样本
                        center_y, center_x = color_cv_raw.shape[0]//2, color_cv_raw.shape[1]//2
                        center_pixel = color_cv_raw[center_y, center_x]
                        self.get_logger().info(f'中心像素值(原始): {center_pixel}')
                    
                    # 检查并转换格式
                    if len(color_cv_raw.shape) == 3 and color_cv_raw.shape[2] == 3:
                        if ros_image.encoding == 'bgr8':
                            # BGR -> RGB
                            color_cv = cv2.cvtColor(color_cv_raw, cv2.COLOR_BGR2RGB)
                            self.get_logger().info('执行了BGR->RGB转换')
                        elif ros_image.encoding == 'rgb8':
                            # 已经是RGB，直接使用
                            color_cv = color_cv_raw.copy()
                            self.get_logger().info('图像已是RGB格式，直接使用')
                        else:
                            # 未知编码，尝试BGR->RGB转换
                            color_cv = cv2.cvtColor(color_cv_raw, cv2.COLOR_BGR2RGB)
                            self.get_logger().warn(f'未知编码 {ros_image.encoding}，尝试BGR->RGB转换')
                        
                        # 🆕 检查转换后的像素值
                        center_pixel_after = color_cv[center_y, center_x]
                        self.get_logger().info(f'中心像素值(转换后): {center_pixel_after}')
                        
                except Exception as cv_error:
                    self.get_logger().error(f'cv_bridge转换失败: {cv_error}')
                    
                    # 🆕 备用方案：直接从原始数据构造
                    try:
                        self.get_logger().info('尝试备用图像转换方案...')
                        
                        # 从ROS消息手动提取图像数据
                        ros_image = img_data.image
                        width = ros_image.width
                        height = ros_image.height
                        encoding = ros_image.encoding
                        step = ros_image.step
                        data = ros_image.data
                        
                        self.get_logger().info(f'ROS图像信息: {width}x{height}, 编码: {encoding}, step: {step}')
                        
                        # 转换为numpy数组
                        if encoding == 'rgb8':
                            image_array = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))
                            color_cv = image_array.copy()
                        elif encoding == 'bgr8':
                            image_array = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))
                            color_cv = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
                        else:
                            self.get_logger().error(f'不支持的编码格式: {encoding}')
                            continue
                        
                        self.get_logger().info(f'备用方案转换成功: {color_cv.shape}')
                        
                    except Exception as backup_error:
                        self.get_logger().error(f'备用转换方案也失败: {backup_error}')
                        continue
                
                # 从waypoint提取位置和角度
                wp = img_data.waypoint
                world_x = wp.pose.position.x
                world_y = wp.pose.position.y
                world_z = wp.pose.position.z  # 🆕 添加Z坐标
                
                # 🆕 提取完整的四元数并转换为欧拉角
                qx = wp.pose.orientation.x
                qy = wp.pose.orientation.y
                qz = wp.pose.orientation.z
                qw = wp.pose.orientation.w
                
                # 转换四元数为欧拉角（roll, pitch, yaw）
                from scipy.spatial.transform import Rotation as R
                rotation = R.from_quat([qx, qy, qz, qw])
                roll_rad, pitch_rad, yaw_rad = rotation.as_euler('xyz')
                
                roll_deg = abs(180-math.degrees(roll_rad))
                pitch_deg = math.degrees(pitch_rad)
                yaw_deg = math.degrees(yaw_rad)
                
                # 🆕 推断深度文件路径
                output_dir = getattr(self, 'current_output_dir', None)
                depth_filename = None
                
                if img_data.filename and 'color_waypoint_' in img_data.filename:
                    depth_filename = img_data.filename.replace('color_waypoint_', 'depth_raw_waypoint_').replace('.jpg', '.npy')
                    
                    if output_dir:
                        depth_filepath = os.path.join(output_dir, depth_filename)
                        depth_exists = os.path.exists(depth_filepath)
                        self.get_logger().info(f'  - 推断深度文件: {depth_filename} (存在: {depth_exists})')
                
                converted_item = {
                    'color_image': color_cv,
                    'waypoint': wp,
                    'filename': img_data.filename,
                    'timestamp': img_data.timestamp,
                    'waypoint_index': wp.waypoint_index,
                    
                    # 🆕 完整的位姿信息
                    'world_pos': (world_x, world_y, world_z),  # 包含Z坐标
                    'roll': roll_deg,
                    'pitch': pitch_deg,  
                    'yaw': yaw_deg,
                    
                    # 🆕 原始四元数（备用）
                    'quaternion': (qx, qy, qz, qw),
                    
                    # 文件路径
                    'color_filename': img_data.filename,
                    'depth_raw_filename': depth_filename
                }
                
                self.get_logger().info(f'🔍 Waypoint {wp.waypoint_index} 完整位姿:')
                self.get_logger().info(f'  - 位置: ({world_x:.1f}, {world_y:.1f}, {world_z:.1f})')
                self.get_logger().info(f'  - 姿态: Roll={roll_deg:.1f}°, Pitch={pitch_deg:.1f}°, Yaw={yaw_deg:.1f}°')
                
                converted_data.append(converted_item)
                
            except Exception as e:
                self.get_logger().error(f'转换图像数据失败: {e}')
                continue
        
        return converted_data

    def _process_single_point(self, image_data, scan_plan, output_dir):
        """单点模式：旋转矫正 + 裁剪"""
        try:
            self.get_logger().info('处理单点扫描')
            
            image = image_data['color_image']
            yaw_deg = image_data['yaw']
            
            # 旋转矫正
            corrected_image = self._rotate_image(image, -yaw_deg)
            
            # 简化裁剪
            cropped_image = self._crop_single_point(corrected_image, scan_plan)
            
            # 保存结果
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(output_dir, f"single_point_result_{timestamp}.jpg")
            
            result_bgr = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_path, result_bgr)
            
            self.get_logger().info(f'单点处理完成: {output_path}')
            return output_path, "single_point_corrected"
            
        except Exception as e:
            self.get_logger().error(f'单点处理失败: {e}')
            return None, "failed"

    def _process_multi_point_dual_axis(self, image_data_list, scan_plan, output_dir):
        """多点模式：双轴优化融合"""
        try:
            self.get_logger().info('处理多点扫描 - 双轴优化融合')
            
            # 计算FOV覆盖参数
            fov_params = self._calculate_fov_parameters(scan_plan)
            
            # 计算理论参数
            theoretical_params = self._calculate_theoretical_parameters(image_data_list, scan_plan, fov_params)
            
            # 应用双轴优化参数（基于你的成功配置）
            dual_axis_params = {
                'margin_ratio_x': 0.01,     # 基于理论 + 微调
                'margin_ratio_y': 0.01,     # 基于理论 + 微调
                'blend_size_x': theoretical_params.get('blend_size_x', 60),
                'blend_size_y': theoretical_params.get('blend_size_y', 70),
                'scale_adjust_x': 1,    # 你的成功参数
                'scale_adjust_y': 1,    # 你的成功参数
                'offset_adjust_x': 0,
                'offset_adjust_y': 0       # 可根据需要调整
            }
            
            self.get_logger().info(f'双轴参数: X缩放={dual_axis_params["scale_adjust_x"]}, Y缩放={dual_axis_params["scale_adjust_y"]}')
            
            # 执行双轴融合
            stitched_image = self._dual_axis_fusion_stitching(image_data_list, scan_plan, fov_params, dual_axis_params)
            
            if stitched_image is None:
                return None, "fusion_failed"
            
            # 保存拼接结果
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            stitched_path = os.path.join(output_dir, f"dual_axis_stitched_{timestamp}.jpg")
            stitched_bgr = cv2.cvtColor(stitched_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(stitched_path, stitched_bgr)
            self.get_logger().info(f'双轴拼接完成: {stitched_path}')
            
            # 精确裁剪到scan area
            final_image = self._crop_to_scan_area_dual_axis(stitched_image, scan_plan, fov_params, dual_axis_params)
            
            # 保存最终结果
            final_path = os.path.join(output_dir, f"final_dual_axis_result_{timestamp}.jpg")
            final_bgr = cv2.cvtColor(final_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(final_path, final_bgr)
            self._save_fusion_mapping(output_dir)
            self.get_logger().info(f'最终结果: {final_path}')
            self.get_logger().info(f'尺寸变化: {stitched_image.shape[1]}×{stitched_image.shape[0]} → {final_image.shape[1]}×{final_image.shape[0]}')
            # 第193行修改为：
            self._publish_reference_data(final_image, None, output_dir)
            return final_path, "dual_axis_optimized_fusion"
            
        except Exception as e:
            self.get_logger().error(f'多点处理失败: {e}')
            import traceback
            traceback.print_exc()
            return None, "failed"

    def _calculate_fov_parameters(self, scan_plan):
        """计算FOV相关参数"""
        scan_height = scan_plan.scan_height
        object_height = scan_plan.object_height
        effective_height = scan_height - object_height
        
        # FOV覆盖尺寸
        fov_width_mm = 2 * effective_height * math.tan(self.fov_h / 2)
        fov_height_mm = 2 * effective_height * math.tan(self.fov_v / 2)
        
        # 像素密度
        pixels_per_mm_x = self.camera_width / fov_width_mm
        pixels_per_mm_y = self.camera_height / fov_height_mm
        
        return {
            'effective_height': effective_height,
            'fov_width_mm': fov_width_mm,
            'fov_height_mm': fov_height_mm,
            'pixels_per_mm_x': pixels_per_mm_x,
            'pixels_per_mm_y': pixels_per_mm_y
        }

    def _calculate_theoretical_parameters(self, image_data_list, scan_plan, fov_params):
        """计算理论融合参数"""
        try:
            # 分析waypoint间距
            positions = [(img['world_pos'][0], img['world_pos'][1]) for img in image_data_list]
            
            distances_x = []
            distances_y = []
            
            for i in range(len(positions)):
                for j in range(i+1, len(positions)):
                    dx = abs(positions[i][0] - positions[j][0])
                    dy = abs(positions[i][1] - positions[j][1])
                    
                    if dx < 400 and dy < 400:  # 相邻waypoint阈值
                        if dx > 0:
                            distances_x.append(dx)
                        if dy > 0:
                            distances_y.append(dy)
            
            # 平均间距
            avg_distance_x = sum(distances_x) / len(distances_x) if distances_x else fov_params['fov_height_mm']
            avg_distance_y = sum(distances_y) / len(distances_y) if distances_y else fov_params['fov_width_mm']
            
            # 理论重叠率
            overlap_x = max(0, (fov_params['fov_height_mm'] - avg_distance_x)*1.5 / fov_params['fov_height_mm'])
            overlap_y = max(0, (fov_params['fov_width_mm'] - avg_distance_y)*1.5 / fov_params['fov_width_mm'])
            
            # 建议融合区域
            blend_size_x = max(40, int(self.camera_height * overlap_x * 1.5))
            blend_size_y = max(600, int(self.camera_width * overlap_y * 1.5))
            
            self.get_logger().info(f'理论参数: 重叠率X={overlap_x:.3f}, Y={overlap_y:.3f}')
            self.get_logger().info(f'建议融合区域: X={blend_size_x}px, Y={blend_size_y}px')
            
            return {
                'overlap_x': overlap_x,
                'overlap_y': overlap_y,
                'blend_size_x': blend_size_x,
                'blend_size_y': blend_size_y
            }
            
        except Exception as e:
            self.get_logger().error(f'理论参数计算失败: {e}')
            return {'blend_size_x': 60, 'blend_size_y': 70}

    def _dual_axis_fusion_stitching(self, image_data_list, scan_plan, fov_params, dual_axis_params):
        """双轴融合拼接"""
        try:
            if not image_data_list:
                return None
            
            self.get_logger().info('开始双轴融合拼接...')
            
            # 获取第一个图像的yaw角度（假设所有图像角度相同）
            yaw_deg = image_data_list[0]['yaw']
            yaw_rad = math.radians(yaw_deg)
            
            # 计算scan area信息
            scan_region = scan_plan.scan_region
            if not scan_region or len(scan_region) < 4:
                self.get_logger().error('缺少scan region信息')
                return None
            
            region_x = [p.x for p in scan_region]
            region_y = [p.y for p in scan_region]
            scan_x_min, scan_x_max = min(region_x), max(region_x)
            scan_y_min, scan_y_max = min(region_y), max(region_y)
            scan_center_x = (scan_x_min + scan_x_max) / 2
            scan_center_y = (scan_y_min + scan_y_max) / 2
            
            # 计算旋转后的边界
            scan_width = scan_y_max - scan_y_min
            scan_height = scan_x_max - scan_x_min
            
            cos_yaw = abs(math.cos(yaw_rad))
            sin_yaw = abs(math.sin(yaw_rad))
            rotated_width = scan_width * cos_yaw + scan_height * sin_yaw
            rotated_height = scan_height * cos_yaw + scan_width * sin_yaw
            
            # 双轴画布尺寸
            canvas_width = int(rotated_width * fov_params['pixels_per_mm_x'] * 
                             (1 + dual_axis_params['margin_ratio_x']) * dual_axis_params['scale_adjust_x'])
            canvas_height = int(rotated_height * fov_params['pixels_per_mm_y'] * 
                              (1 + dual_axis_params['margin_ratio_y']) * dual_axis_params['scale_adjust_y'])
            
            self.get_logger().info(f'双轴画布: {canvas_width}×{canvas_height}')
            
            self.fusion_mapping = {}  # 存储 {(x_stitched, y_stitched): source_info}
            self.waypoint_contributions = {}  # 存储每个waypoint对画布的贡献区域
            # 创建画布
            canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.float32)
            weight_map = np.zeros((canvas_height, canvas_width), dtype=np.float32)
           
            canvas_center_x = canvas_width // 2
            canvas_center_y = canvas_height // 2
            
            # 融合每张图像
            for img_data in image_data_list:
                image = img_data['color_image'].astype(np.float32)
                world_x, world_y, world_z = img_data['world_pos']
                waypoint_idx = img_data['waypoint_index']
                # 世界坐标偏移
                offset_x = world_x - scan_center_x
                offset_y = world_y - scan_center_y
                
                # 旋转变换
                rotated_x = offset_x * math.cos(-yaw_rad) - offset_y * math.sin(-yaw_rad)
                rotated_y = offset_x * math.sin(-yaw_rad) + offset_y * math.cos(-yaw_rad)
                
                # 双轴画布位置
                canvas_pos_x = (canvas_center_x + 
                               int(rotated_y * fov_params['pixels_per_mm_x'] * dual_axis_params['scale_adjust_x']) + 
                               dual_axis_params['offset_adjust_x'])
                canvas_pos_y = (canvas_center_y + 
                               int(rotated_x * fov_params['pixels_per_mm_y'] * dual_axis_params['scale_adjust_y']) + 
                               dual_axis_params['offset_adjust_y'])
                
                # 双轴融合掩码
                mask = self._create_dual_axis_mask(
                    image.shape[:2], 
                    dual_axis_params['blend_size_x'], 
                    dual_axis_params['blend_size_y']
                )
                # 🆕 记录这个waypoint的贡献区域
                self._record_waypoint_contribution(
                    image, canvas_pos_x, canvas_pos_y, waypoint_idx, 
                    canvas_width, canvas_height, img_data
                )
                
                # 融合到画布
                self._blend_to_canvas(canvas, weight_map, image, mask, canvas_pos_x, canvas_pos_y)
                
                self.get_logger().info(f'融合图像 {img_data["waypoint_index"]}: 画布位置({canvas_pos_x},{canvas_pos_y})')
            
            # 归一化结果
            result = self._normalize_canvas(canvas, weight_map)
            
            # 保存融合信息用于后续裁剪
            self._fusion_info = {
                'scan_center': (scan_center_x, scan_center_y),
                'canvas_center': (canvas_center_x, canvas_center_y),
                'yaw_rad': yaw_rad,
                'dual_axis_params': dual_axis_params
            }
            
            self.get_logger().info('双轴融合拼接完成')
            return result
            
        except Exception as e:
            self.get_logger().error(f'双轴融合失败: {e}')
            import traceback
            traceback.print_exc()
            return None

    def _create_dual_axis_mask(self, image_shape, blend_size_x, blend_size_y):
        """创建双轴融合掩码"""
        h, w = image_shape
        mask = np.ones((h, w), dtype=np.float32)
        
        # X轴方向融合（水平边缘）
        for x in range(w):
            dist_from_x_edge = min(x, w - 1 - x)
            if dist_from_x_edge < blend_size_x:
                weight_x = dist_from_x_edge / blend_size_x
                mask[:, x] *= weight_x
        
        # Y轴方向融合（垂直边缘）
        for y in range(h):
            dist_from_y_edge = min(y, h - 1 - y)
            if dist_from_y_edge < blend_size_y:
                weight_y = dist_from_y_edge / blend_size_y
                mask[y, :] *= weight_y
        
        return mask

    def _blend_to_canvas(self, canvas, weight_map, image, mask, pos_x, pos_y):
        """融合图像到画布"""
        try:
            img_h, img_w = image.shape[:2]
            canvas_h, canvas_w = canvas.shape[:2]
            
            # 计算放置区域
            img_left = pos_x - img_w // 2
            img_top = pos_y - img_h // 2
            img_right = img_left + img_w
            img_bottom = img_top + img_h
            
            # 画布有效区域
            canvas_left = max(0, img_left)
            canvas_top = max(0, img_top)
            canvas_right = min(canvas_w, img_right)
            canvas_bottom = min(canvas_h, img_bottom)
            
            # 图像对应区域
            img_crop_left = max(0, -img_left)
            img_crop_top = max(0, -img_top)
            img_crop_right = img_crop_left + (canvas_right - canvas_left)
            img_crop_bottom = img_crop_top + (canvas_bottom - canvas_top)
            
            if (canvas_right > canvas_left and canvas_bottom > canvas_top and
                img_crop_right > img_crop_left and img_crop_bottom > img_crop_top):
                
                # 提取区域
                img_region = image[img_crop_top:img_crop_bottom, img_crop_left:img_crop_right]
                mask_region = mask[img_crop_top:img_crop_bottom, img_crop_left:img_crop_right]
                
                # 验证尺寸匹配
                if img_region.shape[:2] == mask_region.shape:
                    # 融合
                    for c in range(3):
                        canvas[canvas_top:canvas_bottom, canvas_left:canvas_right, c] += img_region[:, :, c] * mask_region
                    
                    weight_map[canvas_top:canvas_bottom, canvas_left:canvas_right] += mask_region
                
        except Exception as e:
            self.get_logger().error(f'画布融合失败: {e}')

    def _normalize_canvas(self, canvas, weight_map):
        """归一化画布"""
        valid_mask = weight_map > 0
        result = np.zeros_like(canvas, dtype=np.uint8)
        
        for c in range(3):
            channel = canvas[:, :, c].copy()
            channel[valid_mask] /= weight_map[valid_mask]
            result[:, :, c] = np.clip(channel, 0, 255).astype(np.uint8)
        
        return result

    def _process_single_point(self, image_data, scan_plan, output_dir):
        """单点模式：旋转矫正 + 裁剪 + 映射信息保存"""
        try:
            self.get_logger().info('处理单点扫描')
            
            image = image_data['color_image']
            yaw_deg = image_data['yaw']
            
            # 旋转矫正
            corrected_image = self._rotate_image(image, -yaw_deg)
            
            # 简化裁剪
            cropped_image = self._crop_single_point(corrected_image, scan_plan)
            
            # 🆕 为单点扫描创建映射信息
            self._create_single_point_mapping(image_data, cropped_image, output_dir)
            
            # 保存结果
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(output_dir, f"single_point_result_{timestamp}.jpg")
            
            result_bgr = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_path, result_bgr)
            
            self.get_logger().info(f'单点处理完成: {output_path}')
            
            # 发布参考数据
            self._publish_reference_data(cropped_image, None, output_dir)
            return output_path, "single_point_corrected"
            
        except Exception as e:
            self.get_logger().error(f'单点处理失败: {e}')
            return None, "failed"

    def _create_single_point_mapping(self, image_data, processed_image, output_dir):
        """为单点扫描创建映射信息"""
        try:
            import pickle
            import json
            
            # 单点扫描的映射相对简单：整个处理后的图像都来自同一个waypoint
            waypoint_idx = image_data['waypoint_index']
            h, w = processed_image.shape[:2]
            
            self.get_logger().info(f'🆕 创建单点映射信息: Waypoint {waypoint_idx}, 尺寸 {w}×{h}')
            
            # 创建简单的1:1映射（简化版本，不需要存储每个像素）
            fusion_mapping = {}
            # 对于单点，我们只存储关键信息，不存储每个像素的映射
            
            waypoint_contributions = {
                waypoint_idx: {
                    'pixel_count': w * h,
                    'coverage_area': (0, 0, w, h),
                    'waypoint_data': {
                        'waypoint_index': waypoint_idx,
                        'color_filename': image_data.get('color_filename', ''),
                        'depth_raw_filename': image_data.get('depth_raw_filename', ''),
                        'world_pos': image_data.get('world_pos', (0, 0, 0)),
                        'roll': image_data.get('roll', 0),
                        'pitch': image_data.get('pitch', 0),
                        'yaw': image_data.get('yaw', 0),
                        'quaternion': image_data.get('quaternion', (0,0,0,1))
                    }
                }
            }
            
            # 保存映射信息
            mapping_file = os.path.join(output_dir, "fusion_mapping.pkl")
            with open(mapping_file, 'wb') as f:
                pickle.dump({
                    'fusion_mapping': fusion_mapping,  # 单点时为空字典，表示使用简化模式
                    'waypoint_contributions': waypoint_contributions,
                    'fusion_params': {
                        'single_point': True,
                        'canvas_size': (w, h),
                        'yaw_correction': -image_data.get('yaw', 0),
                        'waypoint_index': waypoint_idx
                    }
                }, f)
            
            # 保存摘要信息
            summary_file = os.path.join(output_dir, "fusion_mapping_summary.json")
            summary_data = {
                'scan_type': 'single_point',
                'total_mapped_pixels': w * h,
                'canvas_size': [w, h],
                'waypoint_contributions': {
                    str(waypoint_idx): {
                        'pixel_count': w * h,
                        'coverage_percentage': 100.0,
                        'waypoint_index': waypoint_idx,
                        'source_files': {
                            'color': image_data.get('color_filename', ''),
                            'depth': image_data.get('depth_raw_filename', '')
                        }
                    }
                }
            }
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
            self.get_logger().info(f'✅ 单点映射信息已保存: waypoint_{waypoint_idx} -> {w}×{h} 像素')
            
        except Exception as e:
            self.get_logger().error(f'保存单点映射信息失败: {e}')

    def _crop_to_scan_area_dual_axis(self, stitched_image, scan_plan, fov_params, dual_axis_params):
        """双轴优化的scan area裁剪"""
        try:
            if not hasattr(self, '_fusion_info'):
                self.get_logger().warn('缺少融合信息，使用简化裁剪')
                return self._crop_single_point(stitched_image, scan_plan)
            
            fusion_info = self._fusion_info
            
            # scan area边界
            scan_region = scan_plan.scan_region
            region_x = [p.x for p in scan_region]
            region_y = [p.y for p in scan_region]
            
            scan_x_min, scan_x_max = min(region_x), max(region_x)
            scan_y_min, scan_y_max = min(region_y), max(region_y)
            
            # 融合信息
            scan_center_x, scan_center_y = fusion_info['scan_center']
            canvas_center_x, canvas_center_y = fusion_info['canvas_center']
            yaw_rad = fusion_info['yaw_rad']
            
            # 计算scan area边界在画布中的位置
            corners_world = [
                (scan_x_min - scan_center_x, scan_y_min - scan_center_y),
                (scan_x_max - scan_center_x, scan_y_min - scan_center_y),
                (scan_x_max - scan_center_x, scan_y_max - scan_center_y),
                (scan_x_min - scan_center_x, scan_y_max - scan_center_y)
            ]
            
            # 旋转并转换为画布坐标
            corners_canvas = []
            for offset_x, offset_y in corners_world:
                rotated_x = offset_x * math.cos(-yaw_rad) - offset_y * math.sin(-yaw_rad)
                rotated_y = offset_x * math.sin(-yaw_rad) + offset_y * math.cos(-yaw_rad)
                
                canvas_x = canvas_center_x + int(rotated_y * fov_params['pixels_per_mm_x'] * dual_axis_params['scale_adjust_x'])
                canvas_y = canvas_center_y + int(rotated_x * fov_params['pixels_per_mm_y'] * dual_axis_params['scale_adjust_y'])
                
                corners_canvas.append((canvas_x, canvas_y))
            
            # 计算边界框
            canvas_xs = [p[0] for p in corners_canvas]
            canvas_ys = [p[1] for p in corners_canvas]
            
            crop_left = max(0, min(canvas_xs))
            crop_right = min(stitched_image.shape[1], max(canvas_xs))
            crop_top = max(0, min(canvas_ys))
            crop_bottom = min(stitched_image.shape[0], max(canvas_ys))
            
            # 执行裁剪
            if crop_right > crop_left and crop_bottom > crop_top:
                cropped = stitched_image[crop_top:crop_bottom, crop_left:crop_right]
                self.get_logger().info(f'双轴裁剪: {stitched_image.shape[1]}×{stitched_image.shape[0]} → {cropped.shape[1]}×{cropped.shape[0]}')
                return cropped
            else:
                self.get_logger().warn('裁剪区域无效，返回原图')
                return stitched_image
            
        except Exception as e:
            self.get_logger().error(f'双轴裁剪失败: {e}')
            return stitched_image

    def _crop_single_point(self, image, scan_plan):
        """单点简化裁剪"""
        h, w = image.shape[:2]
        crop_ratio = 0.8
        margin_w = int(w * (1 - crop_ratio) / 2)
        margin_h = int(h * (1 - crop_ratio) / 2)
        return image[margin_h:h-margin_h, margin_w:w-margin_w]

    def _rotate_image(self, image, angle_deg):
        """旋转图像"""
        if abs(angle_deg) < 1:
            return image
        
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle_deg, 1.0)
        
        cos_theta = abs(rotation_matrix[0, 0])
        sin_theta = abs(rotation_matrix[0, 1])
        new_w = int((h * sin_theta) + (w * cos_theta))
        new_h = int((h * cos_theta) + (w * sin_theta))
        
        rotation_matrix[0, 2] += (new_w / 2) - center[0]
        rotation_matrix[1, 2] += (new_h / 2) - center[1]
        
        return cv2.warpAffine(image, rotation_matrix, (new_w, new_h), 
                             borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))


    def _publish_reference_data(self, stitched_image, depth_data, output_dir):
        """发布参考图像数据供检测节点使用 - 修复cv_bridge问题"""
        try:
            # 1. 发布拼接完成信号
            complete_msg = String()
            complete_msg.data = output_dir
            self.stitching_complete_pub.publish(complete_msg)
            self.get_logger().info(f'📢 发布拼接完成信号: {output_dir}')
            
            # 2. 发布最终参考图像（修复cv_bridge）
            if stitched_image is not None:
                try:
                    # 确保图像是RGB格式
                    if len(stitched_image.shape) == 3:
                        # 🆕 修复：手动创建ROS消息，避免cv_bridge问题
                        reference_msg = Image()
                        reference_msg.header.stamp = self.get_clock().now().to_msg()
                        reference_msg.header.frame_id = "stitched_frame"
                        reference_msg.height = stitched_image.shape[0]
                        reference_msg.width = stitched_image.shape[1]
                        reference_msg.encoding = "rgb8"
                        reference_msg.is_bigendian = False
                        reference_msg.step = stitched_image.shape[1] * 3
                        reference_msg.data = stitched_image.tobytes()
                    else:
                        # 单通道图像
                        reference_msg = Image()
                        reference_msg.header.stamp = self.get_clock().now().to_msg()
                        reference_msg.header.frame_id = "stitched_frame"
                        reference_msg.height = stitched_image.shape[0]
                        reference_msg.width = stitched_image.shape[1]
                        reference_msg.encoding = "mono8"
                        reference_msg.is_bigendian = False
                        reference_msg.step = stitched_image.shape[1]
                        reference_msg.data = stitched_image.tobytes()
                    
                    self.reference_image_pub.publish(reference_msg)
                    self.get_logger().info('📸 发布参考图像（修复版）')
                    
                except Exception as img_error:
                    self.get_logger().error(f'参考图像发布失败: {img_error}')
            
            # 3. 发布深度信息（如果有）
            if depth_data is not None:
                try:
                    # 🆕 修复：手动创建深度消息
                    if depth_data.dtype != np.uint16:
                        depth_data = depth_data.astype(np.uint16)
                    
                    depth_msg = Image()
                    depth_msg.header.stamp = self.get_clock().now().to_msg()
                    depth_msg.header.frame_id = "stitched_frame"
                    depth_msg.height = depth_data.shape[0]
                    depth_msg.width = depth_data.shape[1]
                    depth_msg.encoding = "16UC1"
                    depth_msg.is_bigendian = False
                    depth_msg.step = depth_data.shape[1] * 2
                    depth_msg.data = depth_data.tobytes()
                    
                    self.reference_depth_pub.publish(depth_msg)
                    self.get_logger().info('📏 发布深度信息（修复版）')
                    
                except Exception as depth_error:
                    self.get_logger().error(f'深度信息发布失败: {depth_error}')
            else:
                self.get_logger().info('📏 深度数据不可用，跳过深度发布')
            
        except Exception as e:
            self.get_logger().error(f'发布参考数据失败: {e}')
            
    def _record_waypoint_contribution(self, image, canvas_pos_x, canvas_pos_y, waypoint_idx, 
                                canvas_width, canvas_height, img_data):
        """记录waypoint对画布的贡献映射"""
        try:
            img_h, img_w = image.shape[:2]
            
            # 计算在画布上的实际放置区域
            img_left = canvas_pos_x - img_w // 2
            img_top = canvas_pos_y - img_h // 2
            img_right = img_left + img_w
            img_bottom = img_top + img_h
            
            # 画布有效区域
            canvas_left = max(0, img_left)
            canvas_top = max(0, img_top)
            canvas_right = min(canvas_width, img_right)
            canvas_bottom = min(canvas_height, img_bottom)
            
            # 图像对应区域
            img_crop_left = max(0, -img_left)
            img_crop_top = max(0, -img_top)
            
            # 为每个有效像素创建映射记录
            for canvas_y in range(canvas_top, canvas_bottom):
                for canvas_x in range(canvas_left, canvas_right):
                    # 计算在原图中的位置
                    img_x = img_crop_left + (canvas_x - canvas_left)
                    img_y = img_crop_top + (canvas_y - canvas_top)
                    
                    # 确保在原图范围内
                    if 0 <= img_x < img_w and 0 <= img_y < img_h:
                        # 🆕 增强的映射信息，包含完整位姿
                        mapping_info = {
                            'source_waypoint': waypoint_idx,
                            'source_pixel': (img_x, img_y),
                            'waypoint_data': {
                                'waypoint_index': waypoint_idx,
                                'world_pos': img_data.get('world_pos', (0, 0, 0)),  # 🆕 包含Z
                                'roll': img_data.get('roll', 0),                     # 🆕 Roll
                                'pitch': img_data.get('pitch', 0),                   # 🆕 Pitch
                                'yaw': img_data.get('yaw', 0),                       # 🆕 Yaw
                                'quaternion': img_data.get('quaternion', (0,0,0,1)), # 🆕 四元数
                                'color_filename': img_data.get('color_filename', ''),
                                'depth_raw_filename': img_data.get('depth_raw_filename', ''),
                                'full_data': img_data  # 保留完整数据
                            },
                            'transform_info': {
                                'canvas_pos': (canvas_pos_x, canvas_pos_y),
                                'world_pos': img_data.get('world_pos', (0, 0, 0)),
                                'full_pose': {
                                    'position': img_data.get('world_pos', (0, 0, 0)),
                                    'orientation': {
                                        'roll': img_data.get('roll', 0),
                                        'pitch': img_data.get('pitch', 0),
                                        'yaw': img_data.get('yaw', 0)
                                    }
                                }
                            }
                        }
                        
                        # 如果已有映射，选择权重更高的
                        if (canvas_x, canvas_y) in self.fusion_mapping:
                            # 可以根据距离图像中心的远近来判断权重
                            existing = self.fusion_mapping[(canvas_x, canvas_y)]
                            current_distance = math.sqrt((img_x - img_w//2)**2 + (img_y - img_h//2)**2)
                            existing_dist = existing.get('distance_from_center', float('inf'))
                            
                            if current_distance < existing_dist:
                                mapping_info['distance_from_center'] = current_distance
                                self.fusion_mapping[(canvas_x, canvas_y)] = mapping_info
                        else:
                            mapping_info['distance_from_center'] = math.sqrt((img_x - img_w//2)**2 + (img_y - img_h//2)**2)
                            self.fusion_mapping[(canvas_x, canvas_y)] = mapping_info
            
            if waypoint_idx not in self.waypoint_contributions:
                self.waypoint_contributions[waypoint_idx] = {
                    'pixel_count': 0,
                    'coverage_area': (canvas_left, canvas_top, canvas_right, canvas_bottom),
                    'waypoint_data': {
                        'waypoint_index': waypoint_idx,
                        'color_filename': img_data.get('color_filename', ''),
                        'depth_raw_filename': img_data.get('depth_raw_filename', ''),
                        'world_pos': img_data.get('world_pos', (0, 0, 0)),
                        'roll': img_data.get('roll', 0),
                        'pitch': img_data.get('pitch', 0),
                        'yaw': img_data.get('yaw', 0),
                        'quaternion': img_data.get('quaternion', (0,0,0,1))
                    }
                }
            
            contribution_pixels = (canvas_right - canvas_left) * (canvas_bottom - canvas_top)
            self.waypoint_contributions[waypoint_idx]['pixel_count'] += contribution_pixels
            
            self.get_logger().info(f'Waypoint {waypoint_idx} 贡献区域: {contribution_pixels} 像素')
            self.get_logger().info(f'  - 完整位姿: 位置{img_data.get("world_pos", (0,0,0))}, 姿态({img_data.get("roll", 0):.1f}°, {img_data.get("pitch", 0):.1f}°, {img_data.get("yaw", 0):.1f}°)')
            
        except Exception as e:
            self.get_logger().error(f'记录waypoint贡献失败: {e}')

    def _save_fusion_mapping(self, output_dir):
        """保存融合映射信息到文件"""
        try:
            import pickle
            import json
            
            # 保存完整映射信息（pickle格式，供程序读取）
            mapping_file = os.path.join(output_dir, "fusion_mapping.pkl")
            with open(mapping_file, 'wb') as f:
                pickle.dump({
                    'fusion_mapping': self.fusion_mapping,
                    'waypoint_contributions': self.waypoint_contributions,
                    'fusion_params': {
                        'dual_axis_params': getattr(self, '_fusion_info', {}).get('dual_axis_params', {}),
                        'canvas_size': (len(self.fusion_mapping) > 0 and 
                                    max([pos[0] for pos in self.fusion_mapping.keys()]) + 1,
                                    len(self.fusion_mapping) > 0 and 
                                    max([pos[1] for pos in self.fusion_mapping.keys()]) + 1) if self.fusion_mapping else (0, 0)
                    }
                }, f)
            
            # 保存可读的摘要信息（JSON格式）
            summary_file = os.path.join(output_dir, "fusion_mapping_summary.json")
            summary_data = {
                'total_mapped_pixels': len(self.fusion_mapping),
                'waypoint_contributions': {
                    str(wp_idx): {
                        'pixel_count': info['pixel_count'],
                        'coverage_percentage': info['pixel_count'] / len(self.fusion_mapping) * 100 if self.fusion_mapping else 0,
                        'waypoint_index': wp_idx,
                        'source_files': {
                            'color': info['waypoint_data'].get('color_filename', ''),
                            'depth': info['waypoint_data'].get('depth_raw_filename', '')
                        }
                    }
                    for wp_idx, info in self.waypoint_contributions.items()
                }
            }
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
            self.get_logger().info(f'融合映射信息已保存:')
            self.get_logger().info(f'  - 完整映射: {mapping_file}')
            self.get_logger().info(f'  - 摘要信息: {summary_file}')
            self.get_logger().info(f'  - 总映射像素: {len(self.fusion_mapping)}')
            
            # 输出waypoint贡献统计
            for wp_idx, info in self.waypoint_contributions.items():
                percentage = info['pixel_count'] / len(self.fusion_mapping) * 100 if self.fusion_mapping else 0
                self.get_logger().info(f'  - Waypoint {wp_idx}: {percentage:.1f}% ({info["pixel_count"]} 像素)')
            
        except Exception as e:
            self.get_logger().error(f'保存融合映射信息失败: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = SmartStitcherNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()