from setuptools import find_packages, setup

package_name = 'sample_arm'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/arm_simulation.launch.py']),
        ('share/' + package_name + '/launch', ['launch/rviz_arm_simulation.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=False,
    maintainer='developer',
    maintainer_email='developer@todo.todo',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            # 'talker = py_pubsub.publisher_member_function:main',
            # 'listener = py_pubsub.subscriber_member_function:main',
            'ros_arm_gui = sample_arm.ros_arm_gui:main',
            'arm_gazebo_bridge = sample_arm.arm_gazebo_bridge:main',
            'joint_state_converter = sample_arm.joint_state_converter:main',
            'tcp_joint_publisher = sample_arm.tcp_joint_publisher:main',
        ],
    },
)
