#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Path Generator
* Author        : Susung Park
* Description   : Path planning and waypoints generation.
* Version       : On development...
********************************************************************************
"""

import threading
import numpy as np
from .datatypes import State2D


class PathGenerator:
    def __init__(self, config_dict, side_slippable):
        # Read path-planner parameters from config_dict.
        self.min_path_radius = config_dict["min_path_radius"]
        self.side_slippable = side_slippable
    
    def generate_path(self, init_pose, final_pose, obstacles):
        if type(init_pose) != State2D:
            raise TypeError("Initial pose should be given in State2D object.")
        if type(final_pose) != State2D:
            raise TypeError("Final pose should be given in State2D object.")
        
    def generate_nonslip_path(self, init_pose, final_pose, obstacles):
        pass
    
    def generate_slip_path(self, init_pose, final_pose, obstacles):
        pass