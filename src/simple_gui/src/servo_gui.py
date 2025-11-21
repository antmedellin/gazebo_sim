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

    @QtCore.Slot()
    def action_pose1(self):
        self.text.setText("Moving to Pose 1")
        #set slider values to specific values
        self.slider_joint1.setValue(0)
        self.slider_joint2.setValue(0)
        self.slider_joint3.setValue(0)
        self.slider_joint4.setValue(0)
        self.slider_joint5.setValue(0)
    @QtCore.Slot()
    def action_pose2(self):
        self.text.setText("Moving to Pose 2")
        #set slider values to specific values
        self.slider_joint1.setValue(90)
        self.slider_joint2.setValue(90)
        self.slider_joint3.setValue(90)
        self.slider_joint4.setValue(90)
        self.slider_joint5.setValue(90)
    @QtCore.Slot()
    def action_pose3(self):
        self.text.setText("Moving to Pose 3")
        #set slider values to specific values
        self.slider_joint1.setValue(20)
        self.slider_joint2.setValue(40)
        self.slider_joint3.setValue(60)
        self.slider_joint4.setValue(80)
        self.slider_joint5.setValue(100)
   
        
    @QtCore.Slot()
    def action_joint1(self):
        self.text.setText(f"Joint 1 Value: {int(self.slider_joint1.value()*270/99)}")
    @QtCore.Slot()
    def action_joint2(self):    
        self.text.setText(f"Joint 2 Value: {int(self.slider_joint2.value()*270/99)}")
    @QtCore.Slot()
    def action_joint3(self):
        self.text.setText(f"Joint 3 Value: {int(self.slider_joint3.value()*270/99)}")
    @QtCore.Slot()
    def action_joint4(self):
        self.text.setText(f"Joint 4 Value: {int(self.slider_joint4.value()*270/99)}")
    @QtCore.Slot()
    def action_joint5(self):
        self.text.setText(f"Joint 5 Value: {int(self.slider_joint5.value()*270/99)}")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(300, 300)
    widget.show()

    sys.exit(app.exec())