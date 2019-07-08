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