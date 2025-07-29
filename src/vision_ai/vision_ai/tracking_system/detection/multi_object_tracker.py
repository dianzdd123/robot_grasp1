# multi_object_tracker.py

import numpy as np
import cv2
import math
import os
import json
import itertools
from typing import List, Dict, Any, Optional
from scipy.optimize import linear_sum_assignment
# --- 辅助类：DetectionResult及其嵌套结构 ---
# 这些类直接包含在这里，便于追踪器直接使用。
# 在实际项目中，它们可能位于一个独立的共享模块中。

class MaskInfo:
    """封装SAM2分割后的Mask信息"""
    def __init__(self, data: Dict[str, Any]):
        self.contour_points: List[List[int]] = data.get('contour_points', [])
        self.mask_shape: List[int] = data.get('mask_shape', [0, 0]) # [height, width]
        self.mask_area: int = data.get('mask_area', 0)
        self.min_area_rect: Dict[str, Any] = data.get('min_area_rect', {})
        self.raw_mask_file: Optional[str] = data.get('raw_mask_file')
        self.raw_mask_shape: List[int] = data.get('raw_mask_shape', [0, 0])
        self.raw_mask_dtype: str = data.get('raw_mask_dtype', 'bool')

    def to_mask_image(self) -> np.ndarray:
        """根据contour_points或加载raw_mask_file转换为二值Mask图像"""
        if self.raw_mask_file and os.path.exists(self.raw_mask_file):
            try:
                # 假设 raw_mask_file 存储的是 numpy 数组
                mask = np.load(self.raw_mask_file)
                if mask.shape != tuple(self.mask_shape):
                    mask = cv2.resize(mask.astype(np.uint8), (self.mask_shape[1], self.mask_shape[0])).astype(bool)
                return mask
            except Exception as e:
                print(f"Error loading mask from file {self.raw_mask_file}: {e}")
        
        if self.contour_points and self.mask_shape:
            mask = np.zeros(self.mask_shape, dtype=np.uint8)
            # 确保 contour_points 是标准的 numpy 格式 for cv2.drawContours
            contours_np = [np.array(self.contour_points, dtype=np.int32)]
            cv2.drawContours(mask, contours_np, -1, 255, thickness=cv2.FILLED)
            return mask.astype(bool)
        return np.zeros(self.mask_shape, dtype=bool)

class FeatureInfo:
    """封装颜色、形状、空间和深度特征"""
    def __init__(self, data: Dict[str, Any]):
        self.color: Dict[str, Any] = data.get('color', {})
        self.shape: Dict[str, Any] = data.get('shape', {})
        self.spatial: Dict[str, Any] = data.get('spatial', {})
        self.depth_info: Dict[str, Any] = data.get('depth_info', {})

class DetectionResult:
    """封装单次YOLOv8+SAM2检测的详细结果"""
    def __init__(self, data: Dict[str, Any]):
        self.object_id: str = data.get('object_id', '') # 原始检测可能没有，追踪器会分配
        self.class_id: int = data.get('class_id', -1)
        self.class_name: str = data.get('class_name', '')
        self.confidence: float = data.get('confidence', 0.0)
        self.description: str = data.get('description', '')
        self.bounding_box: List[float] = data.get('bounding_box', [0.0, 0.0, 0.0, 0.0]) # [x_min, y_min, x_max, y_max]
        self.mask_info: MaskInfo = MaskInfo(data.get('mask_info', {}))
        self.features: FeatureInfo = FeatureInfo(data.get('features', {}))

    @property
    def bbox_xywh(self) -> List[float]:
        """将 [x_min, y_min, x_max, y_max] 转换为 [x_center, y_center, width, height]"""
        x_min, y_min, x_max, y_max = self.bounding_box
        width = x_max - x_min
        height = y_max - y_min
        x_center = x_min + width / 2
        y_center = y_min + height / 2
        return [float(x_center), float(y_center), float(width), float(height)]

    @property
    def bbox_xyxy_int(self) -> List[int]:
        """返回整数形式的 [x_min, y_min, x_max, y_max]"""
        return [int(coord) for coord in self.bounding_box]

    @property
    def centroid_2d(self) -> List[float]:
        """获取2D像素坐标系下的质心。优先使用features.spatial中的，否则从bbox计算"""
        return self.features.spatial.get('centroid_2d', self.bbox_xywh[0:2])

    @property
    def hu_moments(self) -> List[float]:
        """获取Hu矩特征"""
        return self.features.shape.get('hu_moments', [])

    @property
    def fourier_descriptors(self) -> List[float]:
        """获取傅里叶描述子特征"""
        return self.features.shape.get('fourier_descriptors', [])

    @property
    def color_histogram(self) -> List[float]:
        """获取颜色直方图特征"""
        return self.features.color.get('histogram', [])

    @property
    def world_coordinates(self) -> List[float]:
        """获取物体在世界坐标系下的位置 [X, Y, Z]"""
        return self.features.spatial.get('world_coordinates', [0.0, 0.0, 0.0])

    @property
    def recommended_gripper_width_mm(self) -> float:
        """获取推荐的夹爪宽度 (毫米)"""
        return self.features.spatial.get('gripper_width_info', {}).get('recommended_gripper_width', 0.0)

    @property
    def gripper_angle(self) -> float:
        """获取推荐的夹爪角度 (度)"""
        return self.features.spatial.get('gripper_width_info', {}).get('angle', 0.0)

