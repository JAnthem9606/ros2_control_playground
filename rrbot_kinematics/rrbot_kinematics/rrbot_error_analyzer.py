#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState


L1 = 1.0
L2 = 1.0


desired_joints = None
expected_position = None


def forward_kinematics(q1, q2):

    x = L1 * math.cos(q1) + L2 * math.cos(q1 + q2)
    y = L1 * math.sin(q1) + L2 * math.sin(q1 + q2)

    return x, y



def desired_joint_callback(msg):

    global desired_joints

    desired_joints = msg.data



def expected_position_callback(msg):

    global expected_position

    expected_position = msg.data



def joint_state_callback(msg):

    global desired_joints
    global expected_position


    if desired_joints is None:
        return

    if expected_position is None:
        return


    try:

        q1_actual = msg.position[msg.name.index("joint1")]
        q2_actual = msg.position[msg.name.index("joint2")]


        # Joint errors

        error_q1 = desired_joints[0] - q1_actual
        error_q2 = desired_joints[1] - q2_actual



        # Actual FK

        x_actual, y_actual = forward_kinematics(
            q1_actual,
            q2_actual
        )



        # Cartesian error

        error_x = expected_position[0] - x_actual
        error_y = expected_position[1] - y_actual


        distance_error = math.sqrt(
            error_x**2 + error_y**2
        )


        print("\n==============================")
        
        print("\nExpected Joint Positions")
        print("------------------------------")
        print(f"q1 expected = {desired_joints[0]:.6f} rad")
        print(f"q2 expected = {desired_joints[1]:.6f} rad")
        
        
        print("\nActual Joint Positions")
        print("------------------------------")
        print(f"q1 actual = {q1_actual:.6f} rad")
        print(f"q2 actual = {q2_actual:.6f} rad")


        print("\nJoint Error")
        print("------------------------------")
        print(f"q1 error : {error_q1:.6f} rad")
        print(f"q2 error : {error_q2:.6f} rad")


        print("\nExpected Hand:")
        print(f"x = {expected_position[0]:.4f}")
        print(f"y = {expected_position[1]:.4f}")


        print("\nActual Hand:")
        print(f"x = {x_actual:.4f}")
        print(f"y = {y_actual:.4f}")


        print("\nPosition Error:")
        print(f"x error = {error_x:.6f}")
        print(f"y error = {error_y:.6f}")
        print(f"Total error = {distance_error:.6f} m")


        print("==============================")



    except ValueError:

        print("Joint names not found")



def main():

    rclpy.init()

    node = Node("error_analyzer")


    node.create_subscription(
        Float64MultiArray,
        "/desired_joint_positions",
        desired_joint_callback,
        10
    )


    node.create_subscription(
        Float64MultiArray,
        "/expected_hand_position",
        expected_position_callback,
        10
    )


    node.create_subscription(
        JointState,
        "/joint_states",
        joint_state_callback,
        10
    )


    print("Error analyzer running...")


    rclpy.spin(node)


    node.destroy_node()
    rclpy.shutdown()



if __name__ == "__main__":
    main()
