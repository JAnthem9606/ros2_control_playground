#!/usr/bin/env python3

import math
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


# Robot link lengths (meters)
L1 = 1.0
L2 = 1.0


def forward_kinematics(q1, q2):
    x = L1 * math.cos(q1) + L2 * math.cos(q1 + q2)
    y = L1 * math.sin(q1) + L2 * math.sin(q1 + q2)
    return x, y


def main():
    rclpy.init()

    node = Node("joint_command_publisher")

    # Controller command publisher (trajectory-based, not flat array)
    command_pub = node.create_publisher(
        JointTrajectory,
        "/joint_trajectory_controller/joint_trajectory",
        10
    )

    # Desired joint angle publisher
    joint_target_pub = node.create_publisher(
        Float64MultiArray,
        "/desired_joint_positions",
        10
    )

    # Expected hand position publisher
    hand_target_pub = node.create_publisher(
        Float64MultiArray,
        "/expected_hand_position",
        10
    )

    time.sleep(1.0)

    try:
        while rclpy.ok():
            q1 = float(input("Enter Joint 1 angle (rad): "))
            q2 = float(input("Enter Joint 2 angle (rad): "))
            duration_sec = float(input("Move duration (sec): "))

            # ----------------------------
            # Send command to controller
            # ----------------------------
            traj_msg = JointTrajectory()
            traj_msg.joint_names = ["joint1", "joint2"]

            point = JointTrajectoryPoint()
            point.positions = [q1, q2]
            point.time_from_start = Duration(sec=int(duration_sec))

            traj_msg.points = [point]
            command_pub.publish(traj_msg)

            # ----------------------------
            # Publish desired joints
            # ----------------------------
            joint_msg = Float64MultiArray()
            joint_msg.data = [q1, q2]
            joint_target_pub.publish(joint_msg)

            # ----------------------------
            # Compute FK
            # ----------------------------
            x, y = forward_kinematics(q1, q2)

            # ----------------------------
            # Publish expected position
            # ----------------------------
            hand_msg = Float64MultiArray()
            hand_msg.data = [x, y]
            hand_target_pub.publish(hand_msg)

            print("\n----- Command Sent -----")
            print(f"q1 = {q1:.3f} rad")
            print(f"q2 = {q2:.3f} rad")
            print(f"duration = {duration_sec:.1f} sec")

            print("\nExpected Hand Position:")
            print(f"x = {x:.3f} m")
            print(f"y = {y:.3f} m")
            print("------------------------\n")

            rclpy.spin_once(node, timeout_sec=0.1)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
