#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


# Link lengths (meters)
L1 = 1.0
L2 = 1.0


def forward_kinematics(q1, q2):
    x = L1 * math.cos(q1) + L2 * math.cos(q1 + q2)
    y = L1 * math.sin(q1) + L2 * math.sin(q1 + q2)
    return x, y


def joint_state_callback(msg):
    try:
        # Replace these names with your robot's joint names
        q1 = msg.position[msg.name.index("joint1")]
        q2 = msg.position[msg.name.index("joint2")]

        x, y = forward_kinematics(q1, q2)
        print("Actual Joint Angles")
        print("--------------------------------")
        print(f"Joint 1 : {q1:.3f} rad")
        print(f"Joint 2 : {q2:.3f} rad")
        print("Actual End Effector Position")
        print("--------------------------------")
        print(f"End Effector X  : {x:.3f} m")
        print(f"End Effector Y  : {y:.3f} m")

    except ValueError:
        print("Joint names not found in /joint_states")


def main():
    rclpy.init()

    node = Node("fk_from_joint_states")

    node.create_subscription(
        JointState,
        "/joint_states",
        joint_state_callback,
        10,
    )

    print("Listening to /joint_states ...")

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
