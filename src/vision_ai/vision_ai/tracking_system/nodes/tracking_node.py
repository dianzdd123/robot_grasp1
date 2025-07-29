#!/usr/bin/env python3
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
from typing import Dict, Any, Optional, List, Tuple
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as patches

# 导入模块
from ..utils.config import create_tracking_config, TrackingConfig
from ..detection.realtime_detector import RealtimeDetector
from ..detection.multi_object_tracker import MultiObjectTracker, Track, DetectionResult


class EnhancedStabilityDetector:
    """增强稳定性检测器 - 适配MultiObjectTracker"""
    
    def __init__(self, logger=None):
        self.logger = logger
        
        # 15帧检测历史
        self.frame_count = 0
        self.max_frames = 15
        self.tracking_history = []  # 存储Track对象历史
        self.detection_details = []
        
        # 稳定性参数
        self.stable_threshold = 0.6  # 60%稳定率
        self.position_tolerance = 10.0  # 10mm位置容差
        self.confidence_threshold = 0.25
        
        # 移动检测参数
        self.movement_threshold = 5.0  # 5mm移动阈值
        self.position_history_3d = []
        self.movement_detected = False
        self.movement_frame = -1
        
        # 状态
        self.is_stable = False
        self.stability_report = {}
        
        self._log_info(f"增强稳定性检测器配置:")
        self._log_info(f"   稳定性阈值: {self.stable_threshold:.0%}")
        self._log_info(f"   位置容差: {self.position_tolerance}mm")
        self._log_info(f"   置信度阈值: {self.confidence_threshold}")
    
    def add_tracking_result(self, target_track: Optional[Track], all_tracks: List[Track], frame_details=None):
        """添加追踪结果"""
        try:
            self.frame_count += 1
            self._log_info(f"Frame {self.frame_count}:")
            
            # 处理追踪结果
            if target_track:
                self._log_info(f"   找到目标轨迹: ID {target_track.track_id}")
                self._log_info(f"   类别: {target_track.class_name}")
                self._log_info(f"   置信度: {target_track.confidence:.4f}")
                self._log_info(f"   丢失帧数: {target_track.lost_frames}")
                self._log_info(f"   轨迹年龄: {target_track.age}")
                
                # 获取3D坐标
                world_coords = target_track.world_coordinates
                if world_coords and len(world_coords) >= 3:
                    self._log_info(f"   世界坐标: [{world_coords[0]:.1f}, {world_coords[1]:.1f}, {world_coords[2]:.1f}]")
                    
                    # 检查位置移动
                    movement_info = self._check_position_movement(world_coords)
                    if movement_info['movement_detected']:
                        self._log_info(f"检测到位置移动: {movement_info['distance']:.1f}mm")
                        self.movement_detected = True
                        self.movement_frame = self.frame_count
                else:
                    self._log_info("   无3D坐标信息")
                    world_coords = None
                
                match_found = True
                track_confidence = target_track.confidence
                
            else:
                match_found = False
                track_confidence = 0.0
                world_coords = None
                self._log_info("   未找到目标轨迹")
            
            # 记录详细信息
            detail_info = {
                'frame_number': self.frame_count,
                'timestamp': time.time(),
                'target_found': target_track is not None,
                'track_id': target_track.track_id if target_track else None,
                'track_confidence': track_confidence,
                'lost_frames': target_track.lost_frames if target_track else 0,
                'world_coords': world_coords,
                'total_tracks': len(all_tracks),
                'frame_details': frame_details or {}
            }
            
            self.tracking_history.append(target_track)
            self.detection_details.append(detail_info)
            
            # 更新3D位置历史
            if world_coords:
                self.position_history_3d.append(world_coords)
            else:
                self.position_history_3d.append(None)
            
            # 保持最近15帧
            if len(self.tracking_history) > self.max_frames:
                self.tracking_history.pop(0)
                self.detection_details.pop(0)
                self.position_history_3d.pop(0)
            
            # 显示当前统计
            if len(self.tracking_history) > 0:
                success_count = sum(1 for track in self.tracking_history if track is not None)
                current_stability = success_count / len(self.tracking_history)
                self._log_info(f"当前稳定性: {current_stability:.1%} ({success_count}/{len(self.tracking_history)})")
            
        except Exception as e:
            self._log_error(f"添加追踪结果失败: {e}")
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
            
            # 获取最近的有效位置作为参考
            valid_positions = [pos for pos in self.position_history_3d if pos is not None]
            
            if not valid_positions:
                movement_info['reference_position'] = current_position
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
                self._log_info(f"Position movement detected:")
                self._log_info(f"   Reference: [{reference_position[0]:.1f}, {reference_position[1]:.1f}, {reference_position[2]:.1f}]")
                self._log_info(f"   Current:   [{current_position[0]:.1f}, {current_position[1]:.1f}, {current_position[2]:.1f}]")
                self._log_info(f"   Distance:  {distance:.1f}mm (threshold: {self.movement_threshold}mm)")
            
            return movement_info
            
        except Exception as e:
            self._log_error(f"Position movement check failed: {e}")
            return {
                'movement_detected': False,
                'distance': 0.0,
                'reference_position': None,
                'current_position': current_position
            }
    
    def check_stability(self) -> Dict[str, Any]:
        """检查稳定性"""
        try:
            if len(self.tracking_history) < self.max_frames:
                return {
                    'is_stable': False,
                    'reason': f'Insufficient data, current {len(self.tracking_history)}/{self.max_frames} frames',
                    'progress': len(self.tracking_history) / self.max_frames,
                    'movement_detected': self.movement_detected,
                    'movement_frame': self.movement_frame
                }
            
            # 追踪稳定性检查 - 基于是否找到目标轨迹
            successful_tracks = sum(1 for track in self.tracking_history if track is not None)
            track_stability = successful_tracks / len(self.tracking_history)
            
            # 轨迹质量检查 - 基于丢失帧数
            quality_tracks = 0
            total_valid_tracks = 0
            
            for track in self.tracking_history:
                if track is not None:
                    total_valid_tracks += 1
                    # 如果丢失帧数较少且置信度足够，认为是高质量轨迹
                    if track.lost_frames <= 2 and track.confidence >= self.confidence_threshold:
                        quality_tracks += 1
            
            track_quality = quality_tracks / total_valid_tracks if total_valid_tracks > 0 else 0
            
            # 位置稳定性检查
            valid_positions = [pos for pos in self.position_history_3d if pos is not None]
            position_stability = 0.0
            
            if len(valid_positions) >= 2:
                # 计算位置方差
                positions_array = np.array(valid_positions)
                position_variance = np.var(positions_array, axis=0)
                
                # 基于相邻位置的距离检查稳定性
                stable_count = 0
                for i in range(1, len(valid_positions)):
                    distance = np.sqrt(np.sum((np.array(valid_positions[i]) - np.array(valid_positions[i-1]))**2))
                    if distance <= self.position_tolerance:
                        stable_count += 1
                
                position_stability = stable_count / (len(valid_positions) - 1) if len(valid_positions) > 1 else 0
            
            # 如果检测到移动，调整稳定性判断
            if self.movement_detected:
                self._log_info(f"Object movement detected, adjusting stability assessment")
                adjusted_threshold = self.stable_threshold * 1.2  # 提高20%的要求
            else:
                adjusted_threshold = self.stable_threshold
            
            # 综合稳定性判断
            overall_stability = (track_stability + track_quality + position_stability) / 3
            is_stable = (track_stability >= adjusted_threshold and 
                        track_quality >= adjusted_threshold and
                        position_stability >= adjusted_threshold)
            
            # 如果最近检测到移动，可能需要更多观察
            if self.movement_detected and (self.frame_count - self.movement_frame) < 5:
                is_stable = False
                stability_reason = f"Recent movement detected at frame {self.movement_frame}, need more observation"
            else:
                stability_reason = "Normal stability assessment"
            
            # 生成详细报告
            self.stability_report = {
                'is_stable': is_stable,
                'overall_stability': overall_stability,
                'track_stability': track_stability,
                'track_quality': track_quality,
                'position_stability': position_stability,
                'successful_tracks': successful_tracks,
                'total_frames': len(self.tracking_history),
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
            self._log_info(f"\nEnhanced Stability Detection Report:")
            self._log_info(f"   Track stability: {track_stability:.1%} ({successful_tracks}/{len(self.tracking_history)})")
            self._log_info(f"   Track quality: {track_quality:.1%}")
            self._log_info(f"   Position stability: {position_stability:.1%}")
            self._log_info(f"   Overall stability: {overall_stability:.1%}")
            self._log_info(f"   Movement detected: {'Yes' if self.movement_detected else 'No'}")
            if self.movement_detected:
                self._log_info(f"   Movement frame: {self.movement_frame}")
            self._log_info(f"   Adjusted threshold: {adjusted_threshold:.1%}")
            
            result_str = 'Stable' if is_stable else 'Unstable'
            self._log_info(f"   Final assessment: {result_str}")
            self._log_info(f"   Reason: {stability_reason}")
            
            return self.stability_report
            
        except Exception as e:
            self._log_error(f"Stability detection failed: {e}")
            return {
                'is_stable': False, 
                'reason': f'Detection failed: {e}',
                'movement_detected': self.movement_detected
            }
    
    def save_stability_report(self, output_dir: str):
        """保存稳定性报告"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp = int(time.time())
            report_file = os.path.join(output_dir, f'stability_report_{timestamp}.json')
            
            # 清理报告数据
            clean_report = self._clean_stability_data_for_json(self.stability_report)
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(clean_report, f, indent=2, ensure_ascii=False)
            
            self._log_info(f"稳定性报告已保存: {report_file}")
            
        except Exception as e:
            self._log_error(f"保存稳定性报告失败: {e}")
    
    def _clean_stability_data_for_json(self, data):
        """清理稳定性数据用于JSON序列化"""
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
    
    def reset(self):
        """重置检测器"""
        self.frame_count = 0
        self.tracking_history.clear()
        self.detection_details.clear()
        self.position_history_3d.clear()
        self.movement_detected = False
        self.movement_frame = -1
        self.is_stable = False
        self.stability_report = {}
        self._log_info("Enhanced stability detector reset")
    
    def _log_info(self, message: str):
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[ENHANCED_STABILITY] {message}")
    
    def _log_debug(self, message: str):
        if self.logger:
            self.logger.debug(message)
        else:
            print(f"[ENHANCED_STABILITY] DEBUG: {message}")
    
    def _log_error(self, message: str):
        if self.logger:
            self.logger.error(message)
        else:
            print(f"[ENHANCED_STABILITY] ERROR: {message}")


class IntegratedTrackingNode(Node):
    """集成版追踪节点 - MultiObjectTracker + 手眼补偿 - 修复版"""
    
    def __init__(self):
        super().__init__('integrated_tracking_node')
        
        # 系统状态
        self.current_state = "WAITING_DETECTION_COMPLETE"
        
        # 目标信息 - 等待detection_complete信号设置
        self.scan_directory = None
        self.target_object_id = None
        self.target_class_id = None
        self.tracking_target_name = None
        self.current_tracked_target_id = None
        
        # 调试输出目录
        self.debug_output_dir = None
        
        # 图像数据
        self.current_color_image = None
        self.current_depth_image = None
        self.data_lock = threading.Lock()
        
        # 追踪系统组件 - 初始化为None，等待设置
        self.config = None
        self.realtime_detector = None
        self.multi_object_tracker = None
        self.stability_detector = None
        
        # 检测控制
        self.detection_active = False
        self.processing_timer = None
        
        # 手眼标定补偿相关
        self.hand_eye_compensation_offset = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.compensation_history = []
        
        # 设置基础ROS接口
        self._setup_basic_ros_interface()
        
        self.get_logger().info('集成版追踪节点启动完成 - 等待检测完成信号')
        self.get_logger().info('当前状态: WAITING_DETECTION_COMPLETE')
    
    def _setup_basic_ros_interface(self):
        """设置基础ROS2接口"""
        # 基础订阅者
        self.detection_complete_sub = self.create_subscription(
            String, '/detection_complete', 
            self.detection_complete_callback, 10
        )
        
        # 图像订阅者 - 先订阅但不处理
        self.color_image_sub = self.create_subscription(
            Image, '/camera/color/image_raw',
            self.color_image_callback, 10
        )
        
        self.depth_image_sub = self.create_subscription(
            Image, '/camera/depth/image_raw',
            self.depth_image_callback, 10
        )
        
        # 基础发布者
        self.status_pub = self.create_publisher(String, '/tracking/status', 10)
        self.stability_pub = self.create_publisher(String, '/tracking/stability', 10)
        self.debug_pub = self.create_publisher(String, '/tracking/debug', 10)
        self.tracking_visualization_pub = self.create_publisher(Image, '/tracking/visualization', 10)
        
        # 状态发布定时器
        self.status_timer = self.create_timer(2.0, self.publish_status)
    
    def detection_complete_callback(self, msg):
        """检测完成回调 - 核心初始化流程"""
        try:
            self.get_logger().info("接收到检测完成信号，开始初始化追踪系统")
            
            # 1. 解析检测完成信号
            if not self._parse_detection_complete_signal(msg):
                self.get_logger().error("解析检测完成信号失败")
                return
            
            # 2. 设置调试输出目录
            self._setup_debug_output_directory()
            
            # 3. 加载追踪目标信息
            if not self._load_tracking_target():
                self.get_logger().error("加载追踪目标失败")
                return
            
            # 4. 初始化追踪系统
            if not self._initialize_tracking_system():
                self.get_logger().error("初始化追踪系统失败")
                return
            
            # 5. 加载手眼补偿配置
            self._load_compensation_offset()
            
            # 6. 启动稳定性检测
            self._start_stability_detection()
            
            self.get_logger().info("追踪系统初始化完成，开始稳定性检测")
            
        except Exception as e:
            self.get_logger().error(f"检测完成回调失败: {e}")
            import traceback
            self.get_logger().error(f"详细错误: {traceback.format_exc()}")
    
    def _parse_detection_complete_signal(self, msg) -> bool:
        """解析检测完成信号"""
        try:
            data = json.loads(msg.data)
            scan_directory = data.get('scan_directory', '')
            
            if scan_directory and not os.path.isabs(scan_directory):
                workspace_root = os.path.expanduser("~/ros2_ws")
                scan_directory = os.path.join(workspace_root, scan_directory)
            
            self.scan_directory = scan_directory
            
            if not self.scan_directory or not os.path.exists(self.scan_directory):
                self.get_logger().error(f"扫描目录无效: {self.scan_directory}")
                return False
            
            self.get_logger().info(f"检测完成信号解析成功: {self.scan_directory}")
            return True
            
        except Exception as e:
            self.get_logger().error(f"解析检测完成信号失败: {e}")
            return False
    
    def _setup_debug_output_directory(self):
        """设置调试输出目录"""
        try:
            self.debug_output_dir = os.path.join(self.scan_directory, "tracking_debug")
            os.makedirs(self.debug_output_dir, exist_ok=True)
            self.get_logger().info(f"调试输出目录设置成功: {self.debug_output_dir}")
        except Exception as e:
            self.get_logger().error(f"设置调试输出目录失败: {e}")
    
    def _load_tracking_target(self) -> bool:
        """加载追踪目标信息"""
        try:
            # 读取tracking_selection.txt
            selection_file = os.path.join(self.scan_directory, 'detection_results', 'tracking_selection.txt')
            
            if not os.path.exists(selection_file):
                self.get_logger().error(f"未找到tracking_selection.txt: {selection_file}")
                return False
            
            with open(selection_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.get_logger().info(f"tracking_selection.txt内容:\n{content}")
            
            # 解析选择的目标ID
            match = re.search(r'\(ID:\s*([^)]+)\)', content)
            if not match:
                self.get_logger().error("无法从tracking_selection.txt解析目标ID")
                return False
            
            self.target_object_id = match.group(1).strip()
            
            # 临时创建配置来获取类别信息
            temp_config = create_tracking_config()
            
            # 从内容解析类别名称
            for class_name in temp_config.class_names.values():
                if class_name in content:
                    self.tracking_target_name = class_name
                    break
            
            # 获取class_id
            for class_id, class_name in temp_config.class_names.items():
                if class_name == self.tracking_target_name:
                    self.target_class_id = class_id
                    break
            
            if not self.tracking_target_name or self.target_class_id is None:
                self.get_logger().error("无法确定目标类别信息")
                return False
            
            self.get_logger().info(f"追踪目标信息加载成功:")
            self.get_logger().info(f"   目标ID: {self.target_object_id}")
            self.get_logger().info(f"   类别名称: {self.tracking_target_name}")
            self.get_logger().info(f"   类别ID: {self.target_class_id}")
            
            return True
                
        except Exception as e:
            self.get_logger().error(f"加载追踪目标失败: {e}")
            import traceback
            self.get_logger().error(f"详细错误: {traceback.format_exc()}")
            return False
    
    def _initialize_tracking_system(self) -> bool:
        """初始化追踪系统组件"""
        try:
            self.get_logger().info("开始初始化追踪系统组件")
            
            # 1. 创建配置
            self.config = create_tracking_config()
            self.get_logger().info("追踪配置创建成功")
            
            # 2. 初始化实时检测器
            self.realtime_detector = RealtimeDetector(self.config, self.get_logger())
            self.get_logger().info("实时检测器初始化成功")
            
            # 3. 初始化多目标追踪器
            self.multi_object_tracker = MultiObjectTracker(self.config)
            self.get_logger().info("多目标追踪器初始化成功")
            
            # 4. 初始化稳定性检测器
            self.stability_detector = EnhancedStabilityDetector(self.get_logger())
            self.get_logger().info("稳定性检测器初始化成功")
            
            # 5. 显示详细配置
            self._log_current_config()
            
            self.get_logger().info("追踪系统所有组件初始化完成")
            return True
            
        except Exception as e:
            self.get_logger().error(f"初始化追踪系统失败: {e}")
            import traceback
            self.get_logger().error(f"详细错误: {traceback.format_exc()}")
            return False
    
    def _log_current_config(self):
        """显示当前配置"""
        self.get_logger().info('当前追踪配置:')
        self.get_logger().info(f'   追踪目标: {self.tracking_target_name}')
        self.get_logger().info(f'   目标ID: {self.target_object_id}')
        self.get_logger().info(f'   最大丢失帧数: {self.config.get_max_lost_frames()}')
        self.get_logger().info(f'   匹配阈值: {self.config.get_feature_match_threshold()}')
        weights = self.config.get_feature_weights()
        self.get_logger().info(f'   特征权重: {weights}')
    
    def _start_stability_detection(self):
        """启动稳定性检测"""
        try:
            self.current_state = "DETECTING"
            self.stability_detector.reset()
            self.detection_active = True
            
            # 启动图像处理定时器
            if self.processing_timer is None:
                self.processing_timer = self.create_timer(0.2, self.process_frame_callback)  # 5Hz
            
            self.get_logger().info("稳定性检测已启动")
            self.get_logger().info(f"   目标: {self.target_object_id}")
            self.get_logger().info(f"   目标类别: {self.tracking_target_name}")
            self.get_logger().info(f"   类别ID: {self.target_class_id}")
            
        except Exception as e:
            self.get_logger().error(f"启动稳定性检测失败: {e}")
    
    def _stop_stability_detection(self):
        """停止稳定性检测"""
        try:
            self.detection_active = False
            
            # 停止图像处理定时器
            if self.processing_timer is not None:
                self.processing_timer.cancel()
                self.processing_timer = None
            
            self.get_logger().info("稳定性检测已停止")
            
            # 保存调试数据
            if self.debug_output_dir and self.stability_detector:
                self.stability_detector.save_stability_report(self.debug_output_dir)
                
        except Exception as e:
            self.get_logger().error(f"停止稳定性检测失败: {e}")
    
    def process_frame_callback(self):
        """图像处理定时器回调 - 核心追踪逻辑"""
        try:
            # 检查是否应该处理
            if not self.detection_active or not self._is_tracking_system_ready():
                return
            
            with self.data_lock:
                if (self.current_color_image is None or 
                    self.current_depth_image is None):
                    return
                
                self._process_tracking_frame()
                
        except Exception as e:
            self.get_logger().error(f"图像处理回调失败: {e}")
    
    def _is_tracking_system_ready(self) -> bool:
        """检查追踪系统是否就绪"""
        return (self.realtime_detector is not None and 
                self.multi_object_tracker is not None and 
                self.stability_detector is not None and
                self.tracking_target_name is not None)
    
    def _process_tracking_frame(self):
        """处理追踪帧"""
        try:
            current_frame = self.stability_detector.frame_count + 1
            self.get_logger().info(f"处理第{current_frame}帧，目标15帧")
            
            # 运行检测
            detection_results = self.realtime_detector.detect_and_segment(
                self.current_color_image, self.current_depth_image
            )
            
            # 调用MultiObjectTracker更新轨迹
            active_tracks = self.multi_object_tracker.update_tracks(detection_results)
            
            # 记录帧详情
            frame_details = {
                'total_detections': len(detection_results),
                'total_tracks': len(active_tracks),
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
                self.get_logger().info(f"第{current_frame}帧检测到对象: {detected_info}")
            else:
                self.get_logger().info(f"第{current_frame}帧未检测到任何对象")
            
            # 寻找目标轨迹
            target_track = None
            for track in active_tracks:
                # 检查是否是目标类别，并且状态良好
                if (track.class_name == self.tracking_target_name and 
                    track.lost_frames <= self.config.get_max_lost_frames()):
                    target_track = track
                    self.current_tracked_target_id = track.track_id
                    break
            
            if target_track:
                self.get_logger().info(f"第{current_frame}帧找到目标轨迹:")
                self.get_logger().info(f"   轨迹ID: {target_track.track_id}")
                self.get_logger().info(f"   类别: {target_track.class_name}")
                self.get_logger().info(f"   置信度: {target_track.confidence:.4f}")
                self.get_logger().info(f"   丢失帧数: {target_track.lost_frames}")
                self.get_logger().info(f"   轨迹年龄: {target_track.age}")
                
                # 更新世界坐标
                if hasattr(target_track, 'current_features') and target_track.current_features:
                    world_coords = target_track.current_features.spatial.get('world_coordinates')
                    if not world_coords and hasattr(target_track, 'world_coordinates'):
                        world_coords = target_track.world_coordinates
                else:
                    world_coords = getattr(target_track, 'world_coordinates', [0, 0, 0])
                
                if world_coords and len(world_coords) >= 3:
                    self.get_logger().info(f"   世界坐标: [{world_coords[0]:.1f}, {world_coords[1]:.1f}, {world_coords[2]:.1f}]")
                else:
                    self.get_logger().warn("   无世界坐标信息")
            else:
                self.get_logger().info(f"第{current_frame}帧未找到目标轨迹: {self.tracking_target_name}")
                self.current_tracked_target_id = None
                
                # 分析为什么找不到目标
                target_class_tracks = [t for t in active_tracks if t.class_name == self.tracking_target_name]
                if not target_class_tracks:
                    self.get_logger().info(f"   原因: 未追踪到目标类别 {self.tracking_target_name} 的轨迹")
                else:
                    lost_info = [(t.track_id, t.lost_frames) for t in target_class_tracks]
                    self.get_logger().info(f"   检测到 {len(target_class_tracks)} 个目标类别轨迹，但丢失帧数过多: {lost_info}")
            
            # 发布调试信息和可视化
            self._publish_debug_info(frame_details, target_track, active_tracks)
            self._publish_visualization(active_tracks)
            
            # 添加到稳定性检测器
            self.stability_detector.add_tracking_result(
                target_track, active_tracks, frame_details
            )
            
            # 检查是否完成15帧检测
            frames_collected = len(self.stability_detector.tracking_history)
            self.get_logger().info(f"已收集帧数: {frames_collected}/15")
            
            if frames_collected >= 15:
                self.get_logger().info("15帧检测完成，开始稳定性分析...")
                self._handle_stability_check_complete()
            else:
                self.get_logger().info(f"稳定性检测进度: {frames_collected}/15 帧")
            
        except Exception as e:
            self.get_logger().error(f"追踪帧处理失败: {e}")
            import traceback
            self.get_logger().error(f"详细错误: {traceback.format_exc()}")
    
    def _handle_stability_check_complete(self):
        """处理稳定性检测完成"""
        try:
            self.get_logger().info("开始稳定性分析...")
            
            # 停止检测
            self._stop_stability_detection()
            
            # 执行稳定性检查
            stability_result = self.stability_detector.check_stability()
            
            # 发布稳定性结果
            self._publish_stability_result(stability_result)
            
            if stability_result['is_stable']:
                self.current_state = "STABLE_DETECTED"
                self.get_logger().info("目标稳定，询问用户是否进入抓取模式...")
                self._show_detailed_grasp_dialog(stability_result)
            else:
                self.current_state = "IDLE"
                reason = stability_result.get('reason', '未知原因')
                self.get_logger().warn(f"目标不稳定: {reason}")
                
                # 显示改进建议
                self._show_stability_improvement_suggestions(stability_result)
                
                self.get_logger().info("10秒后重新开始检测...")
                threading.Timer(10.0, self._start_stability_detection).start()
            
        except Exception as e:
            self.get_logger().error(f"处理稳定性检测完成失败: {e}")
            import traceback
            self.get_logger().error(f"详细错误: {traceback.format_exc()}")
    
    def _publish_debug_info(self, frame_details, target_track, all_tracks):
        """发布调试信息"""
        try:
            debug_data = {
                'timestamp': time.time(),
                'frame_number': self.stability_detector.frame_count + 1,
                'frame_details': frame_details,
                'target_track': {
                    'found': target_track is not None,
                    'track_id': target_track.track_id if target_track else None,
                    'confidence': target_track.confidence if target_track else 0.0,
                    'lost_frames': target_track.lost_frames if target_track else 0,
                    'age': target_track.age if target_track else 0,
                    'world_coordinates': getattr(target_track, 'world_coordinates', [0, 0, 0]) if target_track else [0, 0, 0]
                },
                'tracking_stats': {
                    'total_active_tracks': len(all_tracks),
                    'target_class_tracks': len([t for t in all_tracks if t.class_name == self.tracking_target_name]),
                    'compensation_offset': self.hand_eye_compensation_offset.tolist()
                }
            }
            
            debug_msg = String()
            debug_msg.data = json.dumps(debug_data, indent=2)
            self.debug_pub.publish(debug_msg)
            
        except Exception as e:
            self.get_logger().error(f"发布调试信息失败: {e}")
    
    def _publish_visualization(self, active_tracks):
        """发布可视化图像"""
        try:
            if self.current_color_image is None:
                return
            
            # 创建可视化图像
            vis_image = self.current_color_image.copy()
            
            for track in active_tracks:
                # 绘制轨迹的当前 BBox
                bbox_int = [int(x) for x in track.bbox]
                x1, y1, x2, y2 = bbox_int
                
                # 根据轨迹状态选择颜色
                if track.lost_frames == 0:
                    if track.class_name == self.tracking_target_name:
                        color = (0, 255, 0)  # 绿色 - 目标轨迹且当前匹配
                    else:
                        color = (0, 255, 255)  # 黄色 - 其他轨迹且当前匹配
                else:
                    color = (0, 0, 255)  # 红色 - 丢失/预测状态
                
                thickness = 3 if track.class_name == self.tracking_target_name else 2
                
                # 绘制边界框
                cv2.rectangle(vis_image, (x1, y1), (x2, y2), color, thickness)
                
                # 绘制轨迹信息
                label = f"ID:{track.track_id} {track.class_name}"
                if track.class_name == self.tracking_target_name:
                    label = f"TARGET {label}"
                
                info_text = f"{label} (C:{track.confidence:.2f}, L:{track.lost_frames})"
                
                # 计算文本位置
                label_size = cv2.getTextSize(info_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                cv2.rectangle(vis_image, (x1, y1 - label_size[1] - 10), 
                             (x1 + label_size[0], y1), color, -1)
                cv2.putText(vis_image, info_text, (x1, y1 - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # 绘制质心
                if hasattr(track, 'current_features'):
                    centroid = track.current_features.spatial.get('centroid_2d', [0, 0])
                else:
                    # 从bbox计算质心
                    centroid = [(x1 + x2) / 2, (y1 + y2) / 2]
                
                cx, cy = int(centroid[0]), int(centroid[1])
                cv2.circle(vis_image, (cx, cy), 5, color, -1)
                
                # 如果有预测框，也绘制
                if track.lost_frames > 0:
                    cv2.rectangle(vis_image, (x1, y1), (x2, y2), (255, 255, 0), 1)
            
            # 转换为ROS Image消息并发布
            vis_msg = Image()
            vis_msg.header.stamp = self.get_clock().now().to_msg()
            vis_msg.header.frame_id = "camera_link"
            vis_msg.height = vis_image.shape[0]
            vis_msg.width = vis_image.shape[1]
            vis_msg.encoding = "rgb8"
            vis_msg.is_bigendian = False
            vis_msg.step = vis_msg.width * 3
            vis_msg.data = vis_image.flatten().tobytes()
            
            self.tracking_visualization_pub.publish(vis_msg)
            
        except Exception as e:
            self.get_logger().error(f"发布可视化失败: {e}")
    
    def _show_stability_improvement_suggestions(self, stability_result):
        """显示稳定性改进建议"""
        try:
            print("\n" + "="*60)
            print("稳定性分析报告")
            print("="*60)
            
            track_stability = stability_result.get('track_stability', 0)
            track_quality = stability_result.get('track_quality', 0)
            position_stability = stability_result.get('position_stability', 0)
            
            print(f"追踪稳定性: {track_stability:.1%}")
            print(f"轨迹质量: {track_quality:.1%}")
            print(f"位置稳定性: {position_stability:.1%}")
            print(f"综合稳定性: {stability_result.get('overall_stability', 0):.1%}")
            
            print("\n改进建议:")
            
            if track_stability < 0.6:
                print("- 追踪稳定性较低，可能需要:")
                print("  • 检查目标对象是否在视野中")
                print("  • 调整追踪参数")
                print("  • 改善光照条件")
                
            if track_quality < 0.6:
                print("- 轨迹质量较低，可能需要:")
                print("  • 提高检测置信度阈值")
                print("  • 减少遮挡和干扰")
                print("  • 确保目标对象清晰可见")
                
            if position_stability < 0.6:
                print("- 位置稳定性较低，可能需要:")
                print("  • 增加位置容差")
                print("  • 检查相机稳定性")
                print("  • 避免目标对象移动")
                
            print("="*60)
            
        except Exception as e:
            self.get_logger().error(f"显示改进建议失败: {e}")
    
    def _show_detailed_grasp_dialog(self, stability_result):
        """显示详细的抓取对话框"""
        try:
            self.current_state = "WAITING_INPUT"
            
            print("\n" + "="*60)
            print("目标稳定性检测完成!")
            print("="*60)
            print(f"目标对象: {self.target_object_id}")
            print(f"目标类别: {self.tracking_target_name}")
            
            # 显示详细统计
            print(f"\n稳定性分析:")
            print(f"  追踪稳定性: {stability_result['track_stability']:.1%}")
            print(f"  轨迹质量: {stability_result['track_quality']:.1%}")
            print(f"  位置稳定性: {stability_result['position_stability']:.1%}")
            print(f"  综合稳定性: {stability_result['overall_stability']:.1%}")
            
            print(f"\n手眼标定补偿:")
            print(f"  当前补偿偏移: [{self.hand_eye_compensation_offset[0]:.1f}, {self.hand_eye_compensation_offset[1]:.1f}, {self.hand_eye_compensation_offset[2]:.1f}] mm")
            print(f"  历史补偿次数: {len(self.compensation_history)}")
            
            print(f"\n调试文件已保存到: {self.debug_output_dir}")
            print("="*60)
            
            # 在新线程中处理用户输入
            threading.Thread(target=self._handle_user_input, daemon=True).start()
            
        except Exception as e:
            self.get_logger().error(f"显示详细抓取对话框失败: {e}")
    
    def _handle_user_input(self):
        """处理用户输入"""
        try:
            while self.current_state == "WAITING_INPUT":
                user_input = input("\n是否进入抓取模式? (y/n/r-重新检测/d-查看调试): ").strip().lower()
                
                if user_input in ['y', 'yes']:
                    self.get_logger().info("用户确认进入抓取模式")
                    self.current_state = "GRASP_READY"
                    self._send_grasp_command_with_compensation()
                    break
                    
                elif user_input in ['n', 'no']:
                    self.get_logger().info("用户取消抓取，重新开始检测")
                    self.current_state = "IDLE"
                    threading.Timer(2.0, self._start_stability_detection).start()
                    break
                    
                elif user_input in ['r', 'restart']:
                    self.get_logger().info("用户要求重新检测")
                    self.current_state = "IDLE"
                    threading.Timer(1.0, self._start_stability_detection).start()
                    break
                    
                elif user_input in ['d', 'debug']:
                    self._show_debug_summary()
                    
                else:
                    print("请输入 y(进入抓取)/n(取消)/r(重新检测)/d(查看调试)")
                    
        except Exception as e:
            self.get_logger().error(f"处理用户输入失败: {e}")
    
    def _show_debug_summary(self):
        """显示调试摘要"""
        try:
            print("\n" + "="*60)
            print("调试信息摘要")
            print("="*60)
            
            # 追踪器统计
            print(f"MultiObjectTracker统计:")
            print(f"  当前活跃轨迹: {len(self.multi_object_tracker.active_tracks)}")
            print(f"  目标轨迹ID: {self.current_tracked_target_id}")
            
            # 显示活跃轨迹详情
            if self.multi_object_tracker.active_tracks:
                print(f"  活跃轨迹详情:")
                for track_id, track in self.multi_object_tracker.active_tracks.items():
                    status = "TARGET" if track.class_name == self.tracking_target_name else "      "
                    print(f"    {status} ID:{track_id} {track.class_name} (conf:{track.confidence:.2f}, lost:{track.lost_frames})")
            
            # 手眼补偿历史
            if self.compensation_history:
                print(f"\n手眼补偿历史 (最近5次):")
                recent_history = self.compensation_history[-5:]
                for i, hist in enumerate(recent_history, 1):
                    success_str = "SUCCESS" if hist['success'] else "FAILED"
                    print(f"    {i}. {success_str} 偏移: {hist['offset']}")
            
            print(f"\n详细调试文件位置: {self.debug_output_dir}")
            print("="*60)
            
        except Exception as e:
            self.get_logger().error(f"显示调试摘要失败: {e}")
    
    # ==================== 手眼标定补偿方法 ====================
    
    def _load_compensation_offset(self):
        """从文件加载手眼标定补偿偏移量"""
        try:
            # 使用scan_directory下的补偿文件，如果不存在则使用默认路径
            if self.scan_directory:
                compensation_file = os.path.join(self.scan_directory, 'hand_eye_compensation.json')
            else:
                compensation_file = os.path.expanduser('~/ros2_ws/src/vision_ai/config/hand_eye_compensation.json')
            
            if os.path.exists(compensation_file):
                with open(compensation_file, 'r') as f:
                    data = json.load(f)
                    self.hand_eye_compensation_offset = np.array(data.get('offset', [0.0, 0.0, 0.0]), dtype=np.float32)
                    self.compensation_history = data.get('history', [])
                    self.get_logger().info(f"成功加载手眼补偿偏移量: {self.hand_eye_compensation_offset} mm")
            else:
                self.get_logger().info("未找到手眼补偿配置文件，使用默认偏移量 [0,0,0]")
        except Exception as e:
            self.get_logger().warn(f"加载手眼补偿偏移量失败: {e}")
    
    def _save_compensation_offset(self):
        """保存当前手眼标定补偿偏移量到文件"""
        try:
            # 保存到scan_directory下
            if self.scan_directory:
                compensation_file = os.path.join(self.scan_directory, 'hand_eye_compensation.json')
            else:
                compensation_dir = os.path.expanduser('~/ros2_ws/src/vision_ai/config')
                os.makedirs(compensation_dir, exist_ok=True)
                compensation_file = os.path.join(compensation_dir, 'hand_eye_compensation.json')
            
            data = {
                'offset': self.hand_eye_compensation_offset.tolist(),
                'history': self.compensation_history,
                'last_updated': time.time(),
                'total_adjustments': len(self.compensation_history)
            }
            
            with open(compensation_file, 'w') as f:
                json.dump(data, f, indent=4)
            self.get_logger().info(f"手眼补偿偏移量已保存: {self.hand_eye_compensation_offset} mm")
        except Exception as e:
            self.get_logger().error(f"保存手眼补偿偏移量失败: {e}")
    
    def grasp_result_callback(self, msg):
        """
        接收抓取结果反馈，并调整手眼补偿偏移量
        注意：需要定义GraspResult消息类型
        """
        try:
            success = msg.success 
            learning_rate_pos = 0.05  # 补偿学习率
            
            if success:
                self.get_logger().info("抓取成功！微调手眼补偿偏移量。")
                # 抓取成功时，缓慢减少补偿量，使其趋向于更准确的标定值
                self.hand_eye_compensation_offset *= 0.99 
                error_vector_for_log = [0.0, 0.0, 0.0]
            else:
                self.get_logger().warn("抓取失败！调整手眼补偿偏移量。")
                # 这里需要根据具体的失败反馈来调整
                if hasattr(msg, 'error_vector') and msg.error_vector:
                    error_vector = np.array(msg.error_vector, dtype=np.float32)
                else:
                    # 简单的随机探索策略
                    error_vector = np.random.uniform(-2.0, 2.0, 3).astype(np.float32)
                    self.get_logger().warn("使用随机探索策略调整补偿")
                
                self.hand_eye_compensation_offset += learning_rate_pos * error_vector
                # 限制补偿范围
                self.hand_eye_compensation_offset = np.clip(self.hand_eye_compensation_offset, -50.0, 50.0)
                error_vector_for_log = error_vector.tolist()
            
            # 记录历史并保存
            self.compensation_history.append({
                'timestamp': self.get_clock().now().to_msg().sec, 
                'offset': self.hand_eye_compensation_offset.tolist(), 
                'success': success, 
                'error_vector': error_vector_for_log
            })
            self._save_compensation_offset()
            
        except Exception as e:
            self.get_logger().error(f"处理抓取结果反馈失败: {e}")
    
    def _send_grasp_command_with_compensation(self):
        """发送带补偿的抓取指令"""
        try:
            if self.current_tracked_target_id is None:
                self.get_logger().error("没有当前追踪的目标轨迹")
                return
            
            # 获取目标轨迹
            target_track = None
            for track in self.multi_object_tracker.active_tracks.values():
                if track.track_id == self.current_tracked_target_id:
                    target_track = track
                    break
            
            if not target_track:
                self.get_logger().error("未找到目标轨迹")
                return
            
            # 获取原始世界坐标
            object_world_coords = np.array(target_track.world_coordinates, dtype=np.float32)
            recommended_gripper_width = target_track.recommended_gripper_width_mm
            gripper_angle = target_track.gripper_angle
            
            # 应用手眼标定补偿偏移量
            final_grasp_world_coords = object_world_coords + self.hand_eye_compensation_offset
            
            self.get_logger().info(f"发送抓取指令:")
            self.get_logger().info(f"   原始抓取点: {object_world_coords}")
            self.get_logger().info(f"   应用补偿: {self.hand_eye_compensation_offset}")
            self.get_logger().info(f"   最终抓取点: {final_grasp_world_coords}")
            self.get_logger().info(f"   夹爪宽度: {recommended_gripper_width}mm")
            self.get_logger().info(f"   夹爪角度: {gripper_angle}°")
            
            # 发布抓取就绪信号
            self._publish_grasp_ready_with_compensation(final_grasp_world_coords, recommended_gripper_width, gripper_angle)
            
        except Exception as e:
            self.get_logger().error(f"发送抓取指令失败: {e}")
    
    def _publish_grasp_ready_with_compensation(self, final_coords, gripper_width, gripper_angle):
        """发布带补偿的抓取就绪信号"""
        try:
            grasp_data = {
                'object_id': self.target_object_id,
                'class_name': self.tracking_target_name,
                'track_id': self.current_tracked_target_id,
                'world_coordinates': final_coords.tolist(),
                'original_coordinates': [coord - offset for coord, offset in zip(final_coords, self.hand_eye_compensation_offset)],
                'compensation_offset': self.hand_eye_compensation_offset.tolist(),
                'tracking_height': final_coords[2] + 200,  # 抓取高度
                'gripper_width': gripper_width,
                'gripper_angle': gripper_angle,
                'yaw_angle': 0.0,
                'stability_report': self.stability_detector.stability_report,
                'compensation_history_count': len(self.compensation_history),
                'debug_output_dir': self.debug_output_dir,
                'timestamp': time.time()
            }
            
            grasp_msg = String()
            grasp_msg.data = json.dumps(grasp_data, indent=2)
            
            grasp_ready_pub = self.create_publisher(String, '/tracking/grasp_ready', 10)
            grasp_ready_pub.publish(grasp_msg)
            
            self.get_logger().info("已发布带补偿的抓取就绪信号")
            
        except Exception as e:
            self.get_logger().error(f"发布抓取就绪信号失败: {e}")
    
    def _publish_stability_result(self, stability_result):
        """发布稳定性结果"""
        try:
            # 清理数据确保可序列化
            clean_result = self._clean_for_json_serialization(stability_result)
            
            stability_msg = String()
            stability_msg.data = json.dumps(clean_result, indent=2)
            self.stability_pub.publish(stability_msg)
            
        except Exception as e:
            self.get_logger().error(f"发布稳定性结果失败: {e}")
    
    def _clean_for_json_serialization(self, data):
        """递归清理数据使其可JSON序列化"""
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
    
    # ==================== ROS回调方法 ====================
    
    def color_image_callback(self, msg):
        """彩色图像回调 - 保持原有转换方式"""
        try:
            with self.data_lock:
                if msg.step == msg.width * 3:  # 正确的RGB步长
                    image_array = np.frombuffer(msg.data, dtype=np.uint8)
                    self.current_color_image = image_array.reshape((msg.height, msg.width, 3))
                else:
                    # 如果步长不对，尝试重新解释数据
                    self.get_logger().warn(f'意外的color image步长: {msg.step}, 期望: {msg.width * 3}')
                    image_array = np.frombuffer(msg.data, dtype=np.uint8)
                    try:
                        self.current_color_image = image_array.reshape((msg.height, msg.width, 3))
                    except ValueError as e:
                        self.get_logger().error(f'Color image reshape失败: {e}')
                        return
                        
        except Exception as e:
            self.get_logger().error(f"彩色图像回调失败: {e}")

    def depth_image_callback(self, msg):
        """深度图像回调 - 保持原有转换方式"""
        try:
            with self.data_lock:
                self.get_logger().debug(f'Depth message: encoding={msg.encoding}, step={msg.step}, expected={msg.width * 2}')
                
                if msg.step == msg.width * 2:  # 正确的16位步长
                    image_array = np.frombuffer(msg.data, dtype=np.uint16)
                    self.current_depth_image = image_array.reshape((msg.height, msg.width))
                else:
                    # 修复深度图像步长问题
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
            self.get_logger().error(f"深度图像回调失败: {e}")
            import traceback
            self.get_logger().error(f'详细错误: {traceback.format_exc()}')
    
    def publish_status(self):
        """发布系统状态"""
        try:
            status_data = {
                'node': 'integrated_tracking_node',
                'state': self.current_state,
                'target_object_id': self.target_object_id,
                'target_class_name': self.tracking_target_name,
                'current_tracked_target_id': self.current_tracked_target_id,
                'scan_directory': self.scan_directory,
                'debug_output_dir': self.debug_output_dir,
                'detection_active': self.detection_active,
                'frame_count': self.stability_detector.frame_count if self.stability_detector else 0,
                'frames_collected': len(self.stability_detector.tracking_history) if self.stability_detector else 0,
                'active_tracks_count': len(self.multi_object_tracker.active_tracks) if self.multi_object_tracker else 0,
                'tracking_system_ready': self._is_tracking_system_ready(),
                'hand_eye_compensation': {
                    'current_offset': self.hand_eye_compensation_offset.tolist(),
                    'adjustment_count': len(self.compensation_history)
                },
                'timestamp': time.time()
            }
            
            status_msg = String()
            status_msg.data = json.dumps(status_data)
            self.status_pub.publish(status_msg)
            
        except Exception as e:
            self.get_logger().error(f"发布状态失败: {e}")
    
    def destroy_node(self):
        """节点销毁清理"""
        try:
            self._stop_stability_detection()
            self._save_compensation_offset()  # 保存最终的补偿参数
            self.get_logger().info("集成版追踪节点已清理")
            
        except Exception as e:
            self.get_logger().error(f"节点清理失败: {e}")
        finally:
            super().destroy_node()


def main(args=None):
    """主函数"""
    rclpy.init(args=args)
    
    try:
        tracking_node = IntegratedTrackingNode()
        
        tracking_node.get_logger().info('集成版追踪节点启动完成，等待检测完成信号...')
        tracking_node.get_logger().info('修复版本特性:')
        tracking_node.get_logger().info('   正确的检测->追踪流程')
        tracking_node.get_logger().info('   延迟初始化追踪组件')
        tracking_node.get_logger().info('   MultiObjectTracker多目标追踪')
        tracking_node.get_logger().info('   增强稳定性检测')
        tracking_node.get_logger().info('   手眼标定自适应补偿')
        tracking_node.get_logger().info('   实时可视化')
        tracking_node.get_logger().info('   详细调试信息')
        
        rclpy.spin(tracking_node)
        
    except KeyboardInterrupt:
        print('\n用户中断，正在退出...')
    except Exception as e:
        print(f'追踪节点错误: {e}')
        import traceback
        print(f'详细错误: {traceback.format_exc()}')
    finally:
        if 'tracking_node' in locals():
            tracking_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()