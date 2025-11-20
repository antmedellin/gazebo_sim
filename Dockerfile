# build docker image
# docker build -t ros_and_gazebo_ros_img .
# docker build --build-arg HOST_UID=$(id -u) -t ros_and_gazebo_ros_img .



# FROM osrf/ros:jazzy-desktop-full
FROM ros:jazzy

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt upgrade -y

RUN apt install -y \
    git \
    build-essential \
    wget \
    unzip \
    pkg-config \
    cmake \
    pip \
    sudo \
    g++ \
    ca-certificates \
    htop \
    nano 

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    lsb-release \
    gnupg \
    gnupg2 \
    python3-colcon-common-extensions \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --break-system-packages pyside6 pyserial

# Add Gazebo (OSRF) apt repository and install Gazebo Harmonic
RUN curl -fsSL https://packages.osrfoundation.org/gazebo.gpg -o /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" > /etc/apt/sources.list.d/gazebo-stable.list \
    && apt-get update \
    && apt-get install -y \
        gz-harmonic \
        ros-jazzy-ros-gz-bridge \
        ros-jazzy-ros-gz-sim \
        ros-jazzy-rviz2 \
        ros-jazzy-robot-state-publisher \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m developer 


RUN echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer

USER developer

WORKDIR /workspaces

RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
RUN echo "source /workspaces/gazebo_sim/install/setup.bash" >> ~/.bashrc


# Set bash as default shell
SHELL ["/bin/bash", "-c"]