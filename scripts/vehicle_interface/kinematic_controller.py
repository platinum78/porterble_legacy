#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Kinematic Controller
* Author        : Susung Park
* Description   : Kinematics controller for autonomous vehicle.
* Version       : On development...
********************************************************************************
"""

import threading
import numpy as np

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
        self.mat_A = np.zeros(4, 4)
        self.mat_B = np.ones(4, 3)

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
    
    def compute_wheel_velocity(self, v_x, v_y, w):
        
    
    def A_func(self, wheel):
        return R * (np.sin(wheel.alpha + wheel.beta) \
                  - np.tan(wheel.alpha + wheel.beta - wheel.gamma) \
                  * np.cos(wheel.alpha + wheel.beta))
    
    def B_func(self, wheel):
        return np.tan(wheel.alpha + wheel.beta - wheel.gamma)
    
    def C_func(self, wheel):
        return np.tan(whee.alpha + wheel.beta - wheel.gamma) * wheel.L_x - wheel.L_y
    
def QuadMecanumKinematics_(wheel_info_dict, v_x, v_y, w):
    pass


class KinematicController:
    def __init__(self):
        """
        Kinematic controller deals only with kinematic constraints.
        This controller acts as if the system is immediately responsive.
        This implementation is in the purpose to isolate kinetic constraints from kinematics,
        in order to make it relatively easy to change the physical composition of the robot.
        """
        # Kinematic state variables.
        self.velocity = Var2D(0, 0, 0)
        self.velocity_ = Var2D(0, 0, 0)
        self.pose = Var2D(0, 0, 0)
        self.pose_ = Var2D(0, 0, 0)

        # Kinematic target variables.
        self.velocity_target = Var2D(0, 0, 0)
        self.velocity_target_ = Var2D(0, 0, 0)
        self.pose_target = Var2D(0, 0, 0)
        self.pose_target_ = Var2D(0, 0, 0)