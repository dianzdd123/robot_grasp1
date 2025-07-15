import sys
if sys.prefix == '/home/qi/miniconda3/envs/rel_env':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/qi/ros2_ws/install/xarm_controller'
