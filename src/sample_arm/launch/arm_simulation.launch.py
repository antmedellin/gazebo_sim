#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Declare arguments
    world_arg = DeclareLaunchArgument(
        'world',
        default_value='/workspaces/gazebo_sim/src/gazebo_files/worlds/arm_world.world',
        description='Path to the world file'
    )
    
    # Set Gazebo model path for Gazebo Garden
    gazebo_model_path = '/workspaces/gazebo_sim/src/gazebo_files/models'
    
    # Set environment variable for Gazebo Garden
    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=gazebo_model_path
    )
    
    # Gazebo Garden launch with explicit resource path and auto-run
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', LaunchConfiguration('world'), '--verbose', '-r'],
        output='screen',
        additional_env={'GZ_SIM_RESOURCE_PATH': gazebo_model_path}
    )
    
    # Bridge GUI ROS topics to Gazebo Transport joint command topics
    # Requires: sudo apt-get install ros-${ROS_DISTRO}-ros-gz-bridge
    ros_gz_param_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_parameter_bridge',
        output='screen',
        arguments=[
            # Main controller topics used by the JointPositionController
            '/model/simple_arm/joint/joint1/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
            '/model/simple_arm/joint/joint2/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
            '/model/simple_arm/joint/joint3/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
            '/model/simple_arm/joint/joint4/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
            '/model/simple_arm/joint/gripper_joint/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
            
            # # Vehicle control topic
            # '/model/vehicle_blue/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            # publish values 
            # ros2 topic pub /model/vehicle_blue/cmd_vel geometry_msgs/Twist "linear: { x: 0.1 }"
            # see values ros
            # ros2 topic echo /model/vehicle_blue/cmd_vel
            # see values ign 
            #  ign topic -e -t /model/vehicle_blue/cmd_vel
            
            # # Alternate topic names (some worlds/models advertise these)
            # '/simple_arm/joint1/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
            # '/simple_arm/joint2/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
            # '/simple_arm/joint3/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
            # '/simple_arm/joint4/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
        ]
    )
    
    # Bridge node to convert GUI commands to Gazebo joint commands
    arm_bridge = Node(
        package='sample_arm',
        executable='arm_gazebo_bridge',
        name='arm_gazebo_bridge',
        output='screen'
    )
    
    # GUI Node
    arm_gui = Node(
        package='sample_arm',
        executable='ros_arm_gui',
        name='robot_arm_gui',
        output='screen'
    )
    
    return LaunchDescription([
        world_arg,
        set_gz_resource_path,
        gazebo,
        ros_gz_param_bridge,
        arm_bridge,
        arm_gui,
    ])
