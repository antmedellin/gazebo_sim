#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
 

    # Joint State Publisher - converts joint commands to joint states for RViz
    # This node will subscribe to joint_commands and publish to /joint_states
    joint_state_converter = Node(
        package='sample_arm',
        executable='joint_state_converter',
        name='joint_state_converter',
        output='screen'
    )

    # GUI Node
    arm_gui = Node(
        package='sample_arm',
        executable='gui_servo',
        name='robot_gui',
        output='screen'
    )
    
    # TCP Joint Publisher Node
    tcp_joint_publisher = Node(
        package='sample_arm',
        executable='tcp_joint_publisher',
        name='tcp_joint_publisher',
        output='screen'
    )
    
 
    
    return LaunchDescription([
  
        joint_state_converter,
        arm_gui,
        tcp_joint_publisher,
        # rviz_node,
    ])
