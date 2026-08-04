#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


def build_point(positions, seconds):
    point = JointTrajectoryPoint()
    point.positions = positions
    point.time_from_start = Duration(sec=int(seconds))
    return point


def main():
    rclpy.init()

    node = Node("multi_waypoint_publisher_ppp")

    command_pub = node.create_publisher(
        JointTrajectory,
        "/joint_trajectory_controller/joint_trajectory",
        10
    )

    time.sleep(1.0)

    # ----------------------------------------------------
    # Define your waypoints here: (q1, q2, q3, time_from_start_sec)
    # time_from_start is CUMULATIVE from the start of the trajectory,
    # not the gap from the previous point.
    # ----------------------------------------------------
    waypoints = [
        (0.5, 0.0, 0.0, 3),
        (0.5, 0.5, 0.0, 6),
        (0.5, 0.5, 0.5, 9),
        (0.0, 0.0, 0.0, 13),
    ]

    traj_msg = JointTrajectory()
    traj_msg.joint_names = ["joint1", "joint2", "joint3"]

    for q1, q2, q3, t in waypoints:
        traj_msg.points.append(build_point([q1, q2, q3], t))

    print("\n----- Sending Multi-Waypoint Trajectory -----")
    for i, (q1, q2, q3, t) in enumerate(waypoints):
        print(f"Waypoint {i+1}: x={q1:.2f} y={q2:.2f} z={q3:.2f}  "
              f"(arrive at t={t}s)")
    print("----------------------------------------------\n")

    command_pub.publish(traj_msg)

    rclpy.spin_once(node, timeout_sec=0.5)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
