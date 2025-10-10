#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, Float64
from sensor_msgs.msg import JointState
import threading

class ArmGazeboBridge(Node):
    def __init__(self):
        super().__init__('arm_gazebo_bridge')
        
        # Subscribers to GUI topics
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
        
        # Publishers to Gazebo Garden joint position controllers (matching SDF topics)
        self.joint1_pub = self.create_publisher(Float64, '/model/simple_arm/joint/joint1/cmd_pos', 10)
        self.joint2_pub = self.create_publisher(Float64, '/model/simple_arm/joint/joint2/cmd_pos', 10)
        self.joint3_pub = self.create_publisher(Float64, '/model/simple_arm/joint/joint3/cmd_pos', 10)
        self.joint4_pub = self.create_publisher(Float64, '/model/simple_arm/joint/joint4/cmd_pos', 10)
        self.gripper_pub = self.create_publisher(Float64, '/model/simple_arm/joint/gripper_joint/cmd_pos', 10)
        
        # Subscribe to Gazebo joint state and republish as standard ROS2 JointState
        self.gazebo_joint_state_sub = self.create_subscription(
            JointState,
            '/model/simple_arm/joint_state',
            self.gazebo_joint_state_callback,
            10
        )
        
        # Publisher for standard ROS2 joint state
        self.joint_state_pub = self.create_publisher(JointState, '/joint_states', 10)
        
        # # Also try alternative topic names that Gazebo might use
        # self.alt_joint1_pub = self.create_publisher(Float64, '/simple_arm/joint1/cmd_pos', 10)
        # self.alt_joint2_pub = self.create_publisher(Float64, '/simple_arm/joint2/cmd_pos', 10)
        # self.alt_joint3_pub = self.create_publisher(Float64, '/simple_arm/joint3/cmd_pos', 10)
        # self.alt_joint4_pub = self.create_publisher(Float64, '/simple_arm/joint4/cmd_pos', 10)
        
        # Store current commands
        self.current_joint_commands = [0.0, 0.0, 0.0, 0.0]
        self.current_gripper_command = 0.0
        
        self.get_logger().info('Arm Gazebo Bridge node started')
    
    def joint_command_callback(self, msg):
        """Convert GUI joint commands to individual Gazebo joint topics"""
        if len(msg.data) >= 4:
            self.current_joint_commands = list(msg.data)
            
            # Publish to individual joint position controllers (try multiple topic formats)
            joint1_msg = Float64()
            joint1_msg.data = self.current_joint_commands[0]
            self.joint1_pub.publish(joint1_msg)
            # self.alt_joint1_pub.publish(joint1_msg)
            
            joint2_msg = Float64()
            joint2_msg.data = self.current_joint_commands[1]
            self.joint2_pub.publish(joint2_msg)
            # self.alt_joint2_pub.publish(joint2_msg)
            
            joint3_msg = Float64()
            joint3_msg.data = self.current_joint_commands[2]
            self.joint3_pub.publish(joint3_msg)
            # self.alt_joint3_pub.publish(joint3_msg)
            
            joint4_msg = Float64()
            joint4_msg.data = self.current_joint_commands[3]
            self.joint4_pub.publish(joint4_msg)
            # self.alt_joint4_pub.publish(joint4_msg)
            
            # self.get_logger().info(f'Published joint commands: {self.current_joint_commands}')
    
    def gripper_command_callback(self, msg):
        """Convert GUI gripper command to Gazebo format"""
        self.current_gripper_command = msg.data
        
        # Convert 0-1 range to gripper joint positions (0.01 to 0.05 range)
        gripper_position = self.current_gripper_command * 0.04 + 0.01  
        
        gripper_msg = Float64()
        gripper_msg.data = gripper_position
        self.gripper_pub.publish(gripper_msg)
        
        # self.get_logger().info(f'Published gripper command: {gripper_position}')
    
    def gazebo_joint_state_callback(self, msg):
        """Forward Gazebo joint state to standard ROS2 joint_states topic"""
        # Create a new JointState message with standard topic name
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = self.get_clock().now().to_msg()
        joint_state_msg.header.frame_id = "base_link"
        
        # Copy joint data from Gazebo joint state
        joint_state_msg.name = msg.name
        joint_state_msg.position = msg.position
        joint_state_msg.velocity = msg.velocity if msg.velocity else [0.0] * len(msg.name)
        joint_state_msg.effort = msg.effort if msg.effort else [0.0] * len(msg.name)
        
        # Publish to standard ROS2 joint_states topic
        self.joint_state_pub.publish(joint_state_msg)
        
        # self.get_logger().info(f'Joint states: {dict(zip(joint_state_msg.name, joint_state_msg.position))}')

def main(args=None):
    rclpy.init(args=args)
    
    bridge_node = ArmGazeboBridge()
    
    try:
        rclpy.spin(bridge_node)
    except KeyboardInterrupt:
        pass
    finally:
        bridge_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
