# build docker image
# docker build -t ros_and_gazebo .

# Base image with ROS 2 Humble (you can switch to Galactic or Iron if needed)
FROM ros:humble

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
    ros-humble-desktop \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-moveit \
    ros-humble-xacro \
    ignition-fortress \
    && rm -rf /var/lib/apt/lists/*

RUN curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null 
    
RUN apt-get update && apt-get install gz-harmonic -y


RUN useradd -m developer 

RUN echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer

USER developer

WORKDIR /workspaces

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "source /workspaces/gazebo_sim/install/setup.bash" >> ~/.bashrc


# Set bash as default shell
SHELL ["/bin/bash", "-c"]