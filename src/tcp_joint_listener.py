#!/usr/bin/env python3

import socket
import json

def main():
    host = 'localhost'
    port = 12345
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")
        
        buffer = ""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            buffer += data.decode('utf-8')
            
            # Process complete messages (assuming newline separated)
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                try:
                    joint_data = json.loads(line)
                    print("Received joint states:")
                    print(f"Names: {joint_data['name']}")
                    print(f"Positions: {joint_data['position']}")
                    print(f"Velocities: {joint_data['velocity']}")
                    print(f"Efforts: {joint_data['effort']}")
                    print("-" * 40)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
    except KeyboardInterrupt:
        print("Interrupted")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == '__main__':
    main()