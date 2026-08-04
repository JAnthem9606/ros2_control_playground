#!/usr/bin/env python3

import math
import time

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


# Robot link lengths (meters)
L1 = 1.0
L2 = 1.0


def forward_kinematics(q1, q2):
    """
    Compute end-effector position from joint angles.
    """
    x = L1 * math.cos(q1) + L2 * math.cos(q1 + q2)
    y = L1 * math.sin(q1) + L2 * math.sin(q1 + q2)
    return x, y


def inverse_kinematics(x, y):
    """
    Compute joint angles from desired end-effector position.
    Returns one IK solution (elbow-up).
    """
    D = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)

    # Check if target is reachable
    if D < -1.0 or D > 1.0:
        return None

    q2 = math.acos(D)

    q1 = math.atan2(y, x) - math.atan2(
        L2 * math.sin(q2),
        L1 + L2 * math.cos(q2)
    )

    return q1, q2


def main():
    rclpy.init()

    node = Node("inverse_kinematics")

    publisher = node.create_publisher(
        JointTrajectory,
        "/joint_trajectory_controller/joint_trajectory",
        10,
    )

    time.sleep(1.0)

    try:
        while rclpy.ok():

            print("\nEnter desired hand position")

            x = float(input("x (m): "))
            y = float(input("y (m): "))
            duration_sec = float(input("Move duration (sec): "))

            result = inverse_kinematics(x, y)

            if result is None:
                print("\nTarget position is outside the robot workspace.\n")
                continue

            q1, q2 = result

            # ----------------------------
            # Publish trajectory command
            # ----------------------------
            traj_msg = JointTrajectory()
            traj_msg.joint_names = ["joint1", "joint2"]

            point = JointTrajectoryPoint()
            point.positions = [q1, q2]
            point.time_from_start = Duration(sec=int(duration_sec))

            traj_msg.points = [point]
            publisher.publish(traj_msg)

            # Verify using Forward Kinematics
            x_fk, y_fk = forward_kinematics(q1, q2)

            print("\n========== Inverse Kinematics ==========")
            print(f"Desired Position")
            print(f"x = {x:.3f} m")
            print(f"y = {y:.3f} m")

            print("\nComputed Joint Angles")
            print(f"q1 = {q1:.3f} rad ({math.degrees(q1):.2f}°)")
            print(f"q2 = {q2:.3f} rad ({math.degrees(q2):.2f}°)")

            print("\nForward Kinematics Verification")
            print(f"x = {x_fk:.3f} m")
            print(f"y = {y_fk:.3f} m")

            print("========================================\n")

            rclpy.spin_once(node, timeout_sec=0.1)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
