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
    # 🆕 窗口4：追踪系统主控制台
    tmux new-window -t vision_ai:4
    tmux send-keys -t vision_ai:4 'echo "🎯 追踪系统主控制台"' Enter
    tmux send-keys -t vision_ai:4 'echo "═══════════════════════════════════════"' Enter
    tmux send-keys -t vision_ai:4 'echo "正在启动追踪节点..."' Enter
    tmux send-keys -t vision_ai:4 'cd ~/ros2_ws && source install/setup.bash' Enter
    tmux send-keys -t vision_ai:4 'echo ""' Enter
    tmux send-keys -t vision_ai:4 'echo "🚀 启动追踪节点..."' Enter
    tmux send-keys -t vision_ai:4 'sleep 2' Enter
    tmux send-keys -t vision_ai:4 'ros2 run vision_ai tracking_node' Enter

    # 右侧分屏：追踪状态监控和控制
    tmux split-window -h -t vision_ai:4
    tmux send-keys -t vision_ai:4.1 'echo "📊 追踪状态监控与控制"' Enter
    tmux send-keys -t vision_ai:4.1 'echo "═══════════════════════════════════════"' Enter
    tmux send-keys -t vision_ai:4.1 'cd ~/ros2_ws && source install/setup.bash' Enter
    tmux send-keys -t vision_ai:4.1 'echo ""' Enter
    tmux send-keys -t vision_ai:4.1 'echo "📋 快捷命令："' Enter
    tmux send-keys -t vision_ai:4.1 'echo "  📊 追踪状态: ros2 topic echo /tracking/status --once"' Enter
    tmux send-keys -t vision_ai:4.1 'echo "  🎮 目标位姿: ros2 topic echo /xarm/target_pose --once"' Enter
    tmux send-keys -t vision_ai:4.1 'echo "  🤏 夹爪控制: ros2 topic echo /xarm/gripper_target --once"' Enter
    tmux send-keys -t vision_ai:4.1 'echo "  🖼️ 可视化流: ros2 topic echo /tracking/visualization --once"' Enter
    tmux send-keys -t vision_ai:4.1 'echo "  🚨 紧急停止: ros2 topic pub /tracking/emergency_stop std_msgs/Empty"' Enter
    tmux send-keys -t vision_ai:4.1 'echo ""' Enter
    tmux send-keys -t vision_ai:4.1 'echo "等待追踪节点启动..."' Enter
    tmux send-keys -t vision_ai:4.1 'sleep 3' Enter
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