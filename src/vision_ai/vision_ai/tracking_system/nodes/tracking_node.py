#!/usr/bin/env python3
"""
Improved Simplified Tracking Node - 使用改进的ID匹配器
专注于稳定性检测和详细调试输出
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
import numpy as np
import json
import os
import time
import threading
from typing import Dict, Any, Optional, List
import re
import pandas as pd
# 在 tracking_node.py 中添加可视化类
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches
# 导入追踪系统模块
from ..utils.config import create_tracking_config, TrackingConfig
from ..detection.realtime_detector import RealtimeDetector
from ..detection.id_matcher import ImprovedIDMatcher  # 使用改进版本
from ..core.state_machine import TrackingState, TrackingMode

class ImprovedStabilityDetector:
    """改进的稳定性检测器 - 增加详细调试"""
    
    def __init__(self, logger=None):
        self.logger = logger
        
        # 15帧检测历史
        self.frame_count = 0
        self.max_frames = 15
        self.position_history = []
        self.match_history = []
        self.confidence_history = []
        self.detection_details = []  # 新增：详细检测信息
        
        # 稳定性参数
        self.stable_threshold = 0.6  # 60%稳定率 (进一步降低用于测试)
        self.position_tolerance = 10.0  # 10mm位置容差
        self.confidence_threshold = 0.25  # 进一步降低置信度阈值
        
        # 状态
        self.is_stable = False
        self.stability_report = {}
        # 🆕 位置移动检测参数
        self.movement_threshold = 5.0  # 5mm移动阈值
        self.position_history_3d = []  # 3D世界坐标历史
        self.movement_detected = False
        self.movement_frame = -1
        self._log_info(f"🔧 稳定性检测器配置:")
        self._log_info(f"   稳定性阈值: {self.stable_threshold:.0%}")
        self._log_info(f"   位置容差: {self.position_tolerance}mm")
        self._log_info(f"   置信度阈值: {self.confidence_threshold}")
    
    def add_detection_result(self, detection_result, world_coords, frame_details=None):
        """添加检测结果 - 修复3D坐标处理"""
        try:
            self.frame_count += 1
            
            # 🆕 添加更详细的调试信息
            self._log_info(f"📍 Frame {self.frame_count}:")
            
            # 处理检测结果
            if detection_result:
                match_found = True
                confidence = getattr(detection_result, 'match_confidence', 0.0)
                
                # 🆕 更新3D坐标计算
                if world_coords:
                    self._log_info(f"   世界坐标: [{world_coords[0]:.1f}, {world_coords[1]:.1f}, {world_coords[2]:.1f}]")
                    self.position_history.append(world_coords[:2])  # 只存储XY坐标
                else:
                    # 🆕 如果没有world_coords，尝试从detection_result计算
                    if hasattr(detection_result, 'centroid_3d') and detection_result.centroid_3d:
                        calc_coords = detection_result.centroid_3d
                        self._log_info(f"   使用检测3D坐标: [{calc_coords[0]:.1f}, {calc_coords[1]:.1f}, {calc_coords[2]:.1f}]")
                        self.position_history.append(calc_coords[:2])
                        world_coords = calc_coords
                    else:
                        self._log_info("   ❌ 无3D坐标信息")
                        self.position_history.append(None)
                
                self._log_info(f"   匹配置信度: {confidence:.4f}")
                self._log_info(f"   对象ID: {getattr(detection_result, 'object_id', 'unknown')}")
                
            else:
                match_found = False
                confidence = 0.0
                self.position_history.append(None)
                self._log_info("   ❌ 未找到目标")
            
            # 记录匹配历史
            self.match_history.append(match_found)
            self.confidence_history.append(confidence)
            
            # 🆕 移动检测处理
            if world_coords:
                movement_info = self._check_position_movement(world_coords)
                if movement_info['movement_detected']:
                    self._log_info(f"🚨 检测到位置移动: {movement_info['distance']:.1f}mm")
            
            # 记录详细信息...
            detail_info = {
                'frame_number': self.frame_count,
                'timestamp': time.time(),
                'world_coords': world_coords,
                'detection_found': detection_result is not None,
                'match_confidence': confidence,
                'frame_details': frame_details or {}
            }
            
            self.detection_details.append(detail_info)
            
            # 保持最近15帧
            if len(self.position_history) > self.max_frames:
                self.position_history.pop(0)
                self.match_history.pop(0)
                self.confidence_history.pop(0)
                self.detection_details.pop(0)
            
            # 显示当前统计
            if len(self.match_history) > 0:
                success_count = sum(self.match_history)
                current_stability = success_count / len(self.match_history)
                self._log_info(f"📈 当前稳定性: {current_stability:.1%} ({success_count}/{len(self.match_history)})")
            
        except Exception as e:
            self._log_error(f"❌ 添加检测结果失败: {e}")
            import traceback
            self._log_error(f"详细错误: {traceback.format_exc()}")

    def _check_position_movement(self, current_position):
        """检查位置移动"""
        try:
            movement_info = {
                'movement_detected': False,
                'distance': 0.0,
                'reference_position': None,
                'current_position': current_position
            }
            
            if not self.position_history_3d:
                # 第一帧，设为参考位置
                movement_info['reference_position'] = current_position
                return movement_info
            
            # 获取最近的有效位置作为参考
            valid_positions = [pos for pos in self.position_history_3d if pos is not None]
            
            if not valid_positions:
                return movement_info
            
            # 使用最近5帧的平均位置作为参考
            recent_positions = valid_positions[-5:]
            reference_position = np.mean(recent_positions, axis=0)
            
            # 计算3D欧氏距离
            distance = np.sqrt(np.sum((np.array(current_position) - np.array(reference_position))**2))
            
            movement_info['distance'] = distance
            movement_info['reference_position'] = reference_position.tolist()
            
            # 判断是否超过阈值
            if distance > self.movement_threshold:
                movement_info['movement_detected'] = True
                self._log_info(f"🚨 Position movement detected:")
                self._log_info(f"   Reference: [{reference_position[0]:.1f}, {reference_position[1]:.1f}, {reference_position[2]:.1f}]")
                self._log_info(f"   Current:   [{current_position[0]:.1f}, {current_position[1]:.1f}, {current_position[2]:.1f}]")
                self._log_info(f"   Distance:  {distance:.1f}mm (threshold: {self.movement_threshold}mm)")
            
            return movement_info
            
        except Exception as e:
            self._log_error(f"❌ Position movement check failed: {e}")
            return {
                'movement_detected': False,
                'distance': 0.0,
                'reference_position': None,
                'current_position': current_position
            }
    
    def check_stability(self) -> Dict[str, Any]:
        """检查稳定性 - 增加移动检测结果"""
        try:
            # 原有稳定性检查代码...
            
            if len(self.position_history) < self.max_frames:
                return {
                    'is_stable': False,
                    'reason': f'Insufficient data, current {len(self.position_history)}/{self.max_frames} frames',
                    'progress': len(self.position_history) / self.max_frames,
                    'movement_detected': self.movement_detected,
                    'movement_frame': self.movement_frame
                }
            
            # 匹配稳定性检查
            successful_matches = sum(self.match_history)
            match_stability = successful_matches / len(self.match_history)
            
            # 位置稳定性检查
            valid_positions = [pos for pos in self.position_history if pos is not None]
            position_stability = 0.0
            
            if len(valid_positions) >= 2:
                positions_array = np.array(valid_positions)
                position_variance = np.var(positions_array, axis=0)
                
                # 计算位置稳定性
                reference_pos = valid_positions[0]
                stable_count = sum(1 for pos in valid_positions[1:] 
                                 if self._positions_close(pos, reference_pos))
                position_stability = stable_count / (len(valid_positions) - 1) if len(valid_positions) > 1 else 0
            
            # 🆕 如果检测到移动，调整稳定性判断
            if self.movement_detected:
                self._log_info(f"⚠️ Object movement detected, adjusting stability assessment")
                # 移动后的稳定性要求更高
                adjusted_threshold = self.stable_threshold * 1.2  # 提高20%的要求
            else:
                adjusted_threshold = self.stable_threshold
            
            # 综合稳定性判断
            overall_stability = (match_stability + position_stability) / 2
            is_stable = (match_stability >= adjusted_threshold and 
                        position_stability >= adjusted_threshold)
            
            # 🆕 如果最近检测到移动，可能需要更多观察
            if self.movement_detected and (self.frame_count - self.movement_frame) < 5:
                is_stable = False
                stability_reason = f"Recent movement detected at frame {self.movement_frame}, need more observation"
            else:
                stability_reason = "Normal stability assessment"
            
            # 生成详细报告
            self.stability_report = {
                'is_stable': is_stable,
                'overall_stability': overall_stability,
                'match_stability': match_stability,
                'position_stability': position_stability,
                'successful_matches': successful_matches,
                'total_frames': len(self.match_history),
                'movement_detected': self.movement_detected,
                'movement_frame': self.movement_frame,
                'stability_reason': stability_reason,
                'adjusted_threshold': adjusted_threshold,
                'detection_details': self.detection_details.copy(),
                'position_history_3d': [pos for pos in self.position_history_3d if pos is not None],
                'thresholds': {
                    'stable_threshold': self.stable_threshold,
                    'movement_threshold': self.movement_threshold,
                    'confidence_threshold': self.confidence_threshold,
                    'position_tolerance': self.position_tolerance
                }
            }
            
            # 详细日志输出
            self._log_info(f"\n Enhanced Stability Detection Report:")
            self._log_info(f"   Match stability: {match_stability:.1%} ({successful_matches}/{len(self.match_history)})")
            self._log_info(f"   Position stability: {position_stability:.1%}")
            self._log_info(f"   Overall stability: {overall_stability:.1%}")
            self._log_info(f"   Movement detected: {'Yes' if self.movement_detected else 'No'}")
            if self.movement_detected:
                self._log_info(f"   Movement frame: {self.movement_frame}")
            self._log_info(f"   Adjusted threshold: {adjusted_threshold:.1%}")
            
            result_str = '✅ Stable' if is_stable else '❌ Unstable'
            self._log_info(f"   Final assessment: {result_str}")
            self._log_info(f"   Reason: {stability_reason}")
            
            return self.stability_report
            
        except Exception as e:
            self._log_error(f"❌ Stability detection failed: {e}")
            return {
                'is_stable': False, 
                'reason': f'Detection failed: {e}',
                'movement_detected': self.movement_detected
            }    
    
    def save_stability_report(self, output_dir: str):
        """保存稳定性报告 - 修复序列化问题"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = int(time.time())
            report_file = os.path.join(output_dir, f'stability_report_{timestamp}.json')
            
            # 🆕 清理报告数据
            clean_report = self._clean_stability_data_for_json(self.stability_report)
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(clean_report, f, indent=2, ensure_ascii=False)
            
            self._log_info(f"💾 稳定性报告已保存: {report_file}")
            
        except Exception as e:
            self._log_error(f" 保存稳定性报告失败: {e}")
    
    def _clean_stability_data_for_json(self, data):
        """清理稳定性数据用于JSON序列化 - 增强版"""
        if isinstance(data, dict):
            return {k: self._clean_stability_data_for_json(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._clean_stability_data_for_json(item) for item in data]
        elif isinstance(data, tuple):
            return list(data)
        elif isinstance(data, np.ndarray):
            return data.tolist()
        elif isinstance(data, (np.integer, np.int64, np.int32, np.int16, np.int8)):
            return int(data)
        elif isinstance(data, (np.floating, np.float64, np.float32, np.float16)):
            # 🆕 处理NaN和inf值
            f_val = float(data)
            if np.isnan(f_val) or np.isinf(f_val):
                return 0.0
            return f_val
        elif isinstance(data, (np.bool_, bool)):
            return bool(data)
        elif isinstance(data, np.str_):
            return str(data)
        else:
            return data
    
    def _positions_close(self, pos1, pos2) -> bool:
        """检查两个位置是否接近"""
        if pos1 is None or pos2 is None:
            return False
        
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        distance = np.sqrt(dx*dx + dy*dy)
        
        return distance <= self.position_tolerance
    
    def reset(self):
        """重置检测器 - 包括移动检测状态"""
        self.frame_count = 0
        self.position_history.clear()
        self.match_history.clear()
        self.confidence_history.clear()
        self.detection_details.clear()
        # 🆕 重置移动检测状态
        self.position_history_3d.clear()
        self.movement_detected = False
        self.movement_frame = -1
        self.is_stable = False
        self.stability_report = {}
        self._log_info("🔄 Enhanced stability detector reset with movement detection")
    
    def _log_info(self, message: str):
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[IMPROVED_STABILITY] {message}")
    
    def _log_debug(self, message: str):
        if self.logger:
            self.logger.debug(message)
        else:
            print(f"[IMPROVED_STABILITY] DEBUG: {message}")
    
    def _log_error(self, message: str):
        if self.logger:
            self.logger.error(message)
        else:
            print(f"[IMPROVED_STABILITY] ERROR: {message}")

class ImprovedSimplifiedTrackingNode(Node):
    """改进的简化版追踪节点"""
    
    def __init__(self):
        super().__init__('improved_simplified_tracking_node')
        
        # 配置和组件
        self.config = create_tracking_config()
        
        # 显示详细配置
        self._log_current_config()
        
        # 初始化组件
        self.realtime_detector = RealtimeDetector(self.config, self.get_logger())
        self.id_matcher = ImprovedIDMatcher(self.config, self.get_logger())
        self.stability_detector = ImprovedStabilityDetector(self.get_logger())
        
        # 目标信息
        self.scan_directory = None
        self.target_object_id = None
        self.target_class_id = None
        
        # 调试输出目录
        self.debug_output_dir = None
        
        # 当前数据
        self.current_color_image = None
        self.current_depth_image = None
        self.data_lock = threading.Lock()
        
        # 检测控制
        self.detection_active = False
        self.detection_timer = None
        
        # 状态
        self.current_state = "IDLE"
        
        # ROS2接口
        self._setup_ros_interface()
        
        self.get_logger().info(' 改进版简化追踪节点启动完成')
    
    def _log_current_config(self):
        """显示当前配置"""
        feature_config = self.config.feature_config
        self.get_logger().info('🔧 当前特征匹配配置:')
        self.get_logger().info(f'   匹配阈值: {feature_config.get("match_threshold", "未设置")}')
        self.get_logger().info(f'   权重配置:')
        weights = feature_config.get("weights", {})
        for key, value in weights.items():
            self.get_logger().info(f'     - {key}: {value}')
        self.get_logger().info(f'   颜色直方图bins: {feature_config.get("color", {}).get("histogram_bins", "未设置")}')
        self.get_logger().info(f'   Hu矩数量: {feature_config.get("shape", {}).get("hu_moments_count", "未设置")}')
    
    def _setup_ros_interface(self):
        """设置ROS2接口"""
        # 订阅者
        self.detection_complete_sub = self.create_subscription(
            String, '/detection_complete', 
            self.detection_complete_callback, 10
        )
        
        self.color_image_sub = self.create_subscription(
            Image, '/camera/color/image_raw',
            self.color_image_callback, 10
        )
        
        self.depth_image_sub = self.create_subscription(
            Image, '/camera/depth/image_raw',
            self.depth_image_callback, 10
        )
        
        # 发布者
        self.status_pub = self.create_publisher(String, '/tracking/status', 10)
        self.stability_pub = self.create_publisher(String, '/tracking/stability', 10)
        self.debug_pub = self.create_publisher(String, '/tracking/debug', 10)  # 新增调试发布者
        
        # 定时器
        self.status_timer = self.create_timer(2.0, self.publish_status)
    
    def detection_complete_callback(self, msg):
        """检测完成回调 - 改进版本"""
        try:
            data = json.loads(msg.data)
            scan_directory = data.get('scan_directory', '')
            
            if scan_directory and not os.path.isabs(scan_directory):
                workspace_root = os.path.expanduser("~/ros2_ws")
                scan_directory = os.path.join(workspace_root, scan_directory)
            
            self.scan_directory = scan_directory
            
            if not self.scan_directory:
                self.get_logger().error(' 检测完成信号中没有扫描目录')
                return
            
            # 设置调试输出目录
            self.debug_output_dir = os.path.join(self.scan_directory, "tracking_debug")
            os.makedirs(self.debug_output_dir, exist_ok=True)
            
            # 为ID匹配器设置调试输出
            self.id_matcher.set_debug_output_dir(self.debug_output_dir)
            
            self.get_logger().info(f'📁 接收到检测完成信号: {self.scan_directory}')
            self.get_logger().info(f'📁 调试输出目录: {self.debug_output_dir}')
            
            # 加载追踪目标
            if self._load_tracking_target():
                self.get_logger().info(f' 追踪目标加载成功: {self.target_object_id}')
                self.start_stability_detection()
            else:
                self.get_logger().error(' 追踪目标加载失败')
                
        except Exception as e:
            self.get_logger().error(f' 处理检测完成信号失败: {e}')
    
    def _load_tracking_target(self) -> bool:
        """加载追踪目标 - 改进版本"""
        try:
            # 加载参考特征数据库
            if not self.id_matcher.load_reference_features(self.scan_directory):
                return False
            
            # 显示ID匹配器详细状态
            self.id_matcher.print_detailed_status()
            
            # 读取tracking_selection.txt
            selection_file = os.path.join(self.scan_directory, 'detection_results', 'tracking_selection.txt')
            
            if not os.path.exists(selection_file):
                self.get_logger().error(f' 未找到tracking_selection.txt: {selection_file}')
                return False
            
            with open(selection_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.get_logger().info(f'📄 tracking_selection.txt内容:\n{content}')
            
            # 解析选择的目标ID
            match = re.search(r'\(ID:\s*([^)]+)\)', content)
            if not match:
                self.get_logger().error(' 无法从tracking_selection.txt解析目标ID')
                return False
            
            self.target_object_id = match.group(1).strip()
            
            # 从参考数据库获取class_id
            if self.target_object_id in self.id_matcher.reference_features_db:
                ref_data = self.id_matcher.reference_features_db[self.target_object_id]
                self.target_class_id = ref_data['class_id']
                
                self.get_logger().info(f' 选择追踪目标: {self.target_object_id} (class_id: {self.target_class_id})')
                
                # 显示目标特征详情
                target_features = ref_data.get('features', {})
                self.get_logger().info(f' 目标特征详情:')
                self.get_logger().info(f'   特征类型: {list(target_features.keys())}')
                
                # 显示颜色特征
                color_features = target_features.get('color', {})
                if 'histogram' in color_features:
                    hist_len = len(color_features['histogram'])
                    self.get_logger().info(f'   颜色直方图: {hist_len} bins')
                
                # 显示形状特征
                shape_features = target_features.get('shape', {})
                if 'hu_moments' in shape_features:
                    hu_len = len(shape_features['hu_moments'])
                    self.get_logger().info(f'   Hu矩: {hu_len} 个')
                    hu_values = shape_features['hu_moments'][:3]  # 显示前3个
                    self.get_logger().info(f'   Hu矩示例: {[f"{h:.4f}" for h in hu_values]}...')
                
                return True
            else:
                self.get_logger().error(f' 目标ID {self.target_object_id} 不在参考数据库中')
                available_ids = list(self.id_matcher.reference_features_db.keys())
                self.get_logger().error(f'   可用ID: {available_ids}')
                return False
                
        except Exception as e:
            self.get_logger().error(f' 加载追踪目标失败: {e}')
            import traceback
            self.get_logger().error(f'详细错误: {traceback.format_exc()}')
            return False
    
    def start_stability_detection(self):
        """开始稳定性检测 - 改进版本"""
        try:
            if self.detection_timer is None:
                self.current_state = "DETECTING"
                self.stability_detector.reset()
                
                # 启动检测定时器 (降低到5Hz避免过于频繁)
                self.detection_timer = self.create_timer(0.2, self.detection_timer_callback)
                
                self.get_logger().info('🔄 开始15帧稳定性检测...')
                self.get_logger().info(f'   目标: {self.target_object_id}')
                self.get_logger().info(f'   目标类别: {self.target_class_id}')
                self.get_logger().info(f'   匹配阈值: {self.id_matcher.match_threshold}')
                self.get_logger().info(f'   稳定性阈值: {self.stability_detector.stable_threshold:.0%}')
                
        except Exception as e:
            self.get_logger().error(f' 启动稳定性检测失败: {e}')
    
    def stop_stability_detection(self):
        """停止稳定性检测 - 增强版本"""
        if self.detection_timer:
            self.detection_timer.cancel()
            self.detection_timer = None
            self.current_state = "IDLE"
            self.get_logger().info('⏹️ 稳定性检测已停止')
            
            # 保存调试数据
            if self.debug_output_dir:
                self.id_matcher.save_all_debug_history()
                self.stability_detector.save_stability_report(self.debug_output_dir)
        else:
            self.get_logger().debug('⏹️ 检测定时器已经是停止状态')
    
    def detection_timer_callback(self):
        """检测定时器回调 - 改进版本"""
        try:
            if self.current_state != "DETECTING":
                return
            
            with self.data_lock:
                if self.current_color_image is None:
                    return
                
                self._process_improved_stability_detection()
                
        except Exception as e:
            self.get_logger().error(f' 检测定时器回调失败: {e}')
    
    def _process_improved_stability_detection(self):
        """处理改进的稳定性检测"""
        try:
            current_frame = self.stability_detector.frame_count + 1
            self.get_logger().info(f"🔍 处理第{current_frame}帧，目标15帧")
            # 运行检测
            detection_results = self.realtime_detector.detect_and_segment(
                self.current_color_image, self.current_depth_image
            )
            world_coords = None
                    # 🆕 添加图像格式调试
            if self.current_color_image is not None:
                self.get_logger().debug(f"当前颜色图像: shape={self.current_color_image.shape}, "
                                    f"dtype={self.current_color_image.dtype}, "
                                    f"range=[{self.current_color_image.min()}, {self.current_color_image.max()}]")
                
                # 检查颜色通道分布
                if len(self.current_color_image.shape) == 3:
                    r_mean = np.mean(self.current_color_image[:, :, 0])
                    g_mean = np.mean(self.current_color_image[:, :, 1])
                    b_mean = np.mean(self.current_color_image[:, :, 2])
                    self.get_logger().debug(f"RGB平均值: R={r_mean:.1f}, G={g_mean:.1f}, B={b_mean:.1f}")

                # 详细记录所有检测结果
            frame_details = {
                'total_detections': len(detection_results),
                'detected_classes': {}
            }
            
            if detection_results:
                for result in detection_results:
                    class_name = result.class_name
                    class_id = result.class_id
                    if class_name not in frame_details['detected_classes']:
                        frame_details['detected_classes'][class_name] = {
                            'class_id': class_id,
                            'count': 0
                        }
                    frame_details['detected_classes'][class_name]['count'] += 1
                
                detected_info = [(r.class_name, r.class_id) for r in detection_results]
                self.get_logger().info(f" 第{self.stability_detector.frame_count + 1}帧检测到对象: {detected_info}")
            else:
                self.get_logger().info(f" 第{self.stability_detector.frame_count + 1}帧未检测到任何对象")
            
            # 使用改进的ID匹配器进行目标专用匹配
            target_detection = self.id_matcher.match_target_only(
                detection_results, 
                self.target_class_id,
                self.target_object_id
            )
            
            # 🆕 获取世界坐标 - 确保变量总是被赋值
            if target_detection:
                # 从参考数据库获取世界坐标
                if self.target_object_id in self.id_matcher.reference_features_db:
                    ref_data = self.id_matcher.reference_features_db[self.target_object_id]
                    world_coords = ref_data['features'].get('spatial', {}).get('world_coordinates', None)
                
                # 🆕 如果参考数据库没有坐标，尝试从检测结果计算
                if world_coords is None and hasattr(target_detection, 'centroid_3d'):
                    world_coords = target_detection.centroid_3d
                    self.get_logger().debug(f"使用检测计算的3D坐标: {world_coords}")
                
                self.get_logger().info(f" 第{self.stability_detector.frame_count + 1}帧找到目标: {self.target_object_id}")
                self.get_logger().info(f"   置信度: {target_detection.match_confidence:.4f}")
                self.get_logger().info(f"   匹配方法: {target_detection.match_method}")
                if world_coords:
                    self.get_logger().info(f"   世界坐标: [{world_coords[0]:.1f}, {world_coords[1]:.1f}, {world_coords[2]:.1f}]")
                else:
                    self.get_logger().warn("   ⚠️ 无世界坐标信息")
            else:
                # 🆕 确保world_coords在未找到目标时也被赋值
                world_coords = None
                self.get_logger().info(f" 第{self.stability_detector.frame_count + 1}帧未找到目标: {self.target_object_id}")
                
                # 分析为什么找不到目标
                target_class_detections = [d for d in detection_results if d.class_id == self.target_class_id]
                if not target_class_detections:
                    self.get_logger().info(f"   原因: 未检测到目标类别 {self.target_class_id} 的对象")
                else:
                    self.get_logger().info(f"   检测到 {len(target_class_detections)} 个目标类别对象，但无法匹配")
            
            # 发布调试信息
            self._publish_debug_info(frame_details, target_detection)
            
            # 🆕 现在world_coords总是被定义了
            # 添加到稳定性检测器
            self.stability_detector.add_detection_result(
                target_detection, world_coords, frame_details
            )
            
            # 检查是否完成15帧检测
            frames_collected = len(self.stability_detector.position_history)
            self.get_logger().info(f"📊 已收集帧数: {frames_collected}/15")
            
            if frames_collected >= 15:
                self.get_logger().info("🎯 15帧检测完成，开始稳定性分析...")
                self._handle_stability_check_complete()
            else:
                self.get_logger().info(f"⏳ 稳定性检测进度: {frames_collected}/15 帧")
            
        except Exception as e:
            self.get_logger().error(f' 改进稳定性检测处理失败: {e}')
            import traceback
            self.get_logger().error(f'详细错误: {traceback.format_exc()}')
    
    def _publish_debug_info(self, frame_details, target_detection):
        """发布调试信息"""
        try:
            debug_data = {
                'timestamp': time.time(),
                'frame_number': self.stability_detector.frame_count + 1,
                'frame_details': frame_details,
                'target_detection': {
                    'found': target_detection is not None,
                    'object_id': getattr(target_detection, 'object_id', None),
                    'match_confidence': getattr(target_detection, 'match_confidence', 0.0),
                    'match_method': getattr(target_detection, 'match_method', 'none')
                } if target_detection else None,
                'id_matcher_stats': self.id_matcher.get_match_statistics()
            }
            
            debug_msg = String()
            debug_msg.data = json.dumps(debug_data, indent=2)
            self.debug_pub.publish(debug_msg)
            
        except Exception as e:
            self.get_logger().error(f' 发布调试信息失败: {e}')
    
    def _handle_stability_check_complete(self):
        """处理稳定性检测完成 - 确保停止检测"""
        try:
            self.get_logger().info("🎯 开始稳定性分析...")
            
            # 🆕 立即停止检测定时器，防止继续处理
            if self.detection_timer:
                self.detection_timer.cancel()
                self.detection_timer = None
                self.get_logger().info("⏹️ 检测定时器已停止")
            
            # 执行稳定性检查
            stability_result = self.stability_detector.check_stability()
            
            # 发布稳定性结果
            self._publish_stability_result(stability_result)
            
            # 显示ID匹配器最终统计
            self.id_matcher.print_detailed_status()
            
            if stability_result['is_stable']:
                self.current_state = "STABLE_DETECTED"
                self.get_logger().info(' 目标稳定，询问用户是否进入抓取模式...')
                self._show_detailed_grasp_dialog(stability_result)
            else:
                self.current_state = "IDLE"
                reason = stability_result.get('reason', '未知原因')
                self.get_logger().warn(f'⚠️ 目标不稳定: {reason}')
                
                # 显示改进建议
                self._show_stability_improvement_suggestions(stability_result)
                
                self.get_logger().info('🔄 10秒后重新开始检测...')
                threading.Timer(10.0, self.start_stability_detection).start()
            
        except Exception as e:
            self.get_logger().error(f' 处理稳定性检测完成失败: {e}')
            import traceback
            self.get_logger().error(f'详细错误: {traceback.format_exc()}')
    
    def _show_stability_improvement_suggestions(self, stability_result):
        """显示稳定性改进建议"""
        try:
            print("\n" + "="*60)
            print(" 稳定性分析报告")
            print("="*60)
            
            match_stability = stability_result.get('match_stability', 0)
            position_stability = stability_result.get('position_stability', 0)
            confidence_analysis = stability_result.get('confidence_analysis', {})
            
            print(f"匹配稳定性: {match_stability:.1%}")
            print(f"位置稳定性: {position_stability:.1%}")
            print(f"平均置信度: {confidence_analysis.get('mean_confidence', 0):.4f}")
            print(f"最大置信度: {confidence_analysis.get('max_confidence', 0):.4f}")
            print(f"最小置信度: {confidence_analysis.get('min_confidence', 0):.4f}")
            
            print("\n💡 改进建议:")
            
            if match_stability < 0.6:
                print("- 匹配稳定性较低，可能需要:")
                print("  • 降低匹配阈值")
                print("  • 调整特征权重")
                print("  • 检查光照条件")
                
            if confidence_analysis.get('max_confidence', 0) < 0.3:
                print("- 最大置信度过低，可能需要:")
                print("  • 重新采集参考特征")
                print("  • 检查目标对象是否在视野中")
                
            if position_stability < 0.6:
                print("- 位置稳定性较低，可能需要:")
                print("  • 增加位置容差")
                print("  • 检查相机稳定性")
                
            print("="*60)
            
        except Exception as e:
            self.get_logger().error(f' 显示改进建议失败: {e}')
    
    def _show_detailed_grasp_dialog(self, stability_result):
        """显示详细的抓取对话框"""
        try:
            self.current_state = "WAITING_INPUT"
            
            print("\n" + "="*60)
            print(" 目标稳定性检测完成!")
            print("="*60)
            print(f"目标对象: {self.target_object_id}")
            
            # 显示详细统计
            match_stats = self.id_matcher.get_match_statistics()
            print(f"\n 匹配统计:")
            print(f"  成功率: {match_stats['success_rate']:.1%}")
            print(f"  平均最佳得分: {match_stats['average_best_score']:.4f}")
            print(f"  匹配阈值: {match_stats['match_threshold']}")
            
            print(f"\n 稳定性分析:")
            print(f"  匹配稳定性: {stability_result['match_stability']:.1%}")
            print(f"  位置稳定性: {stability_result['position_stability']:.1%}")
            print(f"  综合稳定性: {stability_result['overall_stability']:.1%}")
            
            confidence_analysis = stability_result.get('confidence_analysis', {})
            print(f"  平均置信度: {confidence_analysis.get('mean_confidence', 0):.4f}")
            print(f"  置信度范围: {confidence_analysis.get('min_confidence', 0):.4f} - {confidence_analysis.get('max_confidence', 0):.4f}")
            
            print(f"\n📁 调试文件已保存到: {self.debug_output_dir}")
            print("="*60)
            
            # 在新线程中处理用户输入
            threading.Thread(target=self._handle_user_input, daemon=True).start()
            
        except Exception as e:
            self.get_logger().error(f' 显示详细抓取对话框失败: {e}')
    
    def _handle_user_input(self):
        """处理用户输入 - 改进版本"""
        try:
            while self.current_state == "WAITING_INPUT":
                user_input = input("\n是否进入抓取模式? (y/n/r-重新检测/d-查看调试): ").strip().lower()
                
                if user_input in ['y', 'yes']:
                    self.get_logger().info(' 用户确认进入抓取模式')
                    self.current_state = "GRASP_READY"
                    self._publish_grasp_ready()
                    break
                    
                elif user_input in ['n', 'no']:
                    self.get_logger().info(' 用户取消抓取，重新开始检测')
                    self.current_state = "IDLE"
                    threading.Timer(2.0, self.start_stability_detection).start()
                    break
                    
                elif user_input in ['r', 'restart']:
                    self.get_logger().info('🔄 用户要求重新检测')
                    self.current_state = "IDLE"
                    threading.Timer(1.0, self.start_stability_detection).start()
                    break
                    
                elif user_input in ['d', 'debug']:
                    self._show_debug_summary()
                    
                else:
                    print("请输入 y(进入抓取)/n(取消)/r(重新检测)/d(查看调试)")
                    
        except Exception as e:
            self.get_logger().error(f' 处理用户输入失败: {e}')
    
    def _show_debug_summary(self):
        """显示调试摘要"""
        try:
            print("\n" + "="*60)
            print(" 调试信息摘要")
            print("="*60)
            
            # ID匹配器统计
            match_stats = self.id_matcher.get_match_statistics()
            print(f" ID匹配器统计:")
            print(f"  匹配尝试: {match_stats['total_attempts']}")
            print(f"  成功匹配: {match_stats['successful_matches']}")
            print(f"  成功率: {match_stats['success_rate']:.1%}")
            print(f"  平均得分: {match_stats['average_best_score']:.4f}")
            
            # 最近几次匹配详情
            if len(self.id_matcher.match_debug_history) > 0:
                print(f"\n 最近5次匹配详情:")
                recent_matches = self.id_matcher.match_debug_history[-5:]
                for i, match in enumerate(recent_matches, 1):
                    status = "" if match['best_match_found'] else ""
                    print(f"  {i}. {status} 得分: {match['best_score']:.4f}, 候选: {match['candidate_count']}")
            
            # 稳定性详情
            if hasattr(self.stability_detector, 'stability_report') and self.stability_detector.stability_report:
                report = self.stability_detector.stability_report
                failed_frames = report.get('failed_frames', [])
                if failed_frames:
                    print(f"\n 失败帧分析:")
                    for fail in failed_frames[-5:]:
                        print(f"  帧{fail['frame']}: {fail['reason']}")
            
            print(f"\n📁 详细调试文件位置: {self.debug_output_dir}")
            print("="*60)
            
        except Exception as e:
            self.get_logger().error(f' 显示调试摘要失败: {e}')
    
    def _publish_grasp_ready(self):
        """发布抓取就绪信号 - 改进版本"""
        try:
            if self.target_object_id in self.id_matcher.reference_features_db:
                ref_data = self.id_matcher.reference_features_db[self.target_object_id]
                spatial_data = ref_data['features'].get('spatial', {})
                
                grasp_data = {
                    'object_id': self.target_object_id,
                    'class_id': self.target_class_id,
                    'world_coordinates': spatial_data.get('world_coordinates', [0, 0, 0]),
                    'tracking_height': spatial_data.get('world_coordinates', [0, 0, 200])[2] + 200,
                    'gripper_width': spatial_data.get('gripper_width_info', {}).get('recommended_gripper_width', 300),
                    'yaw_angle': 0.0,
                    'stability_report': self.stability_detector.stability_report,
                    'match_statistics': self.id_matcher.get_match_statistics(),
                    'debug_output_dir': self.debug_output_dir
                }
                
                grasp_msg = String()
                grasp_msg.data = json.dumps(grasp_data, indent=2)
                
                grasp_ready_pub = self.create_publisher(String, '/tracking/grasp_ready', 10)
                grasp_ready_pub.publish(grasp_msg)
                
                self.get_logger().info('📡 已发布抓取就绪信号')
                
        except Exception as e:
            self.get_logger().error(f' 发布抓取就绪信号失败: {e}')
    
    def _publish_stability_result(self, stability_result):
        """发布稳定性结果 - 修复序列化问题"""
        try:
            # 🆕 清理数据确保可序列化
            clean_result = self._clean_for_json_serialization(stability_result)
            
            stability_msg = String()
            stability_msg.data = json.dumps(clean_result, indent=2)
            self.stability_pub.publish(stability_msg)
            
        except Exception as e:
            self._log_error(f"❌ Failed to publish stability result: {e}")
    
    def _clean_for_json_serialization(self, data):
        """递归清理数据使其可JSON序列化 - 增强版"""
        if isinstance(data, dict):
            return {k: self._clean_for_json_serialization(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._clean_for_json_serialization(item) for item in data]
        elif isinstance(data, tuple):
            return list(data)
        elif isinstance(data, np.ndarray):
            return data.tolist()
        elif isinstance(data, (np.integer, np.int64, np.int32, np.int16, np.int8)):
            return int(data)
        elif isinstance(data, (np.floating, np.float64, np.float32, np.float16)):
            return float(data)
        elif isinstance(data, (np.bool_, bool)):
            return bool(data)
        elif isinstance(data, np.str_):
            return str(data)
        elif pd and isinstance(data, (pd.Timestamp, pd.Timedelta)):
            return str(data)
        else:
            return data
    
    def color_image_callback(self, msg):
        """彩色图像回调 - 修复版本"""
        try:
            with self.data_lock:
                # 使用与scan_executor_node相同的方法
                if msg.step == msg.width * 3:  # 正确的RGB步长
                    image_array = np.frombuffer(msg.data, dtype=np.uint8)
                    self.current_color_image = image_array.reshape((msg.height, msg.width, 3))
                else:
                    # 如果步长不对，可能需要重新解释数据
                    self.get_logger().warn(f'意外的color image步长: {msg.step}, 期望: {msg.width * 3}')
                    # 尝试直接重建
                    image_array = np.frombuffer(msg.data, dtype=np.uint8)
                    try:
                        self.current_color_image = image_array.reshape((msg.height, msg.width, 3))
                    except ValueError as e:
                        self.get_logger().error(f'Color image reshape失败: {e}')
                        return
                        
        except Exception as e:
            self.get_logger().error(f' 彩色图像回调失败: {e}')

    def depth_image_callback(self, msg):
        """深度图像回调 - 修复版本"""
        try:
            with self.data_lock:
                # 添加调试信息
                self.get_logger().debug(f'Depth message: encoding={msg.encoding}, step={msg.step}, expected={msg.width * 2}')
                
                if msg.step == msg.width * 2:  # 正确的16位步长
                    image_array = np.frombuffer(msg.data, dtype=np.uint16)
                    self.current_depth_image = image_array.reshape((msg.height, msg.width))
                else:
                    # 与scan_executor_node相同的修复方法
                    self.get_logger().warn(f'修复深度图像步长问题: {msg.step} vs {msg.width * 2}')
                    
                    # 直接从原始字节数据重建16位深度图像
                    raw_data = np.frombuffer(msg.data, dtype=np.uint8)
                    # 将连续的两个uint8重新组合为uint16
                    depth_raw = raw_data.view(np.uint16).reshape((msg.height, msg.width))
                    self.current_depth_image = depth_raw
                    
                    # 验证深度数据
                    if self.current_depth_image.max() < 1000:
                        self.get_logger().warn(f'深度值可能过小: max={self.current_depth_image.max()}')
                        
        except Exception as e:
            self.get_logger().error(f' 深度图像回调失败: {e}')
            import traceback
            self.get_logger().error(f'详细错误: {traceback.format_exc()}')
    
    def publish_status(self):
        """发布系统状态"""
        try:
            status_data = {
                'node': 'improved_simplified_tracking',
                'state': self.current_state,
                'target_object_id': self.target_object_id,
                'scan_directory': self.scan_directory,
                'debug_output_dir': self.debug_output_dir,
                'detection_active': self.detection_timer is not None,
                'frame_count': self.stability_detector.frame_count,
                'frames_collected': len(self.stability_detector.position_history),
                'match_statistics': self.id_matcher.get_match_statistics() if hasattr(self, 'id_matcher') else {},
                'timestamp': time.time()
            }
            
            status_msg = String()
            status_msg.data = json.dumps(status_data)
            self.status_pub.publish(status_msg)
            
        except Exception as e:
            self.get_logger().error(f' 发布状态失败: {e}')
    
    def destroy_node(self):
        """节点销毁清理"""
        try:
            self.stop_stability_detection()
            self.get_logger().info('🔄 改进版简化追踪节点已清理')
            
        except Exception as e:
            self.get_logger().error(f' 节点清理失败: {e}')
        finally:
            super().destroy_node()


def main(args=None):
    """主函数"""
    rclpy.init(args=args)
    
    try:
        tracking_node = ImprovedSimplifiedTrackingNode()
        
        tracking_node.get_logger().info(' 改进版简化追踪节点启动完成，等待检测完成信号...')
        rclpy.spin(tracking_node)
        
    except KeyboardInterrupt:
        print('\n🔄 用户中断，正在退出...')
    except Exception as e:
        print(f' 追踪节点错误: {e}')
    finally:
        if 'tracking_node' in locals():
            tracking_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()