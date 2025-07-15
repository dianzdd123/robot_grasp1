#!/bin/bash

source install/setup.bash

if [ "$1" = "full_system" ]; then
    echo "🚀 Starting full vision AI system with 3D detection..."

    # 创建tmux会话，包含所有必需的窗口
    tmux new-session -d -s vision_ai

    # 窗口0：硬件节点（相机+机械臂）
    tmux send-keys -t vision_ai:0 'ros2 run camera_node realsense_publisher' Enter
    tmux split-window -h -t vision_ai:0
    tmux send-keys -t vision_ai:0.1 'ros2 run xarm_controller xarm_controller' Enter

    # 窗口1：AI处理节点（规划器+执行器）
    tmux new-window -t vision_ai:1
    tmux send-keys -t vision_ai:1 'ros2 run vision_ai scan_planner_node' Enter
    tmux split-window -h -t vision_ai:1
    tmux send-keys -t vision_ai:1.1 'ros2 run vision_ai scan_executor_node' Enter

    # 窗口2：拼接和检测 🆕
    tmux new-window -t vision_ai:2
    tmux send-keys -t vision_ai:2 'ros2 run vision_ai smart_stitcher_node' Enter
    tmux split-window -h -t vision_ai:2
    tmux send-keys -t vision_ai:2.1 'ros2 run vision_ai detection_node' Enter

    # 窗口3：GUI和监控
    tmux new-window -t vision_ai:3
    tmux send-keys -t vision_ai:3 'ros2 run vision_ai gui_config_node' Enter
    tmux split-window -h -t vision_ai:3
    tmux send-keys -t vision_ai:3.1 'echo "📊 监控窗口 - 使用以下命令:"' Enter
    tmux send-keys -t vision_ai:3.1 'echo "ros2 topic echo /detection_result"' Enter
    tmux send-keys -t vision_ai:3.1 'echo "ros2 topic echo /stitching_complete"' Enter
    tmux send-keys -t vision_ai:3.1 'echo "ros2 node list"' Enter
    # 🆕 窗口4：检测结果监控
    tmux new-window -t vision_ai:4
    tmux send-keys -t vision_ai:4 'echo "🧬 检测结果监控窗口"' Enter
    tmux send-keys -t vision_ai:4 'echo "等待检测结果..."' Enter
    tmux send-keys -t vision_ai:4 'echo "可用命令："' Enter
    tmux send-keys -t vision_ai:4 'echo "  ros2 topic echo /detection_result --once"' Enter
    tmux send-keys -t vision_ai:4 'echo "  ros2 service call /execute_scan ..."' Enter
    tmux split-window -h -t vision_ai:4
    tmux send-keys -t vision_ai:4.1 'ros2 topic list | grep -E "(detection|stitching)"' Enter
    # 🆕 窗口5：跟踪
    tmux new-window -t vision_ai:5
    tmux send-keys -t vision_ai:5 'echo "🎯 追踪系统"' Enter
    tmux send-keys -t vision_ai:5 'echo "启动追踪节点..."' Enter
    tmux send-keys -t vision_ai:5 'cd ~/ros2_ws && source install/setup.bash' Enter
    tmux send-keys -t vision_ai:5 'ros2 run vision_ai tracking_node' Enter
    tmux split-window -h -t vision_ai:5
    tmux send-keys -t vision_ai:5.1 'echo "🔍 追踪状态监控"' Enter
    tmux send-keys -t vision_ai:5.1 'echo "可用命令："' Enter
    tmux send-keys -t vision_ai:5.1 'echo "  ros2 topic echo /tracking/status --once"' Enter
    tmux send-keys -t vision_ai:5.1 'echo "  ros2 topic echo /xarm/target_pose --once"' Enter
    tmux send-keys -t vision_ai:5.1 'cd ~/ros2_ws && source install/setup.bash' Enter
    # 🆕 窗口6：实时追踪可视化
    tmux new-window -t vision_ai:6
    tmux send-keys -t vision_ai:6 'echo "📺 实时追踪可视化"' Enter
    tmux send-keys -t vision_ai:6 'cd ~/ros2_ws && source install/setup.bash' Enter
    tmux send-keys -t vision_ai:6 'ros2 run rqt_image_view rqt_image_view /tracking/visualization' Enter
    tmux split-window -h -t vision_ai:6
    tmux send-keys -t vision_ai:6.1 'echo "📊 追踪状态监控"' Enter
    tmux send-keys -t vision_ai:6.1 'cd ~/ros2_ws && source install/setup.bash' Enter
    tmux send-keys -t vision_ai:6.1 'watch -n 1 "ros2 topic echo /tracking/status --once | head -20"' Enter

    # # 窗口7：单窗口图像显示
    # tmux new-window -t vision_ai:7
    # tmux send-keys -t vision_ai:7 'echo "📹 相机图像显示"' Enter
    # tmux send-keys -t vision_ai:7 'cd ~/ros2_ws && source install/setup.bash' Enter
    # tmux send-keys -t vision_ai:7 'ros2 run image_view image_view image:=/camera/color/image_raw' Enter
    # tmux split-window -h -t vision_ai:7
    # tmux send-keys -t vision_ai:7.1 'echo "📊 话题监控"' Enter
    # tmux send-keys -t vision_ai:7.1 'ros2 topic hz /camera/color/image_raw' Enter
    # 连接到会话，默认显示第1个窗口（规划+执行）
    tmux select-window -t vision_ai:1
    tmux attach-session -t vision_ai

elif [ "$1" = "both" ]; then
    echo "🔧 Starting basic nodes with detection..."
    tmux new-session -d -s vision_ai
    tmux send-keys -t vision_ai:0 'ros2 run vision_ai scan_planner_node' Enter
    tmux split-window -h -t vision_ai:0
    tmux send-keys -t vision_ai:0.1 'ros2 run vision_ai gui_config_node' Enter
    # 🆕 添加检测节点到基本模式
    tmux split-window -v -t vision_ai:0
    tmux send-keys -t vision_ai:0.2 'ros2 run vision_ai detection_node' Enter
    tmux attach-session -t vision_ai
else
    echo "Usage: ./dev.sh [both|full_system]"
    echo "  both: Basic nodes (planner + GUI + detection)"
    echo "  full_system: All nodes with hardware + 3D detection"
fi