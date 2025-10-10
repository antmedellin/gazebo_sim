import serial
import time

# Replace with your actual COM port (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux/Mac)
arduino_port = 'COM4'
baud_rate = 9600

# Connect to Arduino
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Wait for Arduino to reset

def set_servo_angle(angle):
    if 0 <= angle <= 180:
        ser.write(f"{angle}\n".encode())  # Send angle as string with newline
        print(f"Sent angle: {angle}")
    else:
        print("Angle must be between 0 and 180.")

# Example usage
while True:
    try:
        user_input = input("Enter servo angle (0-180): ")
        angle = int(user_input)
        set_servo_angle(angle)
    except ValueError:
        print("Please enter a valid integer.")