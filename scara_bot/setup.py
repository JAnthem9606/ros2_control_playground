from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'scara_bot'

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
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz'))
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
        'console_scripts': ['scara_fk = scara_bot.scara_forward_kinematics:main',
        'scara_ik = scara_bot.scara_inverse_kinematics:main',
        'scara_command_publisher = scara_bot.scara_joint_command_publisher:main',
        'scara_error_analyzer = scara_bot.scara_error_analyzer:main',
        ],
    },
)