# --- 卡尔曼滤波器类 ---
class KalmanFilter:
    """
    一个简单的2D常速卡尔曼滤波器。
    状态向量: [x_center, y_center, vx, vy]T
    观测向量: [x_center, y_center]T
    """
    def __init__(self, initial_bbox_xywh: List[float], dt: float = 1.0):
        self.dt = dt
        
        # 状态转移矩阵 (A)
        self.A = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        # 观测矩阵 (H)
        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], dtype=np.float32)

        # 过程噪声协方差矩阵 (Q) - 描述模型的不确定性，值越大，滤波器越相信观测
        # 需要根据实际应用场景进行调优
        self.Q = np.diag([5., 5., 0.5, 0.5]).astype(np.float32) 

        # 观测噪声协方差矩阵 (R) - 描述观测的不确定性（检测框的噪声），值越大，滤波器越不相信观测
        # 需要根据检测器的精度进行调优
        self.R = np.diag([20., 20.]).astype(np.float32) 

        # 初始状态协方差矩阵 (P) - 初始状态的不确定性
        self.P = np.diag([100., 100., 10., 10.]).astype(np.float32) 

        # 初始状态向量 (x_hat) - [x_center, y_center, vx, vy]
        x_center, y_center, _, _ = initial_bbox_xywh
        self.x_hat = np.array([[x_center], [y_center], [0.0], [0.0]], dtype=np.float32) # 初始速度设为0

    def predict(self) -> np.ndarray:
        """预测下一时刻的状态"""
        self.x_hat = np.dot(self.A, self.x_hat)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        return self.x_hat

    def update(self, z: np.ndarray):
        """用新的观测值更新状态 (z 是观测向量 [x_center, y_center]T)"""
        y = z - np.dot(self.H, self.x_hat)
        S = np.dot(np.dot(self.H, self.P), self.H.T) + self.R
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S)) # 卡尔曼增益

        self.x_hat = self.x_hat + np.dot(K, y)
        self.P = self.P - np.dot(np.dot(K, self.H), self.P)

    def get_predicted_bbox_xywh(self, current_bbox_size: List[float]) -> List[float]:
        """
        获取预测的边界框 (xywh格式)。
        注意：此简单KF不预测w,h，故使用最新的观测尺寸。
        """
        x_center, y_center = self.x_hat[0, 0], self.x_hat[1, 0]
        # 使用最新的检测到的尺寸，或者可以取历史尺寸的平均值
        _, _, width, height = current_bbox_size 
        return [float(x_center), float(y_center), float(width), float(height)]

