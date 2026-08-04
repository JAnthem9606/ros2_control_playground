#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


def main():
    rclpy.init()

    node = Node("joint_command_publisher_ppp")

    # Controller command publisher (trajectory-based)
    command_pub = node.create_publisher(
        JointTrajectory,
        "/joint_trajectory_controller/joint_trajectory",
        10
    )

    # Desired joint position publisher (for error analyzer)
    joint_target_pub = node.create_publisher(
        Float64MultiArray,
        "/desired_joint_positions",
        10
    )

    time.sleep(1.0)

    try:
        while rclpy.ok():
            q1 = float(input("Enter Joint 1 position, X (m): "))
            q2 = float(input("Enter Joint 2 position, Y (m): "))
            q3 = float(input("Enter Joint 3 position, Z (m): "))
            duration_sec = float(input("Move duration (sec): "))

            # ----------------------------
            # Send trajectory command
            # ----------------------------
            traj_msg = JointTrajectory()
            traj_msg.joint_names = ["joint1", "joint2", "joint3"]

            point = JointTrajectoryPoint()
            point.positions = [q1, q2, q3]
            point.time_from_start = Duration(sec=int(duration_sec))

            traj_msg.points = [point]
            command_pub.publish(traj_msg)

            # ----------------------------
            # Publish desired joints (for analyzer)
            # ----------------------------
            joint_msg = Float64MultiArray()
            joint_msg.data = [q1, q2, q3]
            joint_target_pub.publish(joint_msg)

            print("\n----- Trajectory Sent -----")
            print(f"q1 (X) = {q1:.3f} m")
            print(f"q2 (Y) = {q2:.3f} m")
            print(f"q3 (Z) = {q3:.3f} m")
            print(f"duration = {duration_sec:.1f} sec")
            print("----------------------------\n")

            rclpy.spin_once(node, timeout_sec=0.1)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
