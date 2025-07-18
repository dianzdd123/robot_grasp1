#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from vision_ai_interfaces.srv import PlanScan
from vision_ai_interfaces.msg import ScanPlan, Waypoint
from geometry_msgs.msg import Point, Pose, Quaternion
import math
import numpy as np

class ScanPlannerNode(Node):
    def __init__(self):
        super().__init__('scan_planner_node')
        
        # 机械臂安全约束
        self.safe_pose = [200, 0, 250, 179, 0, 0]  # mm + deg
        self.workspace_limit = 800  # mm
        self.obstacle_radius = 150  # mm
        self.max_height = 450  # mm，最大扫描高度
        
        # 相机参数 (1280x720)
        self.camera_width = 1280
        self.camera_height = 720
        self.fx = 912.694580078125
        self.fy = 910.309814453125
        
        # 计算FOV
        self.fov_h = 2 * math.atan(self.camera_width / (2 * self.fx))
        self.fov_v = 2 * math.atan(self.camera_height / (2 * self.fy))
        
        # 创建服务
        self.plan_service = self.create_service(
            PlanScan, 
            'plan_scan', 
            self.plan_scan_callback
        )
        
        self.get_logger().info('扫描规划节点已启动')
        self.get_logger().info(f'FOV: {math.degrees(self.fov_h):.1f}° × {math.degrees(self.fov_v):.1f}°')
        # 验证FOV计算
        self.get_logger().info(f'Camera intrinsics verification:')
        self.get_logger().info(f'  fx={self.fx:.1f}, fy={self.fy:.1f}')
        self.get_logger().info(f'  FOV H: {math.degrees(self.fov_h):.1f}°')
        self.get_logger().info(f'  FOV V: {math.degrees(self.fov_v):.1f}°')
        
        # 验证：在1米高度的覆盖范围
        test_height = 1000  # 1米
        coverage_h = 2 * test_height * math.tan(self.fov_h / 2)
        coverage_v = 2 * test_height * math.tan(self.fov_v / 2)
        self.get_logger().info(f'  At 1m height: {coverage_h:.0f}×{coverage_v:.0f}mm coverage')

    def plan_scan_callback(self, request, response):
        """处理扫描规划请求"""
        try:
            # 提取参数
            points = [(p.x, p.y) for p in request.points]
            object_height = request.object_height
            mode = request.mode
            
            self.get_logger().info(f'Planning request: mode={mode}, height={object_height}mm, {len(points)} points')
            
            # 🎯 主入口：计算最佳策略
            best_strategy = self.calculate_scanning_strategies(points, object_height)
            
            # 创建scan_plan消息
            scan_plan = ScanPlan()
            scan_plan.object_height = float(object_height)
            scan_plan.mode = mode
            scan_plan.required_height = float(best_strategy['height'])
            scan_plan.scan_height = float(best_strategy.get('scan_height', best_strategy['height']))
            
            # 设置扫描区域
            for point in request.points:
                scan_plan.scan_region.append(point)
            
            # 根据策略生成路径点
            if best_strategy['points'] == 1:
                # 单点扫描
                scan_plan.strategy = "single_point"
                
                # 计算中心点
                centroid_x = sum(p[0] for p in points) / len(points)
                centroid_y = sum(p[1] for p in points) / len(points)
                yaw = best_strategy['yaw']
                
                waypoint = self.create_waypoint_msg((centroid_x, centroid_y, scan_plan.scan_height, yaw), 0)
                scan_plan.waypoints.append(waypoint)
                
                self.get_logger().info(f'Single-point scan: center({centroid_x:.1f}, {centroid_y:.1f}), height={scan_plan.scan_height:.1f}mm, yaw={yaw:.1f}°')
            else:
                # 多点扫描
                scan_plan.strategy = "multi_point"
                
                # 使用策略中的scan_height而不是重新计算
                waypoint_data = self.calculate_zigzag_path_with_strategy(points, object_height, best_strategy)
                
                for i, wp_data in enumerate(waypoint_data):
                    x, y, yaw = wp_data['position']
                    waypoint = self.create_waypoint_msg((x, y, scan_plan.scan_height, yaw), i)
                    scan_plan.waypoints.append(waypoint)
                
                self.get_logger().info(f'Multi-point scan: {len(scan_plan.waypoints)} waypoints, height={scan_plan.scan_height:.1f}mm, yaw={yaw:.1f}°')
            
            response.success = True
            response.message = f"Planning success: {scan_plan.strategy} strategy, {len(scan_plan.waypoints)} waypoints"
            response.scan_plan = scan_plan
            
        except Exception as e:
            response.success = False
            response.message = f"Planning failed: {str(e)}"
            response.scan_plan = ScanPlan()
            self.get_logger().error(f'Planning error: {e}')
        
        return response
    
    def calculate_fov_from_intrinsics(self):
        """计算FOV（已经在__init__中完成，这里返回度数）"""
        fov_h_deg = math.degrees(self.fov_h)
        fov_v_deg = math.degrees(self.fov_v)
        return fov_h_deg, fov_v_deg

    def create_waypoint_msg(self, position, waypoint_index):
        """Create Waypoint message with verified yaw encoding"""
        waypoint = Waypoint()
        
        if len(position) >= 4:
            x, y, z, yaw = position[:4]
        else:
            x, y, z = position[:3]
            yaw = 0.0
        
        # 设置位姿
        waypoint.pose = Pose()
        waypoint.pose.position.x = float(x)
        waypoint.pose.position.y = float(y) 
        waypoint.pose.position.z = float(z)

        
        # 正确设置yaw到四元数（只绕Z轴旋转）
        yaw_rad = math.radians(yaw)
        waypoint.pose.orientation = Quaternion()
        waypoint.pose.orientation.x = 0.0
        waypoint.pose.orientation.y = 0.0
        waypoint.pose.orientation.z = math.sin(yaw_rad / 2)
        waypoint.pose.orientation.w = math.cos(yaw_rad / 2)
        
        waypoint.waypoint_index = int(waypoint_index)
        waypoint.coverage_rect = []
        
        self.get_logger().info(f'🎯 Waypoint {waypoint_index}: ({x:.1f}, {y:.1f}, {z:.1f}) yaw={yaw:.1f}°')
        
        return waypoint
    
    def analyze_region_geometry(self, coordinates):
        """分析区域几何，返回1280px对齐长边时与Y轴的夹角"""
        points = np.array(coordinates)
        
        try:
            from scipy.spatial import ConvexHull
            hull = ConvexHull(points)
            hull_points = points[hull.vertices]
        except:
            hull_points = points
        
        best_area = float('inf')
        best_orientation = None
        best_dims = None
        
        angles = np.linspace(0, np.pi, 180)
        
        for angle in angles:
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            rotation_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
            rotated_points = hull_points @ rotation_matrix.T
            
            x_min, x_max = np.min(rotated_points[:, 0]), np.max(rotated_points[:, 0])
            y_min, y_max = np.min(rotated_points[:, 1]), np.max(rotated_points[:, 1])
            
            # 注意：由于坐标系定义，这里dim1对应Y方向，dim2对应X方向
            y_dim = x_max - x_min  # Y方向尺寸
            x_dim = y_max - y_min  # X方向尺寸
            area = y_dim * x_dim
            
            if area < best_area:
                best_area = area
                best_orientation = angle
                best_dims = (y_dim, x_dim)  # (Y方向, X方向)
        
        y_dim, x_dim = best_dims
        
        # 确定长边方向和1280px对齐长边的yaw角度
        if y_dim > x_dim:
            # Y方向是长边，1280px对齐Y方向长边的角度
            long_dim, short_dim = y_dim, x_dim
            yaw_for_long_edge = (best_orientation + np.pi/2) % (2*np.pi)  # Y轴角度
        else:
            # X方向是长边，1280px对齐X方向长边的角度  
            long_dim, short_dim = x_dim, y_dim
            yaw_for_long_edge = best_orientation % (2*np.pi)  # X轴角度
        
        # 转换为度数并规范化到[-180, 180]
        yaw_for_long_edge_deg = np.degrees(yaw_for_long_edge)
        if yaw_for_long_edge_deg > 180:
            yaw_for_long_edge_deg -= 360
        
        self.get_logger().info(f'区域几何分析:')
        self.get_logger().info(f'  长边: {long_dim:.1f}mm, 短边: {short_dim:.1f}mm')
        self.get_logger().info(f'  1280px→长边 yaw: {yaw_for_long_edge_deg:.1f}°')
        
        return -yaw_for_long_edge_deg, long_dim, short_dim

    def calculate_scanning_strategies(self, coordinates, object_height):
        """计算扫描策略"""
        
        yaw_for_long_edge, long_dim, short_dim = self.analyze_region_geometry(coordinates)
        
        strategies = []
        fov_h_deg, fov_v_deg = self.calculate_fov_from_intrinsics()
        fov_h_rad = math.radians(fov_h_deg / 2)  # 1280px half-angle
        fov_v_rad = math.radians(fov_v_deg / 2)  # 720px half-angle
        
        # 策略1：1280px对齐长边
        strategy1_yaw = self.find_closest_yaw(yaw_for_long_edge, coordinates)
        
        height1_from_long = (long_dim / 2) / math.tan(fov_h_rad) + object_height
        height1_from_short = (short_dim / 2) / math.tan(fov_v_rad) + object_height
        height1 = max(height1_from_long, height1_from_short)
        
        if height1 <= self.max_height:
            scan_height1, points1 = height1, 1
        else:
            scan_height1 = min(400, height1 - 50)
            effective_height1 = scan_height1 - object_height
            coverage_1280 = 2 * effective_height1 * math.tan(fov_h_rad) * 0.7
            coverage_720 = 2 * effective_height1 * math.tan(fov_v_rad) * 0.7
            
            grid_along_long = max(1, int(np.ceil(long_dim / coverage_1280)))
            grid_along_short = max(1, int(np.ceil(short_dim / coverage_720)))
            points1 = grid_along_long * grid_along_short
        
        strategies.append({
            'name': '1280px→长边',
            'yaw': strategy1_yaw,
            'height': height1,
            'scan_height': scan_height1,
            'points': points1,
            'long_dim': long_dim,
            'short_dim': short_dim,
            'camera_1280_along': 'long'
        })
        # 策略2：1280px对齐短边（长边yaw + 90°）
        yaw_for_short_edge = yaw_for_long_edge + 90
        strategy2_yaw = self.find_closest_yaw(yaw_for_short_edge, coordinates)
        
        height2_from_short = (short_dim / 2) / math.tan(fov_h_rad) + object_height  # 1280px覆盖短边
        height2_from_long = (long_dim / 2) / math.tan(fov_v_rad) + object_height   # 720px覆盖长边
        height2 = max(height2_from_long, height2_from_short)
        
        if height2 <= self.max_height:
            scan_height2, points2 = height2, 1
        else:
            scan_height2 = min(400, height2 - 50)
            effective_height2 = scan_height2 - object_height
            coverage_1280 = 2 * effective_height2 * math.tan(fov_h_rad) * 0.7
            coverage_720 = 2 * effective_height2 * math.tan(fov_v_rad) * 0.7
            
            grid_along_short = max(1, int(np.ceil(short_dim / coverage_1280)))
            grid_along_long = max(1, int(np.ceil(long_dim / coverage_720)))
            points2 = grid_along_short * grid_along_long
        
        strategies.append({
            'name': '1280px→短边',
            'yaw': strategy2_yaw,
            'height': height2,
            'scan_height': scan_height2,
            'points': points2,
            'long_dim': long_dim,
            'short_dim': short_dim,
            'camera_1280_along': 'short'
        })
        
        best_strategy = min(strategies, key=lambda x: (x['points'], x['height']))
        
        self.get_logger().info(f'策略对比:')
        for s in strategies:
            self.get_logger().info(f'  {s["name"]}: {s["points"]}点, yaw={s["yaw"]:.1f}°')
        
        return best_strategy

    def find_closest_yaw(self, target_angle, coordinates):
        """基于机械臂坐标系的yaw角度优化"""
        
        # 计算坐标中心点
        x_coords = [coord[0] for coord in coordinates]  # 前后方向
        y_coords = [coord[1] for coord in coordinates]  # 左右方向
        x_mean = sum(x_coords) / len(x_coords)
        y_mean = sum(y_coords) / len(y_coords)
        
        # 机械臂坐标系象限判断和yaw范围
        if x_mean >= 0 and y_mean <= 0:
            # 第一象限：前右区域
            yaw_range = (-180, 0)
            quadrant = "前右"
        elif x_mean >= 0 and y_mean >= 0:
            # 第二象限：前左区域
            yaw_range = (0, 180)
            quadrant = "前左"
        elif x_mean <= 0 and y_mean >= 0:
            # 第三象限：后左区域
            yaw_range = (0, 180)
            quadrant = "后左"
        else:  # x_mean <= 0 and y_mean <= 0
            # 第四象限：后右区域
            yaw_range = (-180, 0)
            quadrant = "后右"
        
        # 规范化目标角度
        target_angle = target_angle % 360
        if target_angle > 180:
            target_angle -= 360
        
        # 等效角度候选
        equivalent_targets = [
            target_angle,
            target_angle + 180,
            target_angle - 180
        ]
        
        # 去重并规范化
        normalized_targets = []
        for t in equivalent_targets:
            norm_t = t % 360
            if norm_t > 180:
                norm_t -= 360
            if norm_t not in normalized_targets:
                normalized_targets.append(norm_t)
        
        # 选择在yaw范围内的角度
        valid_targets = [t for t in normalized_targets if yaw_range[0] <= t <= yaw_range[1]]
        
        if not valid_targets:
            # 选择最接近范围的角度
            distances = []
            for t in normalized_targets:
                if t < yaw_range[0]:
                    dist = yaw_range[0] - t
                    closest = yaw_range[0]
                elif t > yaw_range[1]:
                    dist = t - yaw_range[1]
                    closest = yaw_range[1]
                else:
                    dist = 0
                    closest = t
                distances.append((dist, closest))
            
            best_yaw = min(distances)[1]
        else:
            # 选择最接近原目标的有效角度
            best_yaw = min(valid_targets, key=lambda x: abs(x - target_angle))
        
        return float(best_yaw)

    def calculate_zigzag_path_with_strategy(self, coordinates, object_height, strategy):
        """基于机械臂坐标系生成路径"""
        scan_height = strategy['scan_height']
        yaw = strategy['yaw']
        long_dim = strategy['long_dim']
        short_dim = strategy['short_dim']
        
        self.get_logger().info(f'生成路径（机械臂坐标系）:')
        self.get_logger().info(f'  扫描高度: {scan_height:.1f}mm')
        self.get_logger().info(f'  Yaw角度: {yaw:.1f}°')
        
        # FOV覆盖计算
        fov_h_deg, fov_v_deg = self.calculate_fov_from_intrinsics()
        fov_h_rad = math.radians(fov_h_deg / 2)
        fov_v_rad = math.radians(fov_v_deg / 2)
        
        effective_height = scan_height - object_height
        coverage_1280 = 2 * effective_height * math.tan(fov_h_rad) * 0.7
        coverage_720 = 2 * effective_height * math.tan(fov_v_rad) * 0.7
        
        # 根据策略分配覆盖范围
        if strategy['camera_1280_along'] == 'long':
            # 1280px覆盖长边，720px覆盖短边
            coverage_along_long = coverage_1280
            coverage_along_short = coverage_720
            grid_1280_dim = long_dim
            grid_720_dim = short_dim
            num_1280 = max(1, int(np.ceil(long_dim / coverage_1280)))
            num_720 = max(1, int(np.ceil(short_dim / coverage_720)))
        else:
            # 1280px覆盖短边，720px覆盖长边  
            coverage_along_long = coverage_720
            coverage_along_short = coverage_1280
            grid_1280_dim = short_dim
            grid_720_dim = long_dim
            num_1280 = max(1, int(np.ceil(short_dim / coverage_1280)))
            num_720 = max(1, int(np.ceil(long_dim / coverage_720)))
        
        self.get_logger().info(f'  网格: {num_720}×{num_1280} (720px×1280px)')
        
        # 区域中心
        points = np.array(coordinates)
        centroid = np.mean(points, axis=0)
        
        # 在相机坐标系中生成网格点
        y_step = grid_1280_dim / num_1280 if num_1280 > 1 else 0
        x_step = grid_720_dim / num_720 if num_720 > 1 else 0
        
        y_start = -grid_1280_dim / 2 + y_step / 2
        x_start = -grid_720_dim / 2 + x_step / 2
        
        path = []
        
        # 蛇形路径
        for i in range(num_720):  # X方向（720px）
            camera_x = x_start + i * x_step
            
            y_range = range(num_1280) if i % 2 == 0 else range(num_1280 - 1, -1, -1)
            
            for j in y_range:  # Y方向（1280px）
                camera_y = y_start + j * y_step
                
                # 从相机坐标系转换到世界坐标系
                yaw_rad = math.radians(yaw)
                cos_yaw = math.cos(yaw_rad)
                sin_yaw = math.sin(yaw_rad)
                
                # 旋转：[x'] = [cos -sin][x]   (逆时针旋转)
                #      [y']   [sin  cos][y]
                world_x = centroid[0] + camera_x * cos_yaw - camera_y * sin_yaw
                world_y = centroid[1] + camera_x * sin_yaw + camera_y * cos_yaw
                
                waypoint = {
                    'position': (world_x, world_y, yaw),
                    'camera_pos': (camera_x, camera_y),
                    'grid_pos': (i, j)
                }
                path.append(waypoint)
                
                self.get_logger().info(f'  WP{len(path)}: 世界({world_x:.1f},{world_y:.1f}) '
                                    f'相机({camera_x:.1f},{camera_y:.1f}) yaw={yaw:.1f}°')
        
        return path
    
def main(args=None):
    rclpy.init(args=args)
    node = ScanPlannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()