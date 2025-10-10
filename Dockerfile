# build docker image
# docker build -t ros_and_gazebo_osrf .

FROM osrf/ros:jazzy-desktop-full

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

# RUN pip install --break-system-packages pyside6

RUN useradd -m developer 

RUN echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer

USER developer

WORKDIR /workspaces

RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
RUN echo "source /workspaces/gazebo_sim/install/setup.bash" >> ~/.bashrc


# Set bash as default shell
SHELL ["/bin/bash", "-c"]