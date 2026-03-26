# ROS2 Jazzy Container Cheatsheet

## Start Container

```bash
cd ~/VLA_MODEL/openarm_isaac_lab/docker
docker compose up -d ros2-jazzy
docker exec -it ros2-jazzy bash
```

## Inside Container

### Source Workspace (do this every new shell)

```bash
source /opt/ros/jazzy/setup.bash
source /open_arm_ws/install/setup.bash
```

### Build Workspace (after first start or changes)

```bash
cd /open_arm_ws
colcon build --packages-skip openarm_hardware
source /open_arm_ws/install/setup.bash
```

### Launch MoveIt Demo (bimanual)

```bash
# With fake hardware (standalone simulation, Plan & Execute works)
ros2 launch openarm_bimanual_moveit_config demo.launch.py use_fake_hardware:=true

# With topic-based control (for Isaac Sim bridge)
# Publishes commands to /isaac_joint_commands, reads state from /isaac_joint_states
ros2 launch openarm_bimanual_moveit_config demo.launch.py use_topic_based:=true

# With real hardware (requires CAN bus connection)
ros2 launch openarm_bimanual_moveit_config demo.launch.py
```

### Run Demo Cycle (looping pose sequence for video)

```bash
# Make sure the MoveIt demo launch is running first, then in another terminal:
python3 /open_arm_ws/src/openarm_ros2/openarm_bimanual_moveit_config/scripts/demo_cycle.py
```

### Generate URDFs

```bash
# Bimanual
xacro /open_arm_ws/openarm_description/urdf/robot/v10.urdf.xacro arm_type:=v10 bimanual:=true > /open_arm_ws/openarm_bimanual.urdf

# Unimanual
xacro /open_arm_ws/openarm_description/urdf/robot/v10.urdf.xacro arm_type:=v10 bimanual:=false > /open_arm_ws/openarm_unimanual.urdf
```

### Visualize in RViz

```bash
ros2 launch openarm_description display_openarm.launch.py arm_type:=v10 bimanual:=true
```

## Host Setup (run before starting container)

```bash
xhost +local:root
```

## Rebuild Image (after Dockerfile changes)

```bash
cd ~/VLA_MODEL/openarm_isaac_lab/docker
docker compose build ros2-jazzy
docker compose up -d ros2-jazzy
```
