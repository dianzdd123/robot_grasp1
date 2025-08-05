# utils/data_recorder.py
import os
import json
import cv2
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional

class DataRecorder:
    """追踪数据记录器 - 记录追踪过程和反馈数据"""
    
    def __init__(self, user_id: str, scan_dir: str):
        """
        初始化数据记录器
        
        Args:
            user_id: 用户ID
            scan_dir: 当前扫描目录
        """
        self.user_id = user_id
        self.scan_dir = scan_dir
        
        # 创建数据存储目录
        self.data_dir = os.path.join(scan_dir, 'tracking_data')
        self.images_dir = os.path.join(self.data_dir, 'images')
        self.session_file = os.path.join(self.data_dir, 'tracking_session.json')
        
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        
        # 追踪历史记录
        self.tracking_history = []
        self.session_start_time = datetime.now()
        
        print(f"[DATA_RECORDER] 初始化完成，数据目录: {self.data_dir}")
    
    # def record_tracking_step(self, target_id: str, tracking_result: Dict, 
    #                        rgb_image: np.ndarray, depth_image: np.ndarray):
    #     """
    #     记录单步追踪数据
        
    #     Args:
    #         target_id: 目标ID
    #         tracking_result: 追踪结果
    #         rgb_image: RGB图像
    #         depth_image: 深度图像
    #     """
    #     try:
    #         step_num = len(self.tracking_history) + 1
    #         timestamp = datetime.now()
            
    #         # 保存图像
    #         step_image_dir = os.path.join(self.images_dir, f'step_{step_num:02d}')
    #         os.makedirs(step_image_dir, exist_ok=True)
            
    #         rgb_file = os.path.join(step_image_dir, 'rgb_image.jpg')
    #         depth_file = os.path.join(step_image_dir, 'depth_image.png')
            
    #         # 保存RGB图像
    #         rgb_bgr = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    #         cv2.imwrite(rgb_file, rgb_bgr)
            
    #         # 保存深度图像（可视化版本）
    #         depth_colormap = self._create_depth_colormap(depth_image)
    #         cv2.imwrite(depth_file, depth_colormap)
            
    #         # 保存原始深度数据
    #         depth_raw_file = os.path.join(step_image_dir, 'depth_raw.npy')
    #         np.save(depth_raw_file, depth_image)
            
    #         # 构建记录数据
    #         record = {
    #             'step_number': step_num,
    #             'target_id': target_id,
    #             'timestamp': timestamp.isoformat(),
    #             'tracking_result': self._serialize_tracking_result(tracking_result),
    #             'image_files': {
    #                 'rgb': os.path.relpath(rgb_file, self.data_dir),
    #                 'depth_raw': os.path.relpath(depth_raw_file, self.data_dir)
    #             },
    #             'image_shape': rgb_image.shape,
    #             'human_feedback': None,  # 稍后填入
    #             'feedback_timestamp': None
    #         }
            
    #         self.tracking_history.append(record)
            
    #         print(f"[DATA_RECORDER] 记录第 {step_num} 步追踪数据")
            
    #     except Exception as e:
    #         print(f"[DATA_RECORDER] 记录追踪步骤失败: {e}")
    
    def record_tracking_step(self, target_id: str, tracking_result: Dict, 
                        rgb_image: np.ndarray, depth_image: np.ndarray,
                        detailed_features: Dict = None):
        """
        记录单步追踪数据 - 支持细粒度特征
        """
        try:
            step_num = len(self.tracking_history) + 1
            timestamp = datetime.now()
            
            # 保存图像（现有代码保持不变）
            step_image_dir = os.path.join(self.images_dir, f'step_{step_num:02d}')
            os.makedirs(step_image_dir, exist_ok=True)
            
            rgb_file = os.path.join(step_image_dir, 'rgb_image.jpg')
            depth_file = os.path.join(step_image_dir, 'depth_image.png')
            depth_raw_file = os.path.join(step_image_dir, 'depth_raw.npy')
            
            rgb_bgr = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(rgb_file, rgb_bgr)
            
            depth_colormap = self._create_depth_colormap(depth_image)
            cv2.imwrite(depth_file, depth_colormap)
            np.save(depth_raw_file, depth_image)
            
            # 🆕 构建增强记录数据
            record = {
                'step_number': step_num,
                'target_id': target_id,
                'timestamp': timestamp.isoformat(),
                'tracking_result': self._serialize_tracking_result(tracking_result),
                
                # 🆕 细粒度特征记录
                'detailed_features': detailed_features if detailed_features else {},
                
                # 🆕 抓取条件记录
                'grasp_conditions': tracking_result.get('grasp_conditions', {}),
                
                # 🆕 移动策略记录
                'movement_strategy': tracking_result.get('movement_strategy', {}),
                
                'image_files': {
                    'rgb': os.path.relpath(rgb_file, self.data_dir),
                    'depth_raw': os.path.relpath(depth_raw_file, self.data_dir)
                },
                'image_shape': rgb_image.shape,
                'human_feedback': None,
                'feedback_timestamp': None
            }
            
            self.tracking_history.append(record)
            
            print(f"[DATA_RECORDER] 记录第 {step_num} 步追踪数据 (包含细粒度特征)")
            
        except Exception as e:
            print(f"[DATA_RECORDER] 记录追踪步骤失败: {e}")
    
    def _create_depth_colormap(self, depth_image: np.ndarray) -> np.ndarray:
        """创建深度图像的彩色映射"""
        try:
            # 归一化深度值到0-255范围
            depth_normalized = cv2.normalize(
                depth_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
            )
            
            # 应用颜色映射
            depth_colormap = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_JET)
            
            return depth_colormap
            
        except Exception as e:
            print(f"[DATA_RECORDER] 创建深度颜色映射失败: {e}")
            # 返回灰度图像作为备用
            return cv2.cvtColor(depth_image.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    
    def _serialize_tracking_result(self, tracking_result: Dict) -> Dict:
        """序列化追踪结果，移除不可JSON化的数据"""
        try:
            serialized = {}
            
            # 复制基本数据
            for key, value in tracking_result.items():
                if key in ['target_id', 'detection_confidence', 'tracking_confidence',
                          'match_confidence', 'grasp_coordinate', 'object_info',
                          'timestamp', 'frame_count']:
                    serialized[key] = value
            
            # 处理相似度分解
            if 'similarity_breakdown' in tracking_result:
                serialized['similarity_breakdown'] = tracking_result['similarity_breakdown']
            
            if 'valid_features' in tracking_result:
                serialized['valid_features'] = tracking_result['valid_features']
            
            return serialized
            
        except Exception as e:
            print(f"[DATA_RECORDER] 序列化追踪结果失败: {e}")
            return {'error': str(e)}
    
    def get_tracking_history(self) -> List[Dict]:
        """获取追踪历史记录"""
        return self.tracking_history.copy()
    
    def update_feedback(self, step_number: int, feedback: bool, timestamp: str = None):
        """
        更新指定步骤的反馈
        
        Args:
            step_number: 步骤编号 (1-based)
            feedback: 反馈结果 (True=正确, False=错误)
            timestamp: 反馈时间戳
        """
        try:
            if 1 <= step_number <= len(self.tracking_history):
                step_index = step_number - 1
                self.tracking_history[step_index]['human_feedback'] = 'correct' if feedback else 'incorrect'
                self.tracking_history[step_index]['feedback_timestamp'] = timestamp or datetime.now().isoformat()
                
                print(f"[DATA_RECORDER] 更新步骤 {step_number} 反馈: {'正确' if feedback else '错误'}")
                
            else:
                print(f"[DATA_RECORDER] 无效的步骤编号: {step_number}")
                
        except Exception as e:
            print(f"[DATA_RECORDER] 更新反馈失败: {e}")
    
    def save_session_data(self):
        """保存会话数据到文件"""
        try:
            session_data = {
                'session_info': {
                    'user_id': self.user_id,
                    'scan_directory': self.scan_dir,
                    'start_time': self.session_start_time.isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'total_steps': len(self.tracking_history)
                },
                'tracking_history': self.tracking_history,
                'statistics': self._calculate_session_statistics()
            }
            
            # 保存到JSON文件
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            
            print(f"[DATA_RECORDER] 会话数据已保存: {self.session_file}")
            
            # 创建汇总报告
            self._create_session_summary()
            
        except Exception as e:
            print(f"[DATA_RECORDER] 保存会话数据失败: {e}")
    
    def _calculate_session_statistics(self) -> Dict:
        """计算会话统计信息"""
        try:
            total_steps = len(self.tracking_history)
            if total_steps == 0:
                return {'total_steps': 0}
            
            # 成功/失败统计
            successful_steps = [r for r in self.tracking_history if 'tracking_result' in r]
            failed_steps = [r for r in self.tracking_history if r.get('status') == 'tracking_failed']
            
            # 反馈统计
            feedback_steps = [r for r in self.tracking_history if r.get('human_feedback') is not None]
            correct_feedback = [r for r in feedback_steps if r['human_feedback'] == 'correct']
            
            # 置信度统计
            confidences = []
            for record in successful_steps:
                if 'tracking_result' in record and 'tracking_confidence' in record['tracking_result']:
                    confidences.append(record['tracking_result']['tracking_confidence'])
            
            statistics = {
                'total_steps': total_steps,
                'successful_steps': len(successful_steps),
                'failed_steps': len(failed_steps),
                'success_rate': len(successful_steps) / total_steps if total_steps > 0 else 0,
                'feedback_coverage': len(feedback_steps) / total_steps if total_steps > 0 else 0,
                'human_accuracy': len(correct_feedback) / len(feedback_steps) if feedback_steps else 0,
                'avg_confidence': np.mean(confidences) if confidences else 0,
                'min_confidence': np.min(confidences) if confidences else 0,
                'max_confidence': np.max(confidences) if confidences else 0
            }
            
            return statistics
            
        except Exception as e:
            print(f"[DATA_RECORDER] 计算统计信息失败: {e}")
            return {'error': str(e)}
    
    def _create_session_summary(self):
        """创建可读的会话摘要"""
        try:
            summary_file = os.path.join(self.data_dir, 'session_summary.txt')
            statistics = self._calculate_session_statistics()
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("追踪会话摘要\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"用户ID: {self.user_id}\n")
                f.write(f"扫描目录: {self.scan_dir}\n")
                f.write(f"开始时间: {self.session_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("统计信息:\n")
                f.write("-" * 30 + "\n")
                f.write(f"总步数: {statistics.get('total_steps', 0)}\n")
                f.write(f"成功步数: {statistics.get('successful_steps', 0)}\n")
                f.write(f"失败步数: {statistics.get('failed_steps', 0)}\n")
                f.write(f"成功率: {statistics.get('success_rate', 0):.1%}\n")
                f.write(f"平均置信度: {statistics.get('avg_confidence', 0):.3f}\n")
                f.write(f"人工反馈准确率: {statistics.get('human_accuracy', 0):.1%}\n\n")
                
                f.write("详细步骤:\n")
                f.write("-" * 30 + "\n")
                
                for i, record in enumerate(self.tracking_history, 1):
                    f.write(f"步骤 {i}: ")
                    
                    if 'tracking_result' in record:
                        confidence = record['tracking_result'].get('tracking_confidence', 0)
                        f.write(f"成功 (置信度: {confidence:.3f})")
                    else:
                        f.write("失败")
                    
                    if record.get('human_feedback'):
                        feedback = "✓" if record['human_feedback'] == 'correct' else "✗"
                        f.write(f" - 人工反馈: {feedback}")
                    
                    f.write("\n")
            
            print(f"[DATA_RECORDER] 会话摘要已保存: {summary_file}")
            
        except Exception as e:
            print(f"[DATA_RECORDER] 创建会话摘要失败: {e}")
    
    def load_session_data(self, session_file_path: str) -> Optional[Dict]:
        """
        加载历史会话数据
        
        Args:
            session_file_path: 会话文件路径
            
        Returns:
            Dict: 会话数据，失败返回None
        """
        try:
            if not os.path.exists(session_file_path):
                print(f"[DATA_RECORDER] 会话文件不存在: {session_file_path}")
                return None
            
            with open(session_file_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            print(f"[DATA_RECORDER] 成功加载会话数据: {session_file_path}")
            return session_data
            
        except Exception as e:
            print(f"[DATA_RECORDER] 加载会话数据失败: {e}")
            return None