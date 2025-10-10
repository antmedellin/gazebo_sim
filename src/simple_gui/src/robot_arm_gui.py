import PySide6.QtCore
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)
        
        self.button_pose1 = QtWidgets.QPushButton("Pose 1")
        self.button_pose2 = QtWidgets.QPushButton("Pose 2")
        self.button_pose3 = QtWidgets.QPushButton("Pose 3")
        
        self.gripper_label = QtWidgets.QLabel("Open Gripper")
        self.slider_open_gripper = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.joint1_label = QtWidgets.QLabel("Joint 1")
        self.slider_joint1 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.joint2_label = QtWidgets.QLabel("Joint 2")
        self.slider_joint2 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.joint3_label = QtWidgets.QLabel("Joint 3")
        self.slider_joint3 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.joint4_label = QtWidgets.QLabel("Joint 4")
        self.slider_joint4 = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        
        

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button_pose1)
        self.layout.addWidget(self.button_pose2)
        self.layout.addWidget(self.button_pose3)
        self.layout.addWidget(self.gripper_label)
        self.layout.addWidget(self.slider_open_gripper)
        self.layout.addWidget(self.joint1_label)
        self.layout.addWidget(self.slider_joint1)
        self.layout.addWidget(self.joint2_label)
        self.layout.addWidget(self.slider_joint2)
        self.layout.addWidget(self.joint3_label)
        self.layout.addWidget(self.slider_joint3)
        self.layout.addWidget(self.joint4_label)
        self.layout.addWidget(self.slider_joint4)

        self.button_pose1.clicked.connect(self.action_pose1)
        self.button_pose2.clicked.connect(self.action_pose2)
        self.button_pose3.clicked.connect(self.action_pose3)
        self.slider_open_gripper.valueChanged.connect(self.action_open_gripper)
        self.slider_joint1.valueChanged.connect(self.action_joint1)
        self.slider_joint2.valueChanged.connect(self.action_joint2)
        self.slider_joint3.valueChanged.connect(self.action_joint3)
        self.slider_joint4.valueChanged.connect(self.action_joint4)

    @QtCore.Slot()
    def action_pose1(self):
        self.text.setText("Moving to Pose 1")
        #set slider values to specific values
        self.slider_open_gripper.setValue(50)
        self.slider_joint1.setValue(27)
        self.slider_joint2.setValue(36)
        self.slider_joint3.setValue(27)
        self.slider_joint4.setValue(18)
    @QtCore.Slot()
    def action_pose2(self):
        self.text.setText("Moving to Pose 2")
        #set slider values to specific values
        self.slider_open_gripper.setValue(75)
        self.slider_joint1.setValue(45)
        self.slider_joint2.setValue(54)
        self.slider_joint3.setValue(45)
        self.slider_joint4.setValue(36)
    @QtCore.Slot()
    def action_pose3(self):
        self.text.setText("Moving to Pose 3")
        #set slider values to specific values
        self.slider_open_gripper.setValue(100)
        self.slider_joint1.setValue(63)
        self.slider_joint2.setValue(81)
        self.slider_joint3.setValue(63)
        self.slider_joint4.setValue(54)
    @QtCore.Slot()
    def action_open_gripper(self):
        self.text.setText(f"Gripper Open Value: {self.slider_open_gripper.value()}")
        
        
    @QtCore.Slot()
    def action_joint1(self):
        self.text.setText(f"Joint 1 Value: {round(self.slider_joint1.value()*360/99,2)}")
    @QtCore.Slot()
    def action_joint2(self):    
        self.text.setText(f"Joint 2 Value: {round(self.slider_joint2.value()*270/99,2)}")
    @QtCore.Slot()
    def action_joint3(self):
        self.text.setText(f"Joint 3 Value: {round(self.slider_joint3.value()*270/99,2)}")
    @QtCore.Slot()
    def action_joint4(self):
        self.text.setText(f"Joint 4 Value: {round(self.slider_joint4.value()*270/99,2)}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(300, 300)
    widget.show()

    sys.exit(app.exec())