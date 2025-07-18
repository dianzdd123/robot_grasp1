#!/usr/bin/env python3
"""
追踪系统状态机
管理整个追踪过程的状态转换
"""

import time
from typing import Dict, Optional, Callable
from dataclasses import dataclass
from ..utils.config import TrackingState, TrackingMode, get_config

@dataclass
class StateTransition:
    """状态转换记录"""
    from_state: TrackingState
    to_state: TrackingState
    timestamp: float
    reason: str
    success: bool = True

class TrackingStateMachine:
    """追踪状态机"""
    
    def __init__(self, logger=None):
        self.config = get_config()
        self.logger = logger
        
        # 状态变量
        self.current_state = TrackingState.IDLE
        self.previous_state = TrackingState.IDLE
        self.tracking_mode = TrackingMode.FULL_MATCHING
        
        # 状态历史
        self.state_history = []
        self.transition_count = 0
        
        # 时间戳
        self.state_start_time = time.time()
        self.tracking_start_time = None
        
        # 状态处理回调
        self.state_callbacks: Dict[TrackingState, Callable] = {}
        
        # 错误和重试计数
        self.error_count = 0
        self.max_error_count = 5
        self.recovery_attempts = 0
        
        # 定义有效的状态转换
        self._setup_valid_transitions()
        
        self._log_info("State machine initialized")
    
    def _setup_valid_transitions(self):
        """设置有效的状态转换"""
        self.valid_transitions = {
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
                TrackingState.ERROR,
                TrackingState.IDLE
            ],
            TrackingState.GRASPING: [
                TrackingState.RETURNING,
                TrackingState.ERROR,
                TrackingState.IDLE
            ],
            TrackingState.RETURNING: [
                TrackingState.PLACING,
                TrackingState.ERROR,
                TrackingState.IDLE
            ],
            TrackingState.PLACING: [
                TrackingState.IDLE,
                TrackingState.ERROR
            ],
            TrackingState.RECOVERY: [
                TrackingState.SEARCHING,
                TrackingState.TRACKING,
                TrackingState.ERROR,
                TrackingState.IDLE
            ],
            TrackingState.ERROR: [
                TrackingState.IDLE,
                TrackingState.RECOVERY
            ]
        }
    
    def transition_to(self, new_state: TrackingState, reason: str = "") -> bool:
        """转换到新状态"""
        if not self._is_valid_transition(self.current_state, new_state):
            self._log_error(f"Invalid transition from {self.current_state} to {new_state}")
            return False
        
        # 记录转换
        transition = StateTransition(
            from_state=self.current_state,
            to_state=new_state,
            timestamp=time.time(),
            reason=reason
        )
        
        self.state_history.append(transition)
        self.transition_count += 1
        
        # 更新状态
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_start_time = time.time()
        
        # 特殊状态处理
        if new_state == TrackingState.TRACKING and self.tracking_start_time is None:
            self.tracking_start_time = time.time()
        
        if new_state == TrackingState.IDLE:
            self.tracking_start_time = None
            self.recovery_attempts = 0
            self.error_count = 0
        
        if new_state == TrackingState.RECOVERY:
            self.recovery_attempts += 1
        
        if new_state == TrackingState.ERROR:
            self.error_count += 1
        
        self._log_info(f"State transition: {self.previous_state} → {new_state} ({reason})")
        
        # 执行状态回调
        if new_state in self.state_callbacks:
            try:
                self.state_callbacks[new_state]()
            except Exception as e:
                self._log_error(f"State callback error for {new_state}: {e}")
        
        return True
    
    def _is_valid_transition(self, from_state: TrackingState, to_state: TrackingState) -> bool:
        """检查状态转换是否有效"""
        if from_state not in self.valid_transitions:
            return False
        return to_state in self.valid_transitions[from_state]
    
    def force_transition(self, new_state: TrackingState, reason: str = "Force transition") -> bool:
        """强制转换状态（用于紧急情况）"""
        self._log_info(f"Force transition to {new_state}: {reason}")
        
        # 记录强制转换
        transition = StateTransition(
            from_state=self.current_state,
            to_state=new_state,
            timestamp=time.time(),
            reason=f"FORCE: {reason}",
            success=True
        )
        
        self.state_history.append(transition)
        self.transition_count += 1
        
        # 更新状态
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_start_time = time.time()
        
        return True
    
    def get_state_duration(self) -> float:
        """获取当前状态持续时间"""
        return time.time() - self.state_start_time
    
    def get_tracking_duration(self) -> float:
        """获取追踪总持续时间"""
        if self.tracking_start_time is None:
            return 0.0
        return time.time() - self.tracking_start_time
    
    def can_switch_to_lightweight(self) -> bool:
        """检查是否可以切换到轻量级追踪"""
        if not self.config.lightweight_enable:
            return False
        
        # 必须在TRACKING状态
        if self.current_state != TrackingState.TRACKING:
            return False
        
        # 必须是完整匹配模式
        if self.tracking_mode != TrackingMode.FULL_MATCHING:
            return False
        
        # 状态持续时间足够
        min_duration = self.config.lightweight_continuity_frames / self.config.detection_frequency
        if self.get_state_duration() < min_duration:
            return False
        
        return True
    
    def switch_tracking_mode(self, mode: TrackingMode, reason: str = "") -> bool:
        """切换追踪模式"""
        if mode == self.tracking_mode:
            return True
        
        old_mode = self.tracking_mode
        self.tracking_mode = mode
        
        self._log_info(f"Tracking mode: {old_mode} → {mode} ({reason})")
        return True
    
    def register_state_callback(self, state: TrackingState, callback: Callable) -> None:
        """注册状态回调"""
        self.state_callbacks[state] = callback
        self._log_info(f"Registered callback for state: {state}")
    
    def should_trigger_recovery(self, lost_frames: int) -> bool:
        """判断是否应该触发回退"""
        if lost_frames >= self.config.max_lost_frames:
            return True
        
        # 错误次数过多
        if self.error_count >= self.max_error_count:
            return True
        
        # 在同一状态停留时间过长
        max_state_duration = 30.0  # 30秒
        if self.get_state_duration() > max_state_duration:
            return True
        
        return False
    
    def should_give_up_recovery(self) -> bool:
        """判断是否应该放弃回退"""
        max_recovery_attempts = self.config.recovery_config['max_attempts']
        return self.recovery_attempts >= max_recovery_attempts
    
    def reset(self) -> None:
        """重置状态机"""
        self._log_info("Resetting state machine")
        
        self.current_state = TrackingState.IDLE
        self.previous_state = TrackingState.IDLE
        self.tracking_mode = TrackingMode.FULL_MATCHING
        
        self.state_history.clear()
        self.transition_count = 0
        
        self.state_start_time = time.time()
        self.tracking_start_time = None
        
        self.error_count = 0
        self.recovery_attempts = 0
    
    def get_status(self) -> Dict:
        """获取状态机状态"""
        return {
            'current_state': self.current_state.value,
            'previous_state': self.previous_state.value,
            'tracking_mode': self.tracking_mode.value,
            'state_duration': self.get_state_duration(),
            'tracking_duration': self.get_tracking_duration(),
            'transition_count': self.transition_count,
            'error_count': self.error_count,
            'recovery_attempts': self.recovery_attempts,
            'can_switch_lightweight': self.can_switch_to_lightweight()
        }
    
    def get_state_summary(self) -> str:
        """获取状态摘要"""
        duration = self.get_state_duration()
        mode = self.tracking_mode.value
        return f"{self.current_state.value}({mode}) [{duration:.1f}s]"
    
    def _log_info(self, message: str) -> None:
        """记录信息日志"""
        if self.logger:
            self.logger.info(f"[StateMachine] {message}")
        else:
            print(f"[INFO] [StateMachine] {message}")
    
    def _log_error(self, message: str) -> None:
        """记录错误日志"""
        if self.logger:
            self.logger.error(f"[StateMachine] {message}")
        else:
            print(f"[ERROR] [StateMachine] {message}")

# 测试状态机
if __name__ == "__main__":
    # 创建状态机
    sm = TrackingStateMachine()
    
    # 测试状态转换
    print("Testing state transitions...")
    
    # 正常流程
    sm.transition_to(TrackingState.INITIALIZING, "Start tracking")
    sm.transition_to(TrackingState.SEARCHING, "Initialization complete")
    sm.transition_to(TrackingState.TRACKING, "Target found")
    
    # 打印状态
    print(f"Current state: {sm.get_state_summary()}")
    print(f"Status: {sm.get_status()}")
    
    # 测试轻量级追踪切换
    time.sleep(1)
    print(f"Can switch to lightweight: {sm.can_switch_to_lightweight()}")
    
    # 测试回退
    print(f"Should trigger recovery (0 lost frames): {sm.should_trigger_recovery(0)}")
    print(f"Should trigger recovery (15 lost frames): {sm.should_trigger_recovery(15)}")
    
    print("✅ State machine test completed")