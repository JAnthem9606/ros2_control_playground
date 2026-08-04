from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'rrbot_kinematics'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
         (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ros2',
    maintainer_email='ros2@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': ['rrbot_forward_kinematics = rrbot_kinematics.rrbot_forward_kinematics:main',
        'rrbot_joint_command_publisher = rrbot_kinematics.rrbot_joint_command_publisher:main',
        'rrbot_error_analyzer = rrbot_kinematics.rrbot_error_analyzer:main',
        'rrbot_inverse_kinematics = rrbot_kinematics.rrbot_inverse_kinematics:main'
        ],
    },
)
