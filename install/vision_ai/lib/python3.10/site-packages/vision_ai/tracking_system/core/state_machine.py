#!/usr/bin/env python3

from enum import Enum
import time
from typing import Dict, Optional, Callable

class TrackingState(Enum):
    IDLE = "IDLE"
    SEARCHING = "SEARCHING"
    TRACKING = "TRACKING" 
    APPROACHING = "APPROACHING"
    GRASPING = "GRASPING"
    COMPLETED = "COMPLETED"
    RECOVERING = "RECOVERING"

class StateMachine:
    """追踪系统状态机"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        
        # 当前状态
        self.current_state = TrackingState.IDLE
        self.previous_state = None
        self.state_start_time = time.time()
        
        # 状态转换规则
        self.transition_rules = self._setup_transition_rules()
        
        # 状态回调函数
        self.state_callbacks = {}
        
        self.logger.info("🎰 StateMachine initialized")
    
    def _setup_transition_rules(self) -> Dict:
        """设置状态转换规则"""
        return {
            TrackingState.IDLE: [
                TrackingState.SEARCHING
            ],
            TrackingState.SEARCHING: [
                TrackingState.TRACKING,
                TrackingState.RECOVERING,
                TrackingState.IDLE
            ],
            TrackingState.TRACKING: [
                TrackingState.APPROACHING,
                TrackingState.RECOVERING,
                TrackingState.IDLE
            ],
            TrackingState.APPROACHING: [
                TrackingState.GRASPING,
                TrackingState.TRACKING,
                TrackingState.RECOVERING,
                TrackingState.IDLE
            ],
            TrackingState.GRASPING: [
                TrackingState.COMPLETED,
                TrackingState.RECOVERING,
                TrackingState.IDLE
            ],
            TrackingState.COMPLETED: [
                TrackingState.IDLE
            ],
            TrackingState.RECOVERING: [
                TrackingState.SEARCHING,
                TrackingState.TRACKING,
                TrackingState.IDLE
            ]
        }
    
    def transition_to(self, new_state: TrackingState, context: Dict = None) -> bool:
        """状态转换"""
        # 检查转换是否合法
        if not self._is_transition_valid(self.current_state, new_state):
            self.logger.warn(f"❌ Invalid transition: {self.current_state.value} → {new_state.value}")
            return False
        
        # 执行转换
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_start_time = time.time()
        
        self.logger.info(f"🔄 State transition: {self.previous_state.value} → {new_state.value}")
        
        # 执行状态回调
        self._execute_state_callback(new_state, context)
        
        return True
    
    def _is_transition_valid(self, from_state: TrackingState, to_state: TrackingState) -> bool:
        """检查状态转换是否有效"""
        allowed_states = self.transition_rules.get(from_state, [])
        return to_state in allowed_states
    
    def _execute_state_callback(self, state: TrackingState, context: Dict = None):
        """执行状态回调函数"""
        callback = self.state_callbacks.get(state)
        if callback:
            try:
                callback(context or {})
            except Exception as e:
                self.logger.error(f"State callback error for {state.value}: {e}")
    
    def register_callback(self, state: TrackingState, callback: Callable):
        """注册状态回调函数"""
        self.state_callbacks[state] = callback
        self.logger.debug(f"📝 Registered callback for state: {state.value}")
    
    def get_state_duration(self) -> float:
        """获取当前状态持续时间"""
        return time.time() - self.state_start_time
    
    def should_transition_based_on_context(self, context: Dict) -> Optional[TrackingState]:
        """基于上下文判断是否应该转换状态"""
        current_distance = context.get('distance_mm', 1000)
        lost_frames = context.get('lost_frames', 0)
        detection_available = context.get('detection_available', False)
        
        # 基于距离的自动转换
        if self.current_state == TrackingState.TRACKING:
            if current_distance <= 180:  # 进入抓取范围
                return TrackingState.APPROACHING
        
        elif self.current_state == TrackingState.APPROACHING:
            if current_distance > 220:  # 离开抓取范围
                return TrackingState.TRACKING
        
        # 基于丢失帧数的转换
        if lost_frames >= self.config.tracking.lost_frame_threshold:
            if self.current_state in [TrackingState.TRACKING, TrackingState.APPROACHING]:
                return TrackingState.RECOVERING
        
        # 基于检测状态的转换
        if self.current_state == TrackingState.SEARCHING and detection_available:
            return TrackingState.TRACKING
        
        return None
    
    def force_transition(self, new_state: TrackingState, reason: str = "Manual"):
        """强制状态转换（紧急情况）"""
        self.logger.warn(f"🚨 Force transition to {new_state.value}: {reason}")
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_start_time = time.time()
    
    def get_status(self) -> Dict:
        """获取状态机状态"""
        return {
            'current_state': self.current_state.value,
            'previous_state': self.previous_state.value if self.previous_state else None,
            'state_duration': self.get_state_duration(),
            'state_start_time': self.state_start_time
        }
    
    def reset(self):
        """重置状态机"""
        self.previous_state = self.current_state
        self.current_state = TrackingState.IDLE
        self.state_start_time = time.time()
        self.logger.info("🔄 StateMachine reset to IDLE")