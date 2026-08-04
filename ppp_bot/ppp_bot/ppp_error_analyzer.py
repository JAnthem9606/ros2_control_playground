#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState


desired_joints = None


def desired_joint_callback(msg):
    global desired_joints
    desired_joints = msg.data


def joint_state_callback(msg):
    global desired_joints

    if desired_joints is None:
        return

    try:
        q1_actual = msg.position[msg.name.index("joint1")]
        q2_actual = msg.position[msg.name.index("joint2")]
        q3_actual = msg.position[msg.name.index("joint3")]

        # Joint errors
        error_q1 = desired_joints[0] - q1_actual
        error_q2 = desired_joints[1] - q2_actual
        error_q3 = desired_joints[2] - q3_actual

        print("\n==============================")

        print("\nExpected Joint Positions")
        print("------------------------------")
        print(f"q1 expected = {desired_joints[0]:.6f} m")
        print(f"q2 expected = {desired_joints[1]:.6f} m")
        print(f"q3 expected = {desired_joints[2]:.6f} m")

        print("\nActual Joint Positions")
        print("------------------------------")
        print(f"q1 actual = {q1_actual:.6f} m")
        print(f"q2 actual = {q2_actual:.6f} m")
        print(f"q3 actual = {q3_actual:.6f} m")

        print("\nJoint Error")
        print("------------------------------")
        print(f"q1 error : {error_q1:.6f} m")
        print(f"q2 error : {error_q2:.6f} m")
        print(f"q3 error : {error_q3:.6f} m")

        print("==============================")

    except ValueError:
        print("Joint names not found")


def main():
    rclpy.init()

    node = Node("error_analyzer_ppp")

    node.create_subscription(
        Float64MultiArray,
        "/desired_joint_positions",
        desired_joint_callback,
        10
    )

    node.create_subscription(
        JointState,
        "/joint_states",
        joint_state_callback,
        10
    )

    print("Error analyzer running (PPP manipulator)...")

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
