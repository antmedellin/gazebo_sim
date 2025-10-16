#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Declare arguments
    # world_arg = DeclareLaunchArgument(
    #     'world',
    #     default_value='/workspaces/gazebo_sim/src/gazebo_files/worlds/arm_world.world',
    #     description='Path to the world file'
    # )
    
    # Set Gazebo model path for Gazebo Garden
    # gazebo_model_path = '/workspaces/gazebo_sim/src/gazebo_files/models'
    
    # # Set environment variable for Gazebo Garden
    # set_gz_resource_path = SetEnvironmentVariable(
    #     name='GZ_SIM_RESOURCE_PATH',
    #     value=gazebo_model_path
    # )
    
    # # Gazebo Garden launch with explicit resource path and auto-run
    # gazebo = ExecuteProcess(
    #     cmd=['gz', 'sim', LaunchConfiguration('world'), '--verbose', '-r'],
    #     output='screen',
    #     additional_env={'GZ_SIM_RESOURCE_PATH': gazebo_model_path}
    # )
    
    # Bridge GUI ROS topics to Gazebo Transport joint command topics
    # Requires: sudo apt-get install ros-${ROS_DISTRO}-ros-gz-bridge
    # ros_gz_param_bridge = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     name='ros_gz_parameter_bridge',
    #     output='screen',
    #     arguments=[
    #         # Main controller topics used by the JointPositionController
    #         '/model/simple_arm/joint/joint1/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
    #         '/model/simple_arm/joint/joint2/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
    #         '/model/simple_arm/joint/joint3/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
    #         '/model/simple_arm/joint/joint4/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
    #         '/model/simple_arm/joint/gripper_joint/cmd_pos@std_msgs/msg/Float64@gz.msgs.Double',
    
    #     ]
    # )
    
    # Bridge node to convert GUI commands to Gazebo joint commands
    # arm_bridge = Node(
    #     package='sample_arm',
    #     executable='arm_gazebo_bridge',
    #     name='arm_gazebo_bridge',
    #     output='screen'
    # )
    
    
    urdf_model_path = '/workspaces/gazebo_sim/src/gazebo_files/models/simple_arm/basic_arm.urdf'

    # Read the URDF file
    with open(urdf_model_path, 'r') as urdf_file:
        robot_description_content = urdf_file.read()
    
    # Robot State Publisher - publishes TF transforms from URDF
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description_content,
            'use_sim_time': False
        }]
    )
    
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
        executable='ros_arm_gui',
        name='robot_arm_gui',
        output='screen'
    )
    
    # RViz2 Node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(os.path.dirname(urdf_model_path), 'arm_config.rviz')]
        if os.path.exists(os.path.join(os.path.dirname(urdf_model_path), 'arm_config.rviz'))
        else []
    )
    
    return LaunchDescription([
        # world_arg,
        # set_gz_resource_path,
        # gazebo,
        # ros_gz_param_bridge,
        # arm_bridge,
        robot_state_publisher,
        joint_state_converter,
        arm_gui,
        rviz_node,
    ])
