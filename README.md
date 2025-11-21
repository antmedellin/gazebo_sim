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
# rosdep install -i --from-path src --rosdistro jazzy -y
colcon build --symlink-install
source install/setup.bash
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
  ros2 launch sample_arm arm_simulation.launch.py 

```
 <!-- gz sim /workspaces/gazebo_sim/src/gazebo_files/building_robot.sdf -->

## Development Notes

- ROS 2 Jazzy is used as the base distribution
- Gazebo Harmonic is included for simulation
- The dev container is configured to automatically source the ROS 2 environment




## Creating a New Package
To create a new ROS 2 package, use the following command in the src directory:

```
ros2 pkg create --build-type ament_python --license Apache-2.0 {package_name}
```

modify package.xml and setup.py as needed

build a specific package with:
```
colcon build --packages-select {package_name}
```

## Running the Robot Arm GUI
To run the robot arm GUI, use the following command:

```
ros2 run sample_arm ros_arm_gui

```

To launch the full simulation with the robot arm, use:

```
 ros2 launch sample_arm arm_simulation.launch.py 
```

To launch rviz simulation with the robot arm, use:
```
 ros2 launch sample_arm rviz_arm_simulation.launch.py
```

To launch gui only for testing, use:
```
 ros2 launch sample_arm servo_gui.launch.py
```

 python3 src/tcp_joint_listener.py 