# --- Track 类 ---
class Track:
    """表示一个被追踪的物体轨迹"""
    _id_counter = itertools.count() # 用于生成唯一的Track ID

    def __init__(self, initial_detection: DetectionResult, dt: float = 1.0):
        self.track_id: int = next(self._id_counter)
        self.class_id: int = initial_detection.class_id
        self.class_name: str = initial_detection.class_name
        self.initial_features: FeatureInfo = initial_detection.features # 初始特征作为参考
        self.current_features: FeatureInfo = initial_detection.features # 当前帧的特征
        
        # 初始化卡尔曼滤波器
        self.kalman_filter: KalmanFilter = KalmanFilter(initial_detection.bbox_xywh, dt)
        
        self.hits: int = 1 # 连续匹配成功的帧数
        self.age: int = 1 # 轨迹的年龄
        self.lost_frames: int = 0 # 连续未匹配的帧数
        
        self.bbox: List[float] = initial_detection.bounding_box # [xmin, ymin, xmax, ymax]
        self.mask_info: MaskInfo = initial_detection.mask_info
        self.confidence: float = initial_detection.confidence

        self.history_bboxes: List[List[float]] = [self.bbox] # 用于可视化或调试
        # 世界坐标信息，会在update时更新
        self.world_coordinates: List[float] = initial_detection.world_coordinates 
        self.recommended_gripper_width_mm: float = initial_detection.recommended_gripper_width_mm
        self.gripper_angle: float = initial_detection.gripper_angle

        print(f"[TRACK] 新轨迹创建: ID {self.track_id}, Class: {self.class_name}, Initial BBox: {self.bbox}")

    def update(self, new_detection: DetectionResult):
        """用新的检测结果更新轨迹"""
        # 更新卡尔曼滤波器状态
        self.kalman_filter.update(np.array([[new_detection.centroid_2d[0]], [new_detection.centroid_2d[1]]]))
        
        # 更新轨迹的视觉和空间信息
        self.bbox = new_detection.bounding_box
        self.mask_info = new_detection.mask_info
        self.current_features = new_detection.features
        self.confidence = new_detection.confidence
        self.world_coordinates = new_detection.world_coordinates 
        self.recommended_gripper_width_mm = new_detection.recommended_gripper_width_mm
        self.gripper_angle = new_detection.gripper_angle

        self.hits += 1
        self.lost_frames = 0 # 重置丢失帧数
        self.history_bboxes.append(self.bbox)

    def predict(self) -> List[float]:
        """
        预测轨迹的下一个边界框 (xyxy格式)。
        注意：卡尔曼滤波器只预测中心点，尺寸使用当前轨迹的尺寸。
        """
        self.kalman_filter.predict()
        # 获取预测的xywh格式，并转换回xyxy
        predicted_bbox_xywh = self.kalman_filter.get_predicted_bbox_xywh(self.bbox_xywh) # self.bbox_xywh是track当前帧的尺寸
        
        x_center, y_center, width, height = predicted_bbox_xywh
        x_min = x_center - width / 2
        y_min = y_center - height / 2
        x_max = x_center + width / 2
        y_max = y_center + height / 2
        return [x_min, y_min, x_max, y_max]

    def mark_lost(self):
        """标记轨迹为丢失一帧，并根据预测更新其位置。"""
        self.lost_frames += 1
        # 在丢失帧中，卡尔曼滤波器依然需要预测，但没有观测更新
        # 更新轨迹的bbox为预测值，以便在没有观测时也能有大致位置
        self.bbox = self.predict() # 使用predict方法更新bbox

    @property
    def bbox_xywh(self) -> List[float]:
        """返回当前bbox的xywh格式"""
        x_min, y_min, x_max, y_max = self.bbox
        width = x_max - x_min
        height = y_max - y_min
        x_center = x_min + width / 2
        y_center = y_min + height / 2
        return [float(x_center), float(y_center), float(width), float(height)]

