#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import socket
import threading
import json
import time


class TCPJointPublisher(Node):
    def __init__(self):
        super().__init__('tcp_joint_publisher')
        
        # Subscribe to joint states
        self.joint_state_sub = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_state_callback,
            10
        )
        
        # TCP server setup
        self.host = '0.0.0.0'  # Listen on all interfaces
        self.port = 12345
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.tcp_clients = []
        
        # Start server thread
        self.server_thread = threading.Thread(target=self.handle_connections)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        self.get_logger().info(f'TCP Joint Publisher node started, listening on port {self.port}')
    
    def handle_connections(self):
        while True:
            try:
                client_socket, addr = self.server_socket.accept()
                self.get_logger().info(f'Client connected: {addr}')
                self.tcp_clients.append(client_socket)
            except Exception as e:
                self.get_logger().error(f'Error accepting connection: {e}')
    
    def joint_state_callback(self, msg):
        """Receive joint states and send to TCP clients"""
        # Convert JointState to dict
        joint_data = {
            'header': {
                'stamp': {
                    'sec': msg.header.stamp.sec,
                    'nanosec': msg.header.stamp.nanosec
                },
                'frame_id': msg.header.frame_id
            },
            'name': list(msg.name),
            'position': list(msg.position),
            'velocity': list(msg.velocity),
            'effort': list(msg.effort)
        }
        
        # Serialize to JSON
        data = json.dumps(joint_data) + '\n'
        
        # Send to all clients
        disconnected_clients = []
        for client in self.tcp_clients:
            try:
                client.sendall(data.encode('utf-8'))
            except:
                disconnected_clients.append(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            self.tcp_clients.remove(client)
    
    def __del__(self):
        self.server_socket.close()
        for client in self.tcp_clients:
            client.close()


def main(args=None):
    rclpy.init(args=args)
    node = TCPJointPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()