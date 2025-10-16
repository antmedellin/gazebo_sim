#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, Float64
from sensor_msgs.msg import JointState
from builtin_interfaces.msg import Time


class JointStateConverter(Node):
    def __init__(self):
        super().__init__('joint_state_converter')
        
        # Subscribe to joint commands from GUI
        self.joint_cmd_sub = self.create_subscription(
            Float64MultiArray,
            'joint_commands',
            self.joint_command_callback,
            10
        )
        
        self.gripper_cmd_sub = self.create_subscription(
            Float64,
            'gripper_command',
            self.gripper_command_callback,
            10
        )
        
        # Publisher for joint states (used by robot_state_publisher for RViz)
        self.joint_state_pub = self.create_publisher(JointState, 'joint_states', 10)
        
        # Store current joint positions
        self.joint_positions = [0.0, 0.0, 0.0, 0.0]  # joint1, joint2, joint3, joint4
        self.gripper_position = 0.0
        
        # Timer to publish joint states at regular intervals
        self.timer = self.create_timer(0.05, self.publish_joint_states)  # 20Hz
        
        self.get_logger().info('Joint State Converter node started')
    
    def joint_command_callback(self, msg):
        """Receive joint commands and update internal state"""
        if len(msg.data) >= 4:
            self.joint_positions = list(msg.data[:4])
    
    def gripper_command_callback(self, msg):
        """Receive gripper command and update internal state"""
        # Convert gripper value (0.0 to 1.0) to prismatic joint positions
        # Map to the gripper joint limits: 0.01 to 0.05 meters
        self.gripper_position = 0.01 + (msg.data * 0.04)
    
    def publish_joint_states(self):
        """Publish joint states for RViz visualization"""
        joint_state = JointState()
        
        # Set timestamp
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.header.frame_id = ''
        
        # Define joint names matching the URDF
        joint_state.name = [
            'joint1',
            'joint2',
            'joint3',
            'joint4',
            'gripper_joint1',
            'gripper_joint2'
        ]
        
        # Set joint positions
        joint_state.position = [
            self.joint_positions[0],
            self.joint_positions[1],
            self.joint_positions[2],
            self.joint_positions[3],
            self.gripper_position,
            self.gripper_position
        ]
        
        # Set velocities and efforts (optional, can be empty)
        joint_state.velocity = []
        joint_state.effort = []
        
        # Publish
        self.joint_state_pub.publish(joint_state)


def main(args=None):
    rclpy.init(args=args)
    node = JointStateConverter()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