# --- 多目标追踪器类 ---
# 你原来id_matcher.py的功能将被此替换和增强
class MultiObjectTracker:
    """
    多目标追踪器，管理所有活跃的Track，进行预测、数据关联和轨迹更新。
    需要一个配置对象 (例如 TrackingConfig) 来获取阈值和权重。
    """
    def __init__(self, config: Any): # 使用Any因为TrackingConfig可能未在此文件定义
        self.config = config
        self.active_tracks: Dict[int, Track] = {}
        self.max_lost_frames = self.config.get_max_lost_frames() # 从配置中获取最大丢失帧数
        self.feature_weights = self.config.get_feature_weights()
        self.match_threshold = self.config.get_feature_match_threshold()

    def _iou(self, box1: List[float], box2: List[float]) -> float:
        """
        计算两个边界框的 IoU (Intersection over Union)。
        box: [x_min, y_min, x_max, y_max]
        """
        x1_min, y1_min, x1_max, y1_max = box1
        x2_min, y2_min, x2_max, y2_max = box2

        xi1 = max(x1_min, x2_min)
        yi1 = max(y1_min, y2_min)
        xi2 = min(x1_max, x2_max)
        yi2 = min(y1_max, y2_max)

        inter_width = max(0, xi2 - xi1)
        inter_height = max(0, yi2 - yi1)
        inter_area = inter_width * inter_height

        box1_area = (x1_max - x1_min) * (y1_max - y1_min)
        box2_area = (x2_max - x2_min) * (y2_max - y2_min)

        union_area = box1_area + box2_area - inter_area
        
        return inter_area / union_area if union_area > 0 else 0.0

    def _hu_moments_similarity(self, hu_moments1: List[float], hu_moments2: List[float]) -> float:
        """
        计算两个Hu矩之间的相似度（使用对数变换和欧氏距离）。
        相似度越高，值越大。
        """
        if not hu_moments1 or not hu_moments2 or len(hu_moments1) != len(hu_moments2):
            return 0.0

        # 对Hu矩进行对数变换，使其对尺度和旋转更鲁棒
        hu1_log = [-math.copysign(1.0, m) * math.log(abs(m)) if abs(m) > 0 else 0.0 for m in hu_moments1]
        hu2_log = [-math.copysign(1.0, m) * math.log(abs(m)) if abs(m) > 0 else 0.0 for m in hu_moments2]

        distance = np.linalg.norm(np.array(hu1_log) - np.array(hu2_log))
        
        # 将距离转换为相似度 (0到1，1表示完全相似)
        # 这里的 max_possible_distance 是一个经验值，需要根据实际数据调优
        max_possible_distance = 100.0 
        similarity = max(0.0, 1.0 - (distance / max_possible_distance))
        return similarity

    def _color_histogram_similarity(self, hist1: List[float], hist2: List[float]) -> float:
        """
        计算两个颜色直方图之间的相似度（使用巴氏距离）。
        相似度越高，值越大。
        """
        if not hist1 or not hist2 or len(hist1) != len(hist2):
            return 0.0
        
        hist1_np = np.array(hist1, dtype=np.float32)
        hist2_np = np.array(hist2, dtype=np.float32)

        distance = cv2.compareHist(hist1_np, hist2_np, cv2.HISTCMP_BHATTACHARYYA)
        
        # 巴氏距离在 0 到 1 之间，0表示完全匹配，1表示完全不匹配
        similarity = 1.0 - distance
        return similarity

    def _fourier_descriptors_similarity(self, fd1: List[float], fd2: List[float]) -> float:
        """
        计算两个傅里叶描述子之间的相似度（使用欧氏距离）。
        相似度越高，值越大。
        """
        if not fd1 or not fd2 or len(fd1) != len(fd2):
            return 0.0

        distance = np.linalg.norm(np.array(fd1) - np.array(fd2))

        # 这里的 max_possible_distance 是一个经验值，需要根据实际数据调优
        max_possible_distance = 10.0 
        similarity = max(0.0, 1.0 - (distance / max_possible_distance))
        return similarity

    def _calculate_total_similarity(self, detection: DetectionResult, track: Track) -> float:
        """
        计算DetectionResult和Track之间的综合相似度。
        结合了IoU和各种特征相似度，并使用配置中的权重。
        """
        # 类别不匹配直接返回0相似度
        if detection.class_id != track.class_id:
            return 0.0

        # 获取权重，如果配置中没有，则使用默认值
        weights = {
            'class_id': self.feature_weights.get('class_id', 1.0),
            'iou': self.feature_weights.get('iou', 0.5), # 确保你的配置文件中增加了 'iou' 权重
            'hu_moments': self.feature_weights.get('hu_moments', 0.5),
            'color_histogram': self.feature_weights.get('color_histogram', 0.5),
            'fourier_descriptors': self.feature_weights.get('fourier_descriptors', 0.5),
            'spatial_continuity': self.feature_weights.get('spatial_continuity', 0.2)
        }

        # IoU 相似度
        # 注意这里使用track的当前bbox进行IoU计算，更侧重于几何重叠，而不是预测框
        iou_score = self._iou(track.bbox, detection.bounding_box) 

        # 特征相似度
        hu_sim = self._hu_moments_similarity(detection.hu_moments, track.current_features.shape.get('hu_moments', []))
        color_sim = self._color_histogram_similarity(detection.color_histogram, track.current_features.color.get('histogram', []))
        fourier_sim = self._fourier_descriptors_similarity(detection.fourier_descriptors, track.current_features.shape.get('fourier_descriptors', []))

        # 空间连续性 (基于预测位置与检测位置的距离)
        # 用预测的中心点和检测到的中心点计算距离，距离越小，相似度越高
        predicted_bbox_xywh = track.kalman_filter.get_predicted_bbox_xywh(track.bbox_xywh)
        predicted_xy = np.array(predicted_bbox_xywh[0:2])
        detection_xy = np.array(detection.bbox_xywh[0:2])
        
        distance_2d = np.linalg.norm(predicted_xy - detection_xy)
        
        spatial_continuity_threshold = self.config.detection_params.get('spatial_continuity_threshold', 100.0) # 像素阈值
        spatial_sim = max(0.0, 1.0 - (distance_2d / spatial_continuity_threshold))
        
        # 综合加权得分
        total_similarity = (
            weights['class_id'] * (1.0 if detection.class_id == track.class_id else 0.0) +
            weights['iou'] * iou_score + 
            weights['hu_moments'] * hu_sim +
            weights['color_histogram'] * color_sim +
            weights['fourier_descriptors'] * fourier_sim +
            weights['spatial_continuity'] * spatial_sim
        )
        
        # 归一化总权重 (防止权重和不为1)
        total_weight = sum(weights.values())
        if total_weight > 0:
            total_similarity /= total_weight
        
        return total_similarity

    def update_tracks(self, current_detections: List[DetectionResult]) -> List[Track]:
        """
        更新所有活跃轨迹，并处理新的检测结果。
        这是追踪器的核心方法。
        返回当前帧所有活跃的Track对象。
        """
        # 1. 预测现有轨迹的下一帧位置
        # 对每个活跃轨迹调用predict，更新其卡尔曼滤波器和预测的bbox
        for track_id in list(self.active_tracks.keys()): # 遍历副本以允许在循环中删除
            track = self.active_tracks[track_id]
            track.predict() # 卡尔曼滤波器预测状态，并更新track的bbox为预测值
            track.age += 1 # 轨迹年龄增加

        # 2. 构建代价矩阵
        # 行：现有轨迹 (预测后的位置)
        # 列：当前帧检测
        num_tracks = len(self.active_tracks)
        num_detections = len(current_detections)
        
        # 如果没有活跃轨迹或没有新的检测，直接处理
        if num_tracks == 0 and num_detections == 0:
            return []
        if num_tracks == 0: # 只有新检测
            for detection in current_detections:
                new_track = Track(initial_detection=detection)
                self.active_tracks[new_track.track_id] = new_track
            print(f"[TRACKER] 无活跃轨迹，创建 {len(current_detections)} 个新轨迹。")
            return list(self.active_tracks.values())
        if num_detections == 0: # 只有活跃轨迹，全部标记为丢失
            for track_id in list(self.active_tracks.keys()):
                track = self.active_tracks[track_id]
                track.mark_lost()
                if track.lost_frames > self.max_lost_frames:
                    print(f"[TRACKER] 轨迹 {track.track_id} 丢失超过 {self.max_lost_frames} 帧，已移除。")
                    del self.active_tracks[track_id]
            print(f"[TRACKER] 无新检测，{len(self.active_tracks)} 个轨迹可能丢失。")
            return list(self.active_tracks.values())

        cost_matrix = np.full((num_tracks, num_detections), 1.0) # 初始代价设为1.0 (最大不相似度)
        track_list = list(self.active_tracks.values()) # 转换为列表以便索引

        for i, track in enumerate(track_list):
            for j, detection in enumerate(current_detections):
                similarity = self._calculate_total_similarity(detection, track)
                # 将相似度转换为代价：1.0 - 相似度，代价越小越好
                cost_matrix[i, j] = 1.0 - similarity
        
        # 3. 使用匈牙利算法进行数据关联
        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        matched_tracks_indices = [] # 记录被匹配的轨迹在 track_list 中的索引
        matched_detections_indices = [] # 记录被匹配的检测在 current_detections 中的索引

        # 4. 处理匹配结果
        for i, j in zip(row_ind, col_ind):
            # 只有当匹配代价低于 (1.0 - 阈值) 时，才认为是有效匹配
            if cost_matrix[i, j] <= (1.0 - self.match_threshold): 
                track = track_list[i]
                detection = current_detections[j]
                track.update(detection) # 用新的观测更新轨迹状态
                matched_tracks_indices.append(i)
                matched_detections_indices.append(j)
            else:
                pass # 匹配代价过高，视为未匹配

        # 5. 处理未匹配的轨迹 (丢失或暂时隐藏)
        for i, track in enumerate(track_list):
            if i not in matched_tracks_indices:
                track.mark_lost() # 标记轨迹为丢失一帧
                if track.lost_frames > self.max_lost_frames:
                    print(f"[TRACKER] 轨迹 {track.track_id} 丢失超过 {self.max_lost_frames} 帧，已移除。")
                    del self.active_tracks[track.track_id]
                # 否则，轨迹保留在 active_tracks 中，其位置是预测值

        # 6. 处理未匹配的新检测 (新物体)
        for j, detection in enumerate(current_detections):
            if j not in matched_detections_indices:
                # 创建新轨迹
                new_track = Track(initial_detection=detection)
                self.active_tracks[new_track.track_id] = new_track
        
        print(f"[TRACKER] 当前活跃轨迹数量: {len(self.active_tracks)}")
        # 返回所有当前活跃的轨迹对象
        return list(self.active_tracks.values())