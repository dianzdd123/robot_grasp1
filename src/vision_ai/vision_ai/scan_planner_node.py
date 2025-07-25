#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from vision_ai_interfaces.srv import PlanScan
from vision_ai_interfaces.msg import ScanPlan, Waypoint
from geometry_msgs.msg import Point, Pose, Quaternion
import math
import numpy as np

class ScanPlannerNode(Node):
    """
    A ROS2 node for planning scan paths based on input points and object height.
    It calculates optimal scanning strategies (single-point or multi-point)
    considering camera intrinsics, workspace limits, and object geometry.
    """
    def __init__(self):
        super().__init__('scan_planner_node')
    
        # Robot and workspace parameters
        self.safe_pose = [200, 0, 250, 179, 0, 0]  # mm + deg (x, y, z, roll, pitch, yaw)
        self.workspace_limit = 800  # mm
        self.obstacle_radius = 150  # mm
        self.max_height = 450  # mm (Maximum reachable height for scanning)
        
        # Camera parameters (1280x720 resolution)
        self.camera_width = 1280
        self.camera_height = 720
        self.fx = 912.694580078125  # Focal length in pixels (x-axis)
        self.fy = 910.309814453125  # Focal length in pixels (y-axis)
        
        # Calculate Field of View (FOV)
        self.fov_h = 2 * math.atan(self.camera_width / (2 * self.fx)) # Horizontal FOV in radians
        self.fov_v = 2 * math.atan(self.camera_height / (2 * self.fy)) # Vertical FOV in radians
        
        # Create the planning service
        self.plan_service = self.create_service(
            PlanScan, 
            'plan_scan', 
            self.plan_scan_callback
        )
        
        self.get_logger().info('Scan planning node has started.')
        self.get_logger().info(f'FOV: {math.degrees(self.fov_h):.1f}° × {math.degrees(self.fov_v):.1f}°')
        # Verify FOV calculation
        self.get_logger().info(f'Camera intrinsics verification:')
        self.get_logger().info(f'  fx={self.fx:.1f}, fy={self.fy:.1f}')
        self.get_logger().info(f'  FOV H: {math.degrees(self.fov_h):.1f}°')
        self.get_logger().info(f'  FOV V: {math.degrees(self.fov_v):.1f}°')
        
        # Verification: Coverage at 1 meter height
        test_height = 1000  # 1 meter
        coverage_h = 2 * test_height * math.tan(self.fov_h / 2)
        coverage_v = 2 * test_height * math.tan(self.fov_v / 2)
        self.get_logger().info(f'  At 1m height: {coverage_h:.0f}×{coverage_v:.0f}mm coverage')

    def plan_scan_callback(self, request, response):
        """
        Handles scan planning requests.
        Receives a list of points, object height, and mode, then generates a ScanPlan.
        """
        try:
            # Extract parameters from the request
            points = [(p.x, p.y) for p in request.points]
            object_height = request.object_height
            mode = request.mode
            
            self.get_logger().info(f'Planning request: mode={mode}, height={object_height}mm, {len(points)} points')
            
            # 🎯 Main entry point: Calculate the best scanning strategy
            best_strategy = self.calculate_scanning_strategies(points, object_height)
            
            # Create the ScanPlan message
            scan_plan = ScanPlan()
            scan_plan.object_height = float(object_height)
            scan_plan.mode = mode
            scan_plan.required_height = float(best_strategy['height'])
            # Use 'scan_height' from strategy if available, otherwise default to 'height'
            scan_plan.scan_height = float(best_strategy.get('scan_height', best_strategy['height']))
            
            # Set the scan region
            for point in request.points:
                scan_plan.scan_region.append(point)
            
            # Generate waypoints based on the chosen strategy
            if best_strategy['points'] == 1:
                # Single-point scan
                scan_plan.strategy = "single_point"
                
                # Calculate centroid of the input points
                centroid_x = sum(p[0] for p in points) / len(points)
                centroid_y = sum(p[1] for p in points) / len(points)
                yaw = best_strategy['yaw']
                
                # Create a single waypoint for the centroid
                waypoint = self.create_waypoint_msg((centroid_x, centroid_y, scan_plan.scan_height, yaw), 0)
                scan_plan.waypoints.append(waypoint)
                
                self.get_logger().info(f'Single-point scan: center({centroid_x:.1f}, {centroid_y:.1f}), height={scan_plan.scan_height:.1f}mm, yaw={yaw:.1f}°')
            else:
                # Multi-point scan (zigzag path)
                scan_plan.strategy = "multi_point"
                
                # Use scan_height from the strategy, no recalculation needed
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
            response.scan_plan = ScanPlan() # Return an empty ScanPlan on failure
            self.get_logger().error(f'Planning error: {e}')
        
        return response
    
    def calculate_fov_from_intrinsics(self):
        """
        Calculates FOV in degrees (already done in __init__, just returns the values).
        """
        fov_h_deg = math.degrees(self.fov_h)
        fov_v_deg = math.degrees(self.fov_v)
        return fov_h_deg, fov_v_deg

    def create_waypoint_msg(self, position, waypoint_index):
        """
        Creates a Waypoint message with position (x, y, z) and orientation (yaw).
        Yaw is converted to a Quaternion representing rotation around the Z-axis.
        """
        waypoint = Waypoint()
        
        # Extract x, y, z, and yaw from the position tuple
        if len(position) >= 4:
            x, y, z, yaw = position[:4]
        else:
            x, y, z = position[:3]
            yaw = 0.0 # Default yaw if not provided
        
        # Set position
        waypoint.pose = Pose()
        waypoint.pose.position.x = float(x)
        waypoint.pose.position.y = float(y) 
        waypoint.pose.position.z = float(z)

        # Correctly set yaw into a Quaternion (rotation only around Z-axis)
        yaw_rad = math.radians(yaw)
        waypoint.pose.orientation = Quaternion()
        waypoint.pose.orientation.x = 0.0
        waypoint.pose.orientation.y = 0.0
        waypoint.pose.orientation.z = math.sin(yaw_rad / 2)
        waypoint.pose.orientation.w = math.cos(yaw_rad / 2)
        
        waypoint.waypoint_index = int(waypoint_index)
        waypoint.coverage_rect = [] # Placeholder for coverage rectangle, if needed
        
        self.get_logger().info(f'🎯 Waypoint {waypoint_index}: ({x:.1f}, {y:.1f}, {z:.1f}) yaw={yaw:.1f}°')
        
        return waypoint
    
    def analyze_region_geometry(self, coordinates):
        """
        Analyzes the geometry of the input region (a set of 2D points).
        It finds the minimum bounding box and its orientation, returning
        the yaw angle (for aligning the 1280px camera axis with the long edge)
        and the dimensions of the bounding box.
        """
        points = np.array(coordinates)
        
        try:
            # Use ConvexHull for more robust bounding box calculation if scipy is available
            from scipy.spatial import ConvexHull
            hull = ConvexHull(points)
            hull_points = points[hull.vertices]
        except ImportError:
            # Fallback to using all points if scipy is not installed
            self.get_logger().warn('Scipy not found. Using all points for geometry analysis, ConvexHull not applied.')
            hull_points = points
        
        best_area = float('inf')
        best_orientation = None
        best_dims = None
        
        # Iterate through angles to find the minimum area bounding box
        angles = np.linspace(0, np.pi, 180) # 0 to 180 degrees in radians
        
        for angle in angles:
            cos_a, sin_a = np.cos(angle), np.sin(angle)
            # Rotation matrix for rotating points by 'angle'
            rotation_matrix = np.array([[cos_a, -sin_a], [sin_a, cos_a]])
            rotated_points = hull_points @ rotation_matrix.T # Apply rotation
            
            # Find min/max x and y after rotation
            x_min, x_max = np.min(rotated_points[:, 0]), np.max(rotated_points[:, 0])
            y_min, y_max = np.min(rotated_points[:, 1]), np.max(rotated_points[:, 1])
            
            # Note: Due to coordinate system definition, dim1 corresponds to Y-direction, dim2 to X-direction
            # This is based on the rotation logic where X becomes Y and Y becomes X after rotation for bounding box.
            y_dim = x_max - x_min  # Dimension along the rotated Y-axis
            x_dim = y_max - y_min  # Dimension along the rotated X-axis
            area = y_dim * x_dim
            
            # Update best bounding box if current area is smaller
            if area < best_area:
                best_area = area
                best_orientation = angle # Angle of the rotated X-axis with the original X-axis
                best_dims = (y_dim, x_dim)  # (Y-direction dimension, X-direction dimension)
        
        y_dim, x_dim = best_dims
        
        # Determine the long edge direction and the yaw angle for aligning 1280px with the long edge
        if y_dim > x_dim:
            # Y-direction is the long edge, 1280px camera axis aligns with this Y-direction
            long_dim, short_dim = y_dim, x_dim
            # The yaw for the long edge is the angle of the original Y-axis (which is now rotated by best_orientation)
            # plus 90 degrees to align the camera's 1280px axis (which is usually horizontal) with this long edge.
            yaw_for_long_edge = (best_orientation + np.pi/2) % (2*np.pi) 
        else:
            # X-direction is the long edge, 1280px camera axis aligns with this X-direction
            long_dim, short_dim = x_dim, y_dim
            # The yaw for the long edge is simply the best_orientation itself.
            yaw_for_long_edge = best_orientation % (2*np.pi) 
        
        # Convert to degrees and normalize to [-180, 180]
        yaw_for_long_edge_deg = np.degrees(yaw_for_long_edge)
        if yaw_for_long_edge_deg > 180:
            yaw_for_long_edge_deg -= 360
        
        self.get_logger().info(f'Region geometry analysis:')
        self.get_logger().info(f'  Long edge: {long_dim:.1f}mm, Short edge: {short_dim:.1f}mm')
        self.get_logger().info(f'  1280px aligned with long edge yaw: {yaw_for_long_edge_deg:.1f}°')
        
        # Return negative yaw because the rotation matrix used for analysis is for rotating points,
        # but for robot yaw, we need the opposite rotation to align the robot's frame.
        return -yaw_for_long_edge_deg, long_dim, short_dim

    def calculate_scanning_strategies(self, coordinates, object_height):
        """
        Calculates different scanning strategies (e.g., aligning camera with long/short edge)
        and determines the optimal one based on the number of required scan points and height.
        """
        
        yaw_for_long_edge, long_dim, short_dim = self.analyze_region_geometry(coordinates)
        
        strategies = []
        fov_h_deg, fov_v_deg = self.calculate_fov_from_intrinsics()
        fov_h_rad = math.radians(fov_h_deg / 2)  # Half-angle for 1280px (horizontal)
        fov_v_rad = math.radians(fov_v_deg / 2)  # Half-angle for 720px (vertical)
        
        # Strategy 1: Align 1280px camera axis with the long edge of the object
        strategy1_yaw = self.find_closest_yaw(yaw_for_long_edge, coordinates)
        
        # Calculate required height for full coverage
        # Height based on long dimension covered by 1280px FOV
        height1_from_long = (long_dim / 2) / math.tan(fov_h_rad) + object_height
        # Height based on short dimension covered by 720px FOV
        height1_from_short = (short_dim / 2) / math.tan(fov_v_rad) + object_height
        height1 = max(height1_from_long, height1_from_short) # Take the maximum to ensure full coverage
        
        # Determine if single-point or multi-point scan is needed
        if height1 <= self.max_height:
            scan_height1, points1 = height1, 1 # Single point if within max height
        else:
            # If required height is too high, set scan height to a practical limit (e.g., 400mm)
            # and calculate the number of points needed for coverage at that height.
            scan_height1 = min(400, height1 - 50) # Reduce height slightly for safety/clearance
            effective_height1 = scan_height1 - object_height # Actual height above the object
            
            # Calculate coverage at the reduced scan_height (using 70% overlap for safety)
            coverage_1280 = 2 * effective_height1 * math.tan(fov_h_rad) * 0.7 
            coverage_720 = 2 * effective_height1 * math.tan(fov_v_rad) * 0.7
            
            # Calculate grid points needed
            grid_along_long = max(1, int(np.ceil(long_dim / coverage_1280)))
            grid_along_short = max(1, int(np.ceil(short_dim / coverage_720)))
            points1 = grid_along_long * grid_along_short
        
        strategies.append({
            'name': '1280px_along_long_edge',
            'yaw': strategy1_yaw,
            'height': height1, # Required height for full coverage
            'scan_height': scan_height1, # Actual height to scan from
            'points': points1, # Number of scan points
            'long_dim': long_dim,
            'short_dim': short_dim,
            'camera_1280_along': 'long' # Indicates which dimension the 1280px camera axis aligns with
        })

        # Strategy 2: Align 1280px camera axis with the short edge of the object
        # This means the yaw is 90 degrees offset from the long edge alignment.
        yaw_for_short_edge = yaw_for_long_edge + 90
        strategy2_yaw = self.find_closest_yaw(yaw_for_short_edge, coordinates)
        
        # Calculate required height for full coverage (1280px covers short, 720px covers long)
        height2_from_short = (short_dim / 2) / math.tan(fov_h_rad) + object_height  # 1280px covers short dim
        height2_from_long = (long_dim / 2) / math.tan(fov_v_rad) + object_height   # 720px covers long dim
        height2 = max(height2_from_long, height2_from_short)
        
        # Determine if single-point or multi-point scan is needed
        if height2 <= self.max_height:
            scan_height2, points2 = height2, 1
        else:
            scan_height2 = min(400, height2 - 50)
            effective_height2 = scan_height2 - object_height
            coverage_1280 = 2 * effective_height2 * math.tan(fov_h_rad) * 0.7
            coverage_720 = 2 * effective_height2 * math.tan(fov_v_rad) * 0.7
            
            # Grid calculation is swapped for this strategy
            grid_along_short = max(1, int(np.ceil(short_dim / coverage_1280)))
            grid_along_long = max(1, int(np.ceil(long_dim / coverage_720)))
            points2 = grid_along_short * grid_along_long
        
        strategies.append({
            'name': '1280px_along_short_edge',
            'yaw': strategy2_yaw,
            'height': height2,
            'scan_height': scan_height2,
            'points': points2,
            'long_dim': long_dim,
            'short_dim': short_dim,
            'camera_1280_along': 'short'
        })
        
        # Select the best strategy: prioritize fewer points, then lower height
        best_strategy = min(strategies, key=lambda x: (x['points'], x['height']))
        
        self.get_logger().info(f'Strategy comparison:')
        for s in strategies:
            self.get_logger().info(f'  {s["name"]}: {s["points"]} points, yaw={s["yaw"]:.1f}°')
        
        return best_strategy

    def find_closest_yaw(self, target_angle, coordinates):
        """
        Optimizes the yaw angle based on the robot's coordinate system and quadrant.
        It finds the closest valid yaw angle within the robot's reachable range
        for the given target region.
        """
        
        # Calculate the centroid of the input coordinates
        x_coords = [coord[0] for coord in coordinates]  # X-direction (forward/backward)
        y_coords = [coord[1] for coord in coordinates]  # Y-direction (left/right)
        x_mean = sum(x_coords) / len(x_coords)
        y_mean = sum(y_coords) / len(y_coords)
        
        # Determine the quadrant based on the centroid for robot arm's yaw range
        # This assumes specific robot arm kinematics or preferred operating zones.
        if x_mean >= 0 and y_mean <= 0:
            # Quadrant 1: Front-Right area
            yaw_range = (-180, 0)
            quadrant = "Front-Right"
        elif x_mean >= 0 and y_mean >= 0:
            # Quadrant 2: Front-Left area
            yaw_range = (0, 180)
            quadrant = "Front-Left"
        elif x_mean <= 0 and y_mean >= 0:
            # Quadrant 3: Rear-Left area
            yaw_range = (0, 180)
            quadrant = "Rear-Left"
        else:  # x_mean <= 0 and y_mean <= 0
            # Quadrant 4: Rear-Right area
            yaw_range = (-180, 0)
            quadrant = "Rear-Right"
        
        self.get_logger().info(f'Quadrant for yaw optimization: {quadrant} (Centroid: ({x_mean:.1f}, {y_mean:.1f}))')
        self.get_logger().info(f'Allowed yaw range: {yaw_range[0]}° to {yaw_range[1]}°')

        # Normalize the target angle to [-180, 180]
        target_angle = target_angle % 360
        if target_angle > 180:
            target_angle -= 360
        
        self.get_logger().info(f'Normalized target yaw: {target_angle:.1f}°')

        # Generate equivalent angles (e.g., target_angle, target_angle + 180, target_angle - 180)
        # because a 180-degree rotation of the camera can still cover the same area.
        equivalent_targets = [
            target_angle,
            target_angle + 180,
            target_angle - 180
        ]
        
        # Deduplicate and normalize equivalent targets to [-180, 180]
        normalized_targets = []
        for t in equivalent_targets:
            norm_t = t % 360
            if norm_t > 180:
                norm_t -= 360
            if norm_t not in normalized_targets:
                normalized_targets.append(norm_t)
        
        self.get_logger().info(f'Equivalent normalized target yaws: {", ".join([f"{t:.1f}°" for t in normalized_targets])}')

        # Filter for angles that fall within the allowed yaw range for the robot's quadrant
        valid_targets = [t for t in normalized_targets if yaw_range[0] <= t <= yaw_range[1]]
        
        if not valid_targets:
            # If no equivalent target angle is directly within the range,
            # select the closest angle to the range boundaries.
            self.get_logger().warn(f'No valid yaw found within range. Selecting closest boundary.')
            distances = []
            for t in normalized_targets:
                if t < yaw_range[0]:
                    dist = yaw_range[0] - t
                    closest = yaw_range[0]
                elif t > yaw_range[1]:
                    dist = t - yaw_range[1]
                    closest = yaw_range[1]
                else: # Should not happen if valid_targets is empty
                    dist = 0
                    closest = t
                distances.append((dist, closest))
            
            best_yaw = min(distances)[1]
            self.get_logger().info(f'Selected closest yaw: {best_yaw:.1f}°')
        else:
            # If valid targets exist, choose the one closest to the original target_angle
            best_yaw = min(valid_targets, key=lambda x: abs(x - target_angle))
            self.get_logger().info(f'Selected valid yaw closest to target: {best_yaw:.1f}°')
        
        return float(best_yaw)

    def calculate_zigzag_path_with_strategy(self, coordinates, object_height, strategy):
        """
        Generates a zigzag scanning path based on the chosen strategy,
        considering the object's dimensions and camera FOV.
        Waypoints are generated in the robot's (world) coordinate system.
        """
        scan_height = strategy['scan_height']
        yaw = strategy['yaw']
        long_dim = strategy['long_dim']
        short_dim = strategy['short_dim']
        
        self.get_logger().info(f'Generating path (robot arm coordinate system):')
        self.get_logger().info(f'  Scan height: {scan_height:.1f}mm')
        self.get_logger().info(f'  Yaw angle: {yaw:.1f}°')
        
        # FOV coverage calculation
        fov_h_deg, fov_v_deg = self.calculate_fov_from_intrinsics()
        fov_h_rad = math.radians(fov_h_deg / 2) # Half-angle for 1280px (horizontal)
        fov_v_rad = math.radians(fov_v_deg / 2) # Half-angle for 720px (vertical)
        
        effective_height = scan_height - object_height # Height above the object surface
        
        # Calculate camera coverage at the effective height (with 70% overlap)
        coverage_1280 = 2 * effective_height * math.tan(fov_h_rad) * 0.7 
        coverage_720 = 2 * effective_height * math.tan(fov_v_rad) * 0.7
        
        # Assign coverage based on which camera axis (1280px or 720px) aligns with which object dimension
        if strategy['camera_1280_along'] == 'long':
            # 1280px camera axis covers the long dimension, 720px covers the short dimension
            coverage_along_long = coverage_1280
            coverage_along_short = coverage_720
            grid_1280_dim = long_dim # Dimension covered by 1280px FOV
            grid_720_dim = short_dim # Dimension covered by 720px FOV
            # Number of grid points along each dimension
            num_1280 = max(1, int(np.ceil(long_dim / coverage_1280)))
            num_720 = max(1, int(np.ceil(short_dim / coverage_720)))
        else:
            # 1280px camera axis covers the short dimension, 720px covers the long dimension
            coverage_along_long = coverage_720
            coverage_along_short = coverage_1280
            grid_1280_dim = short_dim
            grid_720_dim = long_dim
            num_1280 = max(1, int(np.ceil(short_dim / coverage_1280)))
            num_720 = max(1, int(np.ceil(long_dim / coverage_720)))
        
        self.get_logger().info(f'  Grid: {num_720}×{num_1280} (720px-axis × 1280px-axis)')
        
        # Calculate the centroid of the input points (region center)
        points = np.array(coordinates)
        centroid = np.mean(points, axis=0)
        
        # Generate grid points in the camera's local coordinate system
        # y_step is the step size along the dimension covered by 1280px FOV
        y_step = grid_1280_dim / num_1280 if num_1280 > 1 else 0
        # x_step is the step size along the dimension covered by 720px FOV
        x_step = grid_720_dim / num_720 if num_720 > 1 else 0
        
        # Start positions for the grid (centered)
        y_start = -grid_1280_dim / 2 + y_step / 2
        x_start = -grid_720_dim / 2 + x_step / 2
        
        path = [] # List to store generated waypoints
        
        # Generate zigzag path
        for i in range(num_720):  # Iterate along the X-direction (720px camera axis)
            camera_x = x_start + i * x_step
            
            # Alternate direction for zigzag pattern
            y_range = range(num_1280) if i % 2 == 0 else range(num_1280 - 1, -1, -1)
            
            for j in y_range:  # Iterate along the Y-direction (1280px camera axis)
                camera_y = y_start + j * y_step
                
                # Convert points from camera's local coordinate system to world coordinate system
                yaw_rad = math.radians(yaw)
                cos_yaw = math.cos(yaw_rad)
                sin_yaw = math.sin(yaw_rad)
                
                # Apply rotation (counter-clockwise rotation matrix)
                # [x_world] = [cos_yaw -sin_yaw][camera_x]
                # [y_world]   [sin_yaw  cos_yaw][camera_y]
                world_x = centroid[0] + camera_x * cos_yaw - camera_y * sin_yaw
                world_y = centroid[1] + camera_x * sin_yaw + camera_y * cos_yaw
                
                waypoint = {
                    'position': (world_x, world_y, yaw), # World coordinates and yaw
                    'camera_pos': (camera_x, camera_y), # Camera local coordinates
                    'grid_pos': (i, j) # Grid index
                }
                path.append(waypoint)
                
                self.get_logger().info(f'  WP{len(path)}: World({world_x:.1f},{world_y:.1f}) '
                                    f'Camera({camera_x:.1f},{camera_y:.1f}) yaw={yaw:.1f}°')
        
        return path
    
def main(args=None):
    """
    Main function to initialize and run the ScanPlannerNode.
    """
    rclpy.init(args=args) # Initialize ROS2 client library
    node = ScanPlannerNode() # Create an instance of the node
    rclpy.spin(node) # Keep the node alive and processing callbacks
    node.destroy_node() # Destroy the node gracefully
    rclpy.shutdown() # Shutdown ROS2 client library

if __name__ == '__main__':
    main()