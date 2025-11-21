#!/usr/bin/env python3

import socket
import json
import serial
import time

if_connected = False

if if_connected:
    # Replace with your actual COM port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux/Mac)
    arduino_port = 'COM4'
    baud_rate = 9600
    # Connect to Arduino
    ser = serial.Serial(arduino_port, baud_rate)
    time.sleep(2)  # Wait for Arduino to reset



def main():
    host = 'localhost'
    port = 12345
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")
        
        buffer = ""
        previous_positions = None
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
                    current_positions = joint_data['position']
                    
                    # Check if positions have changed
                    if previous_positions is None or any(curr != prev for curr, prev in zip(current_positions, previous_positions)):
                        print(f"Joint1 angle: {current_positions[0]}")
                        print(f"Joint2 angle: {current_positions[1]}")
                        print(f"Joint3 angle: {current_positions[2]}")
                        print(f"Joint4 angle: {current_positions[3]}")
                        print(f"Joint5 angle: {current_positions[4]}")
                        print("-" * 40)
                        previous_positions = current_positions.copy()
                        
                        if if_connected:
                            if 0 <= current_positions[0] <= 270:
                                ser.write(f"{current_positions[0]}\n".encode())  # Send angle as string with newline
                                print(f"Sent angle: {current_positions[0]}")
                            else:
                                print("Angle must be between 0 and 270.")
                            
        
                    
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