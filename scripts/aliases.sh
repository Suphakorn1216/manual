#!/usr/bin/env bash

# ---- ROS2 Environment ----
source /opt/ros/humble/setup.bash
source ~/turtlebot3_ws/install/setup.bash
export ROS_DOMAIN_ID=7
export TURTLEBOT3_MODEL=burger

# ---- Project path (อ้างอิง path repo แบบชัวร์) ----
export TB3_PROJ_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ---- Joystick device (default js2, เปลี่ยนได้) ----
export JOY_DEV=${JOY_DEV:-/dev/input/js2}

# ---- Short commands ----
alias run_joy="ros2 run joy joy_node --ros-args -p dev:=${JOY_DEV}"

# ใช้ config ของระบบ (PS3) ถ้าต้องการ
alias run_teleop="ros2 run teleop_twist_joy teleop_node --ros-args --params-file /opt/ros/humble/share/teleop_twist_joy/config/ps3.config.yaml"

# ใช้ config ของโปรเจค (ของคุณ)
alias go_racing="ros2 run teleop_twist_joy teleop_node --ros-args --params-file ${TB3_PROJ_DIR}/config/my_teleop.yaml --remap __node:=teleop_node"
