#!/usr/bin/env python3

import math
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


# SCARA link lengths (meters)
L1 = 1.0
L2 = 1.0


def forward_kinematics(q1, q2, d3):
    x = L1 * math.cos(q1) + L2 * math.cos(q1 + q2)
    y = L1 * math.sin(q1) + L2 * math.sin(q1 + q2)
    z = d3
    return x, y, z


def main():
    rclpy.init()

    node = Node("scara_joint_command_publisher")

    # Controller command publisher (trajectory-based)
    command_pub = node.create_publisher(
        JointTrajectory,
        "/joint_trajectory_controller/joint_trajectory",
        10
    )

    # Desired joint values publisher (for error analyzer)
    joint_target_pub = node.create_publisher(
        Float64MultiArray,
        "/desired_joint_positions",
        10
    )

    # Expected hand position publisher (for error analyzer)
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
            d3 = float(input("Enter Joint 3 offset (m): "))
            duration_sec = float(input("Move duration (sec): "))

            # ----------------------------
            # Send trajectory command
            # ----------------------------
            traj_msg = JointTrajectory()
            traj_msg.joint_names = ["joint1", "joint2", "joint3"]

            point = JointTrajectoryPoint()
            point.positions = [q1, q2, d3]
            point.time_from_start = Duration(sec=int(duration_sec))

            traj_msg.points = [point]
            command_pub.publish(traj_msg)

            # ----------------------------
            # Publish desired joints (for analyzer)
            # ----------------------------
            joint_msg = Float64MultiArray()
            joint_msg.data = [q1, q2, d3]
            joint_target_pub.publish(joint_msg)

            # ----------------------------
            # Compute FK
            # ----------------------------
            x, y, z = forward_kinematics(q1, q2, d3)

            # ----------------------------
            # Publish expected position (for analyzer)
            # ----------------------------
            hand_msg = Float64MultiArray()
            hand_msg.data = [x, y, z]
            hand_target_pub.publish(hand_msg)

            print("\n----- Trajectory Sent -----")
            print(f"q1 = {q1:.3f} rad")
            print(f"q2 = {q2:.3f} rad")
            print(f"d3 = {d3:.3f} m")
            print(f"duration = {duration_sec:.1f} sec")

            print("\nExpected Hand Position:")
            print(f"x = {x:.3f} m, y = {y:.3f} m, z = {z:.3f} m")
            print("----------------------------\n")

            rclpy.spin_once(node, timeout_sec=0.1)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
