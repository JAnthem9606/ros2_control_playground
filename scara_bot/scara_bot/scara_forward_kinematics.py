#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


# SCARA link lengths (meters)
L1 = 1.0
L2 = 1.0


def forward_kinematics(q1, q2, d3):
    """
    SCARA FK: X-Y from the two revolute joints (identical to 2R planar),
    Z is fully decoupled -- just the prismatic joint's own offset.
    """
    x = L1 * math.cos(q1) + L2 * math.cos(q1 + q2)
    y = L1 * math.sin(q1) + L2 * math.sin(q1 + q2)
    z = d3
    return x, y, z


def joint_state_callback(msg):
    try:
        q1 = msg.position[msg.name.index("joint1")]
        q2 = msg.position[msg.name.index("joint2")]
        d3 = msg.position[msg.name.index("joint3")]

        x, y, z = forward_kinematics(q1, q2, d3)

        print("\nActual Joint Values")
        print("--------------------------------")
        print(f"Joint 1 (q1) : {q1:.3f} rad")
        print(f"Joint 2 (q2) : {q2:.3f} rad")
        print(f"Joint 3 (d3) : {d3:.3f} m")

        print("\nActual End Effector Position")
        print("--------------------------------")
        print(f"X : {x:.3f} m")
        print(f"Y : {y:.3f} m")
        print(f"Z : {z:.3f} m")

    except ValueError:
        print("Joint names not found in /joint_states")


def main():
    rclpy.init()

    node = Node("scara_fk_from_joint_states")

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
