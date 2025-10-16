"""
arduino_servo.py

WSL notes:
 - WSL2 doesn't have native USB passthrough by default. If your Arduino appears on Windows as COMx, you can either
     * use a Windows-side program to forward the COM port into WSL (e.g., com0com, socat on Windows, or use newer WSL USB support),
     * or access the device via a Linux device path if the device is exposed (e.g., /dev/ttyS* or /dev/ttyUSB*).
 - Ensure your WSL user has permission to read/write the serial device (add to the 'dialout' group or use udev rules):
         sudo usermod -a -G dialout $USER
         # then log out/in for group changes to take effect

This script auto-detects common serial device names and accepts --port to override.
"""

import serial
import time
import sys
import argparse
import platform
from glob import glob

baud_rate = 9600


def guess_ports():
    """Return a list of likely serial ports depending on the platform.

    This covers Windows (COM*), Linux/WSL (/dev/ttyUSB*, /dev/ttyACM*, /dev/ttyS*),
    and macOS (/dev/tty.* /dev/cu.*).
    """
    system = platform.system()
    ports = []
    if system == 'Windows':
        # Common COM ports; pyserial accepts 'COM3', 'COM4', etc.
        ports = [f'COM{i}' for i in range(1, 21)]
    elif system == 'Darwin':
        ports = glob('/dev/tty.*') + glob('/dev/cu.*')
    else:
        # Linux and WSL
        ports = glob('/dev/ttyUSB*') + glob('/dev/ttyACM*') + glob('/dev/ttyS*')

    return ports


def find_port(preferred=None):
    # If user provided a preferred port, try that first
    if preferred:
        return preferred

    candidates = guess_ports()
    if not candidates:
        return None

    # Prefer /dev/ttyACM* or /dev/ttyUSB* if present
    for pattern in ('/dev/ttyACM', '/dev/ttyUSB', 'COM'):
        for p in candidates:
            if pattern in p:
                return p

    # Fallback to first candidate
    return candidates[0]


def connect(port, baud):
    try:
        ser = serial.Serial(port, baud, timeout=1)
        # Give Arduino a moment to reset after opening the port
        time.sleep(2)
        print(f'Connected to {port} at {baud} baud')
        return ser
    except serial.SerialException as e:
        msg = str(e)
        print(f'Failed to open serial port {port}: {msg}')

        # Provide actionable tips for common permission errors
        if 'Permission' in msg or 'permission' in msg or 'denied' in msg.lower():
            print('\nPermission denied when opening the serial port.')
            print('Common fixes:')
            print(" - Add your user to the 'dialout' group (permanent): sudo usermod -a -G dialout $USER")
            print("   Then log out/in or run 'newgrp dialout' in your shell to activate the group immediately.")
            print(" - Temporary workaround (not recommended for production): sudo chmod 666 {port}")
            print(" - As a last resort, run the script with sudo, e.g., sudo python3 arduino_servo.py")
            print(" - In WSL: ensure the device is visible in /dev (WSL2 may need USB passthrough or a Windows-side forwarder).")

        return None


def set_servo_angle(ser, angle):
    if ser is None:
        print('Serial port not open.')
        return

    if 0 <= angle <= 180:
        try:
            ser.write(f"{angle}\n".encode())  # Send angle as string with newline
            print(f"Sent angle: {angle}")
        except serial.SerialException as e:
            print(f'Error writing to serial port: {e}')
    else:
        print('Angle must be between 0 and 180.')


def main():
    parser = argparse.ArgumentParser(description='Send servo angles to an Arduino.')
    parser.add_argument('--port', '-p', help='Serial port (e.g. COM3 or /dev/ttyACM0).')
    parser.add_argument('--baud', '-b', type=int, default=baud_rate, help=f'Baud rate (default {baud_rate})')
    args = parser.parse_args()

    port = find_port(args.port)
    if not port:
        print('No serial ports found. If you are using WSL, pass the Windows path (e.g., /dev/ttyS* or /dev/ttyUSB*) or mount the device.\n'
              'In WSL you may need to map the device from Windows or enable USB support.\n'
              'Alternatively pass --port to specify the serial device explicitly.')
        sys.exit(1)

    ser = connect(port, args.baud)
    if ser is None:
        sys.exit(1)

    try:
        while True:
            try:
                user_input = input('Enter servo angle (0-180): ')
                angle = int(user_input)
                set_servo_angle(ser, angle)
            except ValueError:
                print('Please enter a valid integer.')
    except (KeyboardInterrupt, EOFError):
        print('\nExiting and closing serial port.')
    finally:
        try:
            ser.close()
        except Exception:
            pass


if __name__ == '__main__':
    main()