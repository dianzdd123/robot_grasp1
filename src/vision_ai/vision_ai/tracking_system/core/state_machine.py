#!/usr/bin/env python3
"""
Tracking System State Machine
追踪系统状态机
"""

import time
import threading
from typing import Dict, Any, Optional, Callable
from ..utils.config import TrackingState, TrackingMode, TrackingConfig


class TrackingStateMachine:
    """追踪系统状态机"""
    
    def __init__(self, config: TrackingConfig, logger=None):
        """
        初始化状态机
        
        Args:
            config: 追踪配置
            logger: 日志记录器
        """
        self.config = config
        self.logger = logger
        
        # 状态管理
        self.current_state = TrackingState.IDLE
        self.previous_state = TrackingState.IDLE
        self.current_mode = TrackingMode.FULL_MATCHING
        
        # 状态变更历史
        self.state_history = []
        self.state_start_time = time.time()
        
        # 追踪统计
        self.lost_frames_count = 0
        self.successful_tracking_frames = 0
        self.lightweight_tracking_frames = 0
        self.total_tracking_time = 0.0
        
        # 目标信息
        self.target_object_id = None
        self.target_class_id = None
        
        # 状态锁
        self.state_lock = threading.Lock()
        
        # 状态回调函数
        self.state_callbacks: Dict[TrackingState, Callable] = {}
        
        # 初始化状态转换规则
        self._initialize_state_transitions()
        
        self._log_info("🎯 追踪状态机初始化完成")
    
    def _initialize_state_transitions(self):
        """初始化状态转换规则"""
        # 定义允许的状态转换
        self.allowed_transitions = {
            TrackingState.IDLE: [
                TrackingState.INITIALIZING,
                TrackingState.ERROR
            ],
            TrackingState.INITIALIZING: [
                TrackingState.SEARCHING,
                TrackingState.ERROR,
                TrackingState.IDLE
            ],
            TrackingState.SEARCHING: [
                TrackingState.TRACKING,
                TrackingState.RECOVERY,
                TrackingState.ERROR,
                TrackingState.IDLE
            ],
            TrackingState.TRACKING: [
                TrackingState.APPROACHING,
                TrackingState.RECOVERY,
                TrackingState.ERROR,
                TrackingState.IDLE
            ],
            TrackingState.APPROACHING: [
                TrackingState.GRASPING,
                TrackingState.TRACKING,
                TrackingState.RECOVERY,
                TrackingState.ERROR
            ],
            TrackingState.GRASPING: [
                TrackingState.RETURNING,
                TrackingState.ERROR,
                TrackingState.RECOVERY
            ],
            TrackingState.RETURNING: [
                TrackingState.PLACING,
                TrackingState.ERROR
            ],
            TrackingState.PLACING: [
                TrackingState.IDLE,
                TrackingState.ERROR
            ],
            TrackingState.RECOVERY: [
                TrackingState.SEARCHING,
                TrackingState.TRACKING,
                TrackingState.IDLE,
                TrackingState.ERROR
            ],
            TrackingState.ERROR: [
                TrackingState.IDLE,
                TrackingState.RECOVERY
            ]
        }
    
    def transition_to(self, new_state: TrackingState, reason: str = "", force: bool = False) -> bool:
        """
        状态转换
        
        Args:
            new_state: 新状态
            reason: 转换原因
            force: 是否强制转换
        
        Returns:
            是否转换成功
        """
        with self.state_lock:
            # 检查是否为有效转换
            if not force and new_state not in self.allowed_transitions.get(self.current_state, []):
                self._log_warn(f"❌ 无效状态转换: {self.current_state} → {new_state}")
                return False
            
            # 记录状态变更
            self.previous_state = self.current_state
            state_duration = time.time() - self.state_start_time
            
            # 更新状态历史
            self.state_history.append({
                'from_state': self.previous_state,
                'to_state': new_state,
                'duration': state_duration,
                'timestamp': time.time(),
                'reason': reason
            })
            
            # 执行状态退出处理
            self._on_state_exit(self.current_state)
            
            # 更新当前状态
            self.current_state = new_state
            self.state_start_time = time.time()
            
            # 执行状态进入处理
            self._on_state_enter(new_state)
            
            # 日志记录
            force_str = " (强制)" if force else ""
            self._log_info(f"🔄 状态转换{force_str}: {self.previous_state.value} → {new_state.value}")
            if reason:
                self._log_info(f"   原因: {reason}")
            
            # 执行状态回调
            if new_state in self.state_callbacks:
                try:
                    self.state_callbacks[new_state]()
                except Exception as e:
                    self._log_error(f"状态回调执行失败: {e}")
            
            return True
    
    def _on_state_enter(self, state: TrackingState):
        """状态进入处理"""
        if state == TrackingState.TRACKING:
            self.lost_frames_count = 0
            self.successful_tracking_frames = 0
            
        elif state == TrackingState.SEARCHING:
            self.lost_frames_count = 0
            
        elif state == TrackingState.RECOVERY:
            self._log_warn("🔧 进入回退状态，开始回退策略")
            
        elif state == TrackingState.ERROR:
            self._log_error("❌ 进入错误状态")
            
        elif state == TrackingState.IDLE:
            self._reset_tracking_stats()
    
    def _on_state_exit(self, state: TrackingState):
        """状态退出处理"""
        if state == TrackingState.TRACKING:
            # 记录追踪统计
            tracking_duration = time.time() - self.state_start_time
            self.total_tracking_time += tracking_duration
            self._log_info(f"📊 追踪阶段统计: 成功帧数={self.successful_tracking_frames}, 轻量级帧数={self.lightweight_tracking_frames}")
    
    def switch_tracking_mode(self, new_mode: TrackingMode, reason: str = "") -> bool:
        """
        切换追踪模式
        
        Args:
            new_mode: 新追踪模式
            reason: 切换原因
        
        Returns:
            是否切换成功
        """
        if self.current_mode == new_mode:
            return True
        
        previous_mode = self.current_mode
        self.current_mode = new_mode
        
        self._log_info(f"🔀 追踪模式切换: {previous_mode.value} → {new_mode.value}")
        if reason:
            self._log_info(f"   原因: {reason}")
        
        # 根据模式更新统计
        if new_mode == TrackingMode.LIGHTWEIGHT_TRACKING:
            self.lightweight_tracking_frames = 0
        
        return True
    
    def update_target_info(self, object_id: str, class_id: int):
        """更新目标信息"""
        self.target_object_id = object_id
        self.target_class_id = class_id
        self._log_info(f"🎯 更新追踪目标: {object_id} (class_id: {class_id})")
    
    def on_detection_success(self, detection_mode: TrackingMode = TrackingMode.FULL_MATCHING):
        """检测成功回调"""
        self.lost_frames_count = 0
        self.successful_tracking_frames += 1
        
        if detection_mode == TrackingMode.LIGHTWEIGHT_TRACKING:
            self.lightweight_tracking_frames += 1
    
    def on_detection_failed(self):
        """检测失败回调"""
        self.lost_frames_count += 1
        
        # 检查是否需要进入回退状态
        max_lost_frames = self.config.get_max_lost_frames()
        if self.lost_frames_count >= max_lost_frames:
            self.transition_to(
                TrackingState.RECOVERY,
                f"连续{self.lost_frames_count}帧检测失败"
            )
    
    def check_approach_conditions(self, distance_xy: float, yaw_error: float) -> bool:
        """
        检查是否满足逼近条件
        
        Args:
            distance_xy: XY平面距离
            yaw_error: YAW角度误差
        
        Returns:
            是否满足逼近条件
        """
        xy_threshold = self.config.get_target_tolerance_xy()
        yaw_threshold = self.config.get_target_tolerance_yaw()
        
        xy_ok = distance_xy <= xy_threshold
        yaw_ok = abs(yaw_error) <= yaw_threshold
        
        if xy_ok and yaw_ok:
            self._log_info(f"✅ 满足逼近条件: distance={distance_xy:.1f}mm<={xy_threshold}mm, yaw_error={yaw_error:.1f}°<={yaw_threshold}°")
            return True
        
        return False
    
    def check_lightweight_tracking_conditions(self, class_detections_count: int) -> bool:
        """
        检查是否满足轻量级追踪条件
        
        Args:
            class_detections_count: 当前帧中目标类别的检测数量
        
        Returns:
            是否可以使用轻量级追踪
        """
        # 条件1: 当前帧中该类别只有一个对象
        if class_detections_count != 1:
            return False
        
        # 条件2: 当前正在追踪状态
        if self.current_state != TrackingState.TRACKING:
            return False
        
        # 条件3: 已经有足够的连续成功追踪帧
        required_frames = self.config.get_lightweight_continuity_frames()
        if self.successful_tracking_frames < required_frames:
            return False
        
        # 条件4: 当前模式允许切换到轻量级
        if self.current_mode == TrackingMode.SPATIAL_PREDICTION:
            return False
        
        return True
    
    def force_transition(self, new_state: TrackingState, reason: str = ""):
        """强制状态转换（用于紧急情况）"""
        self.transition_to(new_state, reason, force=True)
    
    def emergency_stop(self):
        """紧急停止"""
        self.force_transition(TrackingState.ERROR, "紧急停止")
        self._reset_tracking_stats()
        self._log_warn("🚨 执行紧急停止")
    
    def reset(self):
        """重置状态机"""
        with self.state_lock:
            self.transition_to(TrackingState.IDLE, "手动重置")
            self._reset_tracking_stats()
            self.state_history.clear()
            self._log_info("🔄 状态机已重置")
    
    def _reset_tracking_stats(self):
        """重置追踪统计"""
        self.lost_frames_count = 0
        self.successful_tracking_frames = 0
        self.lightweight_tracking_frames = 0
        self.target_object_id = None
        self.target_class_id = None
        self.current_mode = TrackingMode.FULL_MATCHING
    
    def register_state_callback(self, state: TrackingState, callback: Callable):
        """注册状态回调函数"""
        self.state_callbacks[state] = callback
        self._log_info(f"📝 注册状态回调: {state.value}")
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态机状态"""
        current_time = time.time()
        state_duration = current_time - self.state_start_time
        
        return {
            'current_state': self.current_state.value,
            'previous_state': self.previous_state.value,
            'current_mode': self.current_mode.value,
            'state_duration': state_duration,
            'lost_frames': self.lost_frames_count,
            'successful_frames': self.successful_tracking_frames,
            'lightweight_frames': self.lightweight_tracking_frames,
            'total_tracking_time': self.total_tracking_time,
            'target_id': self.target_object_id,
            'target_class_id': self.target_class_id,
            'state_history_count': len(self.state_history)
        }
    
    def get_state_history(self) -> list:
        """获取状态历史"""
        return self.state_history.copy()
    
    def is_in_state(self, state: TrackingState) -> bool:
        """检查是否在指定状态"""
        return self.current_state == state
    
    def is_in_mode(self, mode: TrackingMode) -> bool:
        """检查是否在指定模式"""
        return self.current_mode == mode
    
    def can_transition_to(self, state: TrackingState) -> bool:
        """检查是否可以转换到指定状态"""
        return state in self.allowed_transitions.get(self.current_state, [])
    
    def get_time_in_current_state(self) -> float:
        """获取在当前状态的时间"""
        return time.time() - self.state_start_time
    
    def should_enter_recovery(self) -> bool:
        """检查是否应该进入回退状态"""
        return (self.lost_frames_count >= self.config.get_max_lost_frames() and 
                self.current_state in [TrackingState.SEARCHING, TrackingState.TRACKING])
    
    def get_tracking_efficiency(self) -> Dict[str, float]:
        """获取追踪效率统计"""
        total_frames = self.successful_tracking_frames + self.lost_frames_count
        if total_frames == 0:
            return {'success_rate': 0.0, 'lightweight_rate': 0.0}
        
        success_rate = self.successful_tracking_frames / total_frames
        lightweight_rate = (self.lightweight_tracking_frames / self.successful_tracking_frames 
                           if self.successful_tracking_frames > 0 else 0.0)
        
        return {
            'success_rate': success_rate,
            'lightweight_rate': lightweight_rate,
            'total_frames': total_frames,
            'avg_tracking_time': (self.total_tracking_time / len(self.state_history) 
                                 if self.state_history else 0.0)
        }
    
    def print_status_summary(self):
        """打印状态摘要"""
        status = self.get_status()
        efficiency = self.get_tracking_efficiency()
        
        print("\n" + "="*40)
        print("🎯 TRACKING STATE MACHINE STATUS")
        print("="*40)
        print(f"🟢 当前状态: {status['current_state']}")
        print(f"🔄 当前模式: {status['current_mode']}")
        print(f"⏱️  状态持续时间: {status['state_duration']:.1f}s")
        print(f"🎯 追踪目标: {status['target_id'] or 'None'}")
        print(f"📊 成功帧数: {status['successful_frames']}")
        print(f"⚡ 轻量级帧数: {status['lightweight_frames']}")
        print(f"❌ 丢失帧数: {status['lost_frames']}")
        print(f"📈 成功率: {efficiency['success_rate']:.2%}")
        print(f"🚀 轻量级使用率: {efficiency['lightweight_rate']:.2%}")
        print(f"📜 状态历史: {status['state_history_count']} 次转换")
        print("="*40)
    
    # ============ 日志方法 ============
    
    def _log_info(self, message: str):
        """记录信息日志"""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[STATE_MACHINE] {message}")
    
    def _log_warn(self, message: str):
        """记录警告日志"""
        if self.logger:
            self.logger.warn(message)
        else:
            print(f"[STATE_MACHINE] WARNING: {message}")
    
    def _log_error(self, message: str):
        """记录错误日志"""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"[STATE_MACHINE] ERROR: {message}")


class TrackingStateManager:
    """追踪状态管理器 - 提供更高层的状态管理接口"""
    
    def __init__(self, config: TrackingConfig, logger=None):
        """初始化状态管理器"""
        self.state_machine = TrackingStateMachine(config, logger)
        self.config = config
        self.logger = logger
        
        # 注册默认状态回调
        self._register_default_callbacks()
    
    def _register_default_callbacks(self):
        """注册默认状态回调"""
        self.state_machine.register_state_callback(
            TrackingState.RECOVERY, 
            self._on_recovery_state
        )
        self.state_machine.register_state_callback(
            TrackingState.ERROR, 
            self._on_error_state
        )
    
    def _on_recovery_state(self):
        """回退状态回调"""
        self._log_info("🔧 开始执行回退策略...")
        # 这里后续会调用回退管理器
        print("[RECOVERY] 回退策略执行 - 待实现")
    
    def _on_error_state(self):
        """错误状态回调"""
        self._log_error("❌ 进入错误状态，系统需要人工干预")
        # 这里可以添加错误处理逻辑
        print("[ERROR] 错误处理 - 待实现")
    
    def start_tracking(self, target_id: str, class_id: int) -> bool:
        """开始追踪"""
        try:
            self.state_machine.update_target_info(target_id, class_id)
            success = self.state_machine.transition_to(
                TrackingState.INITIALIZING, 
                f"开始追踪目标: {target_id}"
            )
            
            if success:
                # 继续转换到搜索状态
                success = self.state_machine.transition_to(
                    TrackingState.SEARCHING,
                    "初始化完成，开始搜索"
                )
            
            return success
            
        except Exception as e:
            self._log_error(f"启动追踪失败: {e}")
            return False
    
    def stop_tracking(self) -> bool:
        """停止追踪"""
        try:
            return self.state_machine.transition_to(
                TrackingState.IDLE,
                "手动停止追踪"
            )
        except Exception as e:
            self._log_error(f"停止追踪失败: {e}")
            return False
    
    def process_detection_result(self, detection_found: bool, 
                               detection_mode: TrackingMode = TrackingMode.FULL_MATCHING,
                               distance_xy: float = 0.0,
                               yaw_error: float = 0.0) -> bool:
        """
        处理检测结果
        
        Args:
            detection_found: 是否检测到目标
            detection_mode: 检测模式
            distance_xy: XY距离
            yaw_error: YAW误差
        
        Returns:
            是否处理成功
        """
        try:
            if detection_found:
                self.state_machine.on_detection_success(detection_mode)
                
                # 根据当前状态决定下一步
                if self.state_machine.is_in_state(TrackingState.SEARCHING):
                    # 搜索状态找到目标，切换到追踪
                    self.state_machine.transition_to(
                        TrackingState.TRACKING,
                        "搜索到目标，开始追踪"
                    )
                
                elif self.state_machine.is_in_state(TrackingState.TRACKING):
                    # 检查是否满足逼近条件
                    if self.state_machine.check_approach_conditions(distance_xy, yaw_error):
                        self.state_machine.transition_to(
                            TrackingState.APPROACHING,
                            f"满足逼近条件 (距离:{distance_xy:.1f}mm, yaw:{yaw_error:.1f}°)"
                        )
                
                elif self.state_machine.is_in_state(TrackingState.RECOVERY):
                    # 回退状态重新找到目标
                    self.state_machine.transition_to(
                        TrackingState.TRACKING,
                        "回退后重新找到目标"
                    )
            
            else:
                self.state_machine.on_detection_failed()
            
            return True
            
        except Exception as e:
            self._log_error(f"处理检测结果失败: {e}")
            return False
    
    def trigger_grasp_sequence(self) -> bool:
        """触发抓取序列"""
        try:
            if self.state_machine.is_in_state(TrackingState.APPROACHING):
                return self.state_machine.transition_to(
                    TrackingState.GRASPING,
                    "开始抓取序列"
                )
            else:
                self._log_warn("只能在APPROACHING状态触发抓取")
                return False
        except Exception as e:
            self._log_error(f"触发抓取失败: {e}")
            return False
    
    def complete_grasp(self) -> bool:
        """完成抓取"""
        try:
            return self.state_machine.transition_to(
                TrackingState.RETURNING,
                "抓取完成，开始返回"
            )
        except Exception as e:
            self._log_error(f"完成抓取失败: {e}")
            return False
    
    def complete_task(self) -> bool:
        """完成任务"""
        try:
            return self.state_machine.transition_to(
                TrackingState.IDLE,
                "任务完成"
            )
        except Exception as e:
            self._log_error(f"完成任务失败: {e}")
            return False
    
    # 代理状态机的方法
    def get_current_state(self) -> TrackingState:
        """获取当前状态"""
        return self.state_machine.current_state
    
    def get_current_mode(self) -> TrackingMode:
        """获取当前模式"""
        return self.state_machine.current_mode
    
    def get_status(self) -> Dict[str, Any]:
        """获取状态"""
        return self.state_machine.get_status()
    
    def emergency_stop(self):
        """紧急停止"""
        self.state_machine.emergency_stop()
    
    def reset(self):
        """重置"""
        self.state_machine.reset()
    
    def _log_info(self, message: str):
        """记录信息日志"""
        if self.logger:
            self.logger.info(message)
        else:
            print(f"[STATE_MANAGER] {message}")
    
    def _log_warn(self, message: str):
        """记录警告日志"""
        if self.logger:
            self.logger.warn(message)
        else:
            print(f"[STATE_MANAGER] WARNING: {message}")
    
    def _log_error(self, message: str):
        """记录错误日志"""
        if self.logger:
            self.logger.error(message)
        else:
            print(f"[STATE_MANAGER] ERROR: {message}")


if __name__ == "__main__":
    # 测试状态机
    from ..utils.config import create_tracking_config
    
    config = create_tracking_config()
    state_manager = TrackingStateManager(config)
    
    print("🧪 测试状态机...")
    
    # 测试状态转换
    state_manager.start_tracking("lemon_0", 4)
    state_manager.process_detection_result(True, TrackingMode.FULL_MATCHING, 50.0, 10.0)
    state_manager.process_detection_result(True, TrackingMode.FULL_MATCHING, 25.0, 3.0)
    
    # 打印状态摘要
    state_manager.state_machine.print_status_summary()