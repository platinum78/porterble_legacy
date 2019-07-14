#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Kinematic Controller
* Author        : Susung Park
* Description   : Kinematics controller for autonomous vehicle.
* Version       : On development...
********************************************************************************
"""

import time, threading
import numpy as np
from .geometry_datatypes import Pose2D

class MecanumWheel:
    def __init__(self, wheel_info_dict):
        self.L_x, self.L_y = wheel_info_dict["origin"]
        self.radius = wheel_info_dict["radius"]
        self.wheel_orientation = wheel_info_dict["wheel_orientation"]
        self.roller_orientation = wheel_info_dict["roller_orientation"]
        self.alpha = np.arctan2(self.L_y, self.L_x)
        self.beta = self.wheel_orientation - self.alpha
        self.gamma = self.wheel_orientation - self.roller_orientation

class QuadMecanumKinematics:
    def __init__(self, config_dict):
        wheel_info_dict = config_dict["wheel_info"]

        # Load wheel dimension and allocation information from configuration dict.
        self.wheel_1 = MecanumWheel(wheel_info_dict["wheel_1"])
        self.wheel_2 = MecanumWheel(wheel_info_dict["wheel_2"])
        self.wheel_3 = MecanumWheel(wheel_info_dict["wheel_3"])
        self.wheel_4 = MecanumWheel(wheel_info_dict["wheel_4"])

        # Create matrices A and B and set coefficients.
        self.mat_A = np.zeros([4, 4])
        self.mat_B = np.ones([4, 3])
        self.W = np.zeros([4, 1])
        self.V = np.zeros([3, 1])

        self.mat_A[0, 0] = self.A_func(self.wheel_1)
        self.mat_A[1, 1] = self.A_func(self.wheel_2)
        self.mat_A[2, 2] = self.A_func(self.wheel_3)
        self.mat_A[3, 3] = self.A_func(self.wheel_4)

        self.mat_B[0, 1] = self.B_func(self.wheel_1)
        self.mat_B[1, 1] = self.B_func(self.wheel_2)
        self.mat_B[2, 1] = self.B_func(self.wheel_3)
        self.mat_B[3, 1] = self.B_func(self.wheel_4)

        self.mat_B[0, 2] = self.C_func(self.wheel_1)
        self.mat_B[1, 2] = self.C_func(self.wheel_2)
        self.mat_B[2, 2] = self.C_func(self.wheel_3)
        self.mat_B[3, 2] = self.C_func(self.wheel_4)

        # Pre-compute inv(A) * B, to save computing resource.
        self.AiB = np.matmul(np.linalg.inv(self.mat_A), self.mat_B)
    
    def compute_wheel_velocity(self, v_x, v_y, w):
        self.V[:, 0] = [v_x, v_y, w]
        self.W = np.matmul(self.AiB)
        w_1, w_2, w_3, w_4 = self.W[:, 0]
        return w_1, w_2, w_3, w_4
    
    def A_func(self, wheel):
        return R * (np.sin(wheel.alpha + wheel.beta) \
                  - np.tan(wheel.alpha + wheel.beta - wheel.gamma) \
                  * np.cos(wheel.alpha + wheel.beta))
    
    def B_func(self, wheel):
        return np.tan(wheel.alpha + wheel.beta - wheel.gamma)
    
    def C_func(self, wheel):
        return np.tan(whee.alpha + wheel.beta - wheel.gamma) * wheel.L_x - wheel.L_y


class KinematicControllerPID:
    def __init__(self, kp, ki, kd):
        """
        Kinematic controller deals only with kinematic constraints.
        This controller acts as if the system is immediately responsive.
        This implementation is in the purpose to isolate kinetic constraints from kinematics,
        in order to make it relatively easy to change the physical composition of the robot.
        """
        # Get PID gains.
        self.kp = kp
        self.ki = ki
        self.kd = kd

        # Kinematic state variables.
        self.pose_curr = Pose2D(0, 0, 0)
        self.pose_prev = Pose2D(0, 0, 0)
        self.pose_diff = Pose2D(0, 0, 0)
        self.velocity_curr = Pose2D(0, 0, 0)
        self.velocity_prev = Pose2D(0, 0, 0)
        self.velocity_diff = Pose2D(0, 0, 0)

        # Kinematic target variables.
        self.pose_target = Pose2D(0, 0, 0)
        self.velocity_target = Pose2D(0, 0, 0)

        # Timestamps.
        self.timestamp_curr = 0.0
        self.timestamp_prev = 0.0
        self.timestamp_diff = 0.0

        # Error-related variables.
        self.error_integral = Pose2D(0, 0, 0)
        self.error_differential = Pose2D(0, 0, 0)

    def pid_controller(self, pose_target=None, velocity_target=None):
        if pose_target is not None:
            self.pose_target