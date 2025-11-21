import PySide6.QtCore
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, Float64
from sensor_msgs.msg import JointState
from std_srvs.srv import SetBool
import threading

class RobotArmNode(Node):
    def __init__(self):
        super().__init__('robot_arm_gui_node')
        
        # ROS2 Publishers
        self.joint_cmd_pub = self.create_publisher(Float64MultiArray, 'joint_commands', 10)
      
        
        # Timer for publishing joint commands
        self.timer = self.create_timer(0.1, self.publish_joint_commands)  # 10Hz
        
        # Store current slider values
        self.current_joint_values = [20, 20, 20, 20,20]  # Default middle position
    
    def update_joint_values(self, joint1, joint2, joint3, joint4, joint5):
        """Update joint values from GUI"""
        self.current_joint_values = [joint1, joint2, joint3, joint4, joint5]
    
    def publish_joint_commands(self):
        """Publish current slider values as joint commands"""
        # Convert slider values (0-99) to radians for joints, centered around zero
        joint_msg = Float64MultiArray()
        joint_msg.data = [
            (self.current_joint_values[0] ),  # 0 to 270 degrees
            (self.current_joint_values[1] ),  # 0 to 270 degrees
            (self.current_joint_values[2] ),  # 0 to 270 degrees
            (self.current_joint_values[3] ),  # 0 to 270 degrees
            (self.current_joint_values[4] ),  # 0 to 270 degrees
        ]
        self.joint_cmd_pub.publish(joint_msg)
        
   

class robot_arm_gui(QtWidgets.QWidget):
    def __init__(self, ros_node):
        super().__init__()
        
        # Store reference to ROS node
        self.ros_node = ros_node
        
        self.text = QtWidgets.QLabel("Robot Arm Controller", alignment=QtCore.Qt.AlignCenter)
        
        self.button_pose1 = QtWidgets.QPushButton("Pose 1")
        self.button_pose2 = QtWidgets.QPushButton("Pose 2")
        self.button_pose3 = QtWidgets.QPushButton("Pose 3")
        

        self.joint1_label = QtWidgets.QLabel("Joint 1")
        self.slider_joint1 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.joint2_label = QtWidgets.QLabel("Joint 2")
        self.slider_joint2 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.joint3_label = QtWidgets.QLabel("Joint 3")
        self.slider_joint3 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.joint4_label = QtWidgets.QLabel("Joint 4")
        self.slider_joint4 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.joint5_label = QtWidgets.QLabel("Joint 5")
        self.slider_joint5 = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button_pose1)
        self.layout.addWidget(self.button_pose2)
        self.layout.addWidget(self.button_pose3)
        self.layout.addWidget(self.joint1_label)
        self.layout.addWidget(self.slider_joint1)
        self.layout.addWidget(self.joint2_label)
        self.layout.addWidget(self.slider_joint2)
        self.layout.addWidget(self.joint3_label)
        self.layout.addWidget(self.slider_joint3)
        self.layout.addWidget(self.joint4_label)
        self.layout.addWidget(self.slider_joint4)
        self.layout.addWidget(self.joint5_label)
        self.layout.addWidget(self.slider_joint5)

        self.button_pose1.clicked.connect(self.action_pose1)
        self.button_pose2.clicked.connect(self.action_pose2)
        self.button_pose3.clicked.connect(self.action_pose3)
        self.slider_joint1.valueChanged.connect(self.action_joint1)
        self.slider_joint2.valueChanged.connect(self.action_joint2)
        self.slider_joint3.valueChanged.connect(self.action_joint3)
        self.slider_joint4.valueChanged.connect(self.action_joint4)
        self.slider_joint5.valueChanged.connect(self.action_joint5)
        
        # Initialize slider ranges (0-99 default, but you can set specific ranges)
        for slider in [self.slider_joint1, self.slider_joint2, self.slider_joint3, self.slider_joint4, self.slider_joint5]:
            slider.setMinimum(0)
            slider.setMaximum(270)
            slider.setValue(20)  # Start at middle position

    @QtCore.Slot()
    def action_pose1(self):
        # self.text.setText("Moving to Pose 1")
        # Set slider values to specific values
        self.slider_joint1.setValue(0)
        self.slider_joint2.setValue(0)
        self.slider_joint3.setValue(0)
        self.slider_joint4.setValue(0)
        self.slider_joint5.setValue(0)
        # Update ROS node with new values
        self.update_ros_values()
        
    @QtCore.Slot()
    def action_pose2(self):
        # self.text.setText("Moving to Pose 2")
        # Set slider values to specific values
        self.slider_joint1.setValue(90)
        self.slider_joint2.setValue(90)
        self.slider_joint3.setValue(90)
        self.slider_joint4.setValue(90)
        self.slider_joint5.setValue(90)
        # Update ROS node with new values
        self.update_ros_values()
        
    @QtCore.Slot()
    def action_pose3(self):
        # self.text.setText("Moving to Pose 3")
        # Set slider values to specific values
        self.slider_joint1.setValue(20)
        self.slider_joint2.setValue(40)
        self.slider_joint3.setValue(60)
        self.slider_joint4.setValue(80)
        self.slider_joint5.setValue(100)
        # Update ROS node with new values
        self.update_ros_values()
        
    @QtCore.Slot()
    def action_joint1(self):
        angle = (self.slider_joint1.value() )  # 0 to 270 degrees
        self.joint1_label.setText(f"Joint 1: {round(angle, 2)}°")
        self.update_ros_values()
        
    @QtCore.Slot()
    def action_joint2(self):
        angle = (self.slider_joint2.value() )  # 0 to 270 degrees
        self.joint2_label.setText(f"Joint 2: {round(angle, 2)}°")
        self.update_ros_values()
        
    @QtCore.Slot()
    def action_joint3(self):
        angle = (self.slider_joint3.value() )  # 0 to 270 degrees
        self.joint3_label.setText(f"Joint 3: {round(angle, 2)}°")
        self.update_ros_values()
        
    @QtCore.Slot()
    def action_joint4(self):
        angle = (self.slider_joint4.value() )  # 0 to 270 degrees
        self.joint4_label.setText(f"Joint 4: {round(angle, 2)}°")
        self.update_ros_values()
    
    @QtCore.Slot()
    def action_joint5(self):
        angle = (self.slider_joint5.value() )  # 0 to 270 degrees
        self.joint5_label.setText(f"Joint 5: {round(angle, 2)}°")
        self.update_ros_values()
    
    def update_ros_values(self):
        """Update the ROS node with current slider values"""
        self.ros_node.update_joint_values(
            self.slider_joint1.value(),
            self.slider_joint2.value(),
            self.slider_joint3.value(),
            self.slider_joint4.value(),
            self.slider_joint5.value()
        )
      


def main(args=None):
    rclpy.init(args=args)
    
    # Create ROS2 node
    ros_node = RobotArmNode()
    
    # Create Qt application
    app = QtWidgets.QApplication([])
    
    # Create GUI and pass ROS node to it
    arm_gui = robot_arm_gui(ros_node)
    arm_gui.setWindowTitle("Robot Arm Controller")
    arm_gui.resize(400, 600)
    arm_gui.show()
    
    # Create a thread for ROS2 spinning
    def ros_spin():
        rclpy.spin(ros_node)
    
    ros_thread = threading.Thread(target=ros_spin, daemon=True)
    ros_thread.start()
    
    try:
        sys.exit(app.exec())
    finally:
        ros_node.destroy_node()
        rclpy.shutdown()
    
if __name__ == "__main__":
    
    main()
