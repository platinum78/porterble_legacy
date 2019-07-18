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
from ..utils.logging import *
from .geometry_datatypes import Pose2D

def cubic_parametrize(b, c):
    mat = np.ones([2, 2])
    mat[0, 0] = b**3 / 3 - (b + c) * b**2 / 2 + b**2 * c
    mat[1, 0] = c**3 / 3 - (b + c) * c**2 / 2 + b * c**2
    vec = np.array([[b], [c]])
    res = np.matmul(np.linalg.inv(mat), vec)
    a = res[0, 0]
    k = res[1, 0]
    
    def cubic_func(x):
        return a / 3 * x**3 - a / 2 * (b + c) * x**2 + a * b * c * x + k
    
    return cubic_func

class PathGenerator:
    def __init__(self, config_dict):
        # Read path-planner parameters from config_dict.
        self.min_path_radius = config_dict["min_path_radius"]
        self.side_slippable = config_dict["side_slippable"]
        print_info("Path generator initialized.")
        pass
        
    def generate_path(self, grid_map, init_pose, final_pose, path_resolution=0.05):
        """
        Generate path between two points.
        Other sophisticated path generators will refer to this method.
        init_pose and final_pose should be given in Pose2D type, and path resolution is given in meters.
        """
        if type(init_pose) != Pose2D:
            raise TypeError("Initial pose should be given in Pose2D object.")
        if type(final_pose) != Pose2D:
            raise TypeError("Final pose should be given in Pose2D object.")

        pose_diff = final_pose - init_pose
        scalar_dist = np.sqrt(pose_diff.x ** 2 + pose_diff.y ** 2)
        waypoints_num = int(scalar_dist / path_resolution)
        cubic_func = cubic_parametrize(init_pose.t, final_pose.t)
        x = np.linspace(init_pose.x, final_pose.x, waypoints_num, True)
        y = np.linspace(init_pose.y, final_pose.y, waypoints_num, True)
        t = np.linspace(init_pose.t, final_pose.t, waypoints_num, True)
        t_cubic = cubic_func(t)
        
        path = np.append(x, y, axis=0)
        path = np.append(path, t, axis=0)
        path = np.transpose(path)

        for point in path:
            yield Pose2D(point[0], point[1], point[2])