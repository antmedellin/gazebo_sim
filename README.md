# Gazebo Simulation Project

This project provides a ROS 2 and Gazebo simulation environment for robotic applications.

## Prerequisites

- Docker
- VS Code with Dev Containers extension

## Quick Start

### Building the Docker Image

To build the Docker image for this project:

```bash
docker build -t ros_and_gazebo .
```

### Development Environment

This project is configured to run in a VS Code dev container. Simply:

1. Open the project in VS Code
2. When prompted, click "Reopen in Container"
3. The container will automatically start with the Gazebo simulation

## ROS 2 Workspace Setup

If you need to manually set up the ROS 2 workspace, run the following commands from the project root directory (/workspaces/gazebo_sim):

```bash
rosdep update
rosdep install -i --from-path src --rosdistro humble -y
colcon build 
. install/setup.bash
```

## Documentation References

- **Gazebo Robot Building Tutorial**: [Building a Robot in Gazebo](https://gazebosim.org/docs/harmonic/building_robot/)
- **ROS 2 C++ Publisher/Subscriber Tutorial**: [Writing a Simple C++ Publisher and Subscriber](https://docs.ros.org/en/foxy/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Cpp-Publisher-And-Subscriber.html)

## Project Structure

```
gazebo_sim/
├── .devcontainer/          # VS Code dev container configuration
├── src/
│   └── gazebo_files/
│       └── building_robot.sdf  # Robot simulation definition
├── Dockerfile              # Container setup
└── README.md               # This file
```

## Running the Simulation

The simulation automatically starts when the dev container launches. The robot model is defined in `src/gazebo_files/building_robot.sdf` and will be loaded into Gazebo Sim.

The command is
```
 gz sim /workspaces/gazebo_sim/src/gazebo_files/building_robot.sdf
```

## Development Notes

- ROS 2 Humble is used as the base distribution
- Gazebo Harmonic is included for simulation
- The dev container is configured to automatically source the ROS 2 environment