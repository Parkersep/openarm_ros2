FROM osrf/ros:jazzy-desktop

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
  ros-jazzy-controller-manager \
  ros-jazzy-gripper-controllers \
  ros-jazzy-hardware-interface \
  ros-jazzy-joint-state-broadcaster \
  ros-jazzy-joint-trajectory-controller \
  ros-jazzy-forward-command-controller \
  ros-jazzy-moveit \
  ros-jazzy-moveit-configs-utils \
  ros-jazzy-moveit-planners \
  ros-jazzy-moveit-ros-move-group \
  ros-jazzy-moveit-ros-planning \
  ros-jazzy-moveit-ros-visualization \
  ros-jazzy-moveit-simple-controller-manager \
  ros-jazzy-xacro \
  ros-jazzy-moveit-py \
  ros-jazzy-joint-state-publisher-gui \
  ros-jazzy-rmw-cyclonedds-cpp \
  ros-jazzy-ros2-controllers \
  git \
  && rm -rf /var/lib/apt/lists/*

# Build topic_based_ros2_control from source (not available as Jazzy apt package)
RUN apt-get update && apt-get install -y ros-jazzy-ros2-control-test-assets && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /topic_based_ws/src && cd /topic_based_ws/src \
  && git clone https://github.com/PickNikRobotics/topic_based_ros2_control.git \
  && cd /topic_based_ws \
  && . /opt/ros/jazzy/setup.sh \
  && colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF \
  && rm -rf /topic_based_ws/src /topic_based_ws/build /topic_based_ws/log

RUN apt-get update && apt-get install -y python3-pip sudo && rm -rf /var/lib/apt/lists/*

# Reuse the existing ubuntu user (UID 1000) and grant sudo
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/ubuntu

# Set up shell sources for the non-root user
RUN echo "source /opt/ros/jazzy/setup.bash" >> /home/ubuntu/.bashrc
RUN echo '[ -f /topic_based_ws/install/setup.bash ] && source /topic_based_ws/install/setup.bash' >> /home/ubuntu/.bashrc
RUN echo '[ -f /open_arm_ws/install/setup.bash ] && source /open_arm_ws/install/setup.bash || (cd /open_arm_ws && colcon build && source /open_arm_ws/install/setup.bash) 2>/dev/null' >> /home/ubuntu/.bashrc

USER ubuntu
WORKDIR /open_arm_ws