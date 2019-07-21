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
from ...utils.logging import *
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


class TripleMarkerPoseEstimator:
    def __init__(self, marker2, marker3):
        self.marker2 = marker2
        self.marker3 = marker3

        self.offset_x = 0
        self.offset_y = 0
        self.rotation = 0

    def compute_pose(self, t1, t2, t3):
        x2, y2 = self.marker2.x, self.marker2.y
        x3, y3 = self.marker3.x, self.marker3.y
        alpha2 = t2 - np.arctan2(y2, x2)
        alpha3 = t3 - np.arctan2(y3, x3)
        A2 = np.sqrt(x2**2 + y2**2) / np.sin(t2 - t1)
        A3 = np.sqrt(x3**2 + y3**2) / np.sin(t3 - t1)
        tan_theta = (A3 * np.sin(alpha3) - A2 * np.sin(alpha2)) / (A3 * np.cos(alpha3) - A2 * np.cos(alpha2))
        theta = np.arctan(tan_theta)
        omega = -theta
        if omega < 0:
            omega += np.pi

        d1 = (y3 * np.cos(omega + t3) - x3 * np.sin(omega + t3)) / np.sin(t3 - t1)
        d1_ = (y2 * np.cos(omega + t2) - x2 * np.sin(omega + t2)) / np.sin(t2 - t1)
        print("Comparison: ", d1, d1_)
        d2 = (y2 * np.cos(omega + t1) - x2 * np.sin(omega + t1)) / np.sin(t2 - t1)
        d3 = (y3 * np.cos(omega + t1) - x3 * np.sin(omega + t1)) / np.sin(t3 - t1)

        mat_A = np.array([[ 2 * x2, 2 * y2 ],
                          [ 2 * x3, 2 * y3 ]])
        vec_b = np.array([[ d1**2 - d2**2 + x2**2 + y2**2 ],
                          [ d1**2 - d3**2 + x3**2 + y3**2 ]])
        vec_x = np.matmul(np.linalg.inv(mat_A), vec_b)
        x = vec_x[0, 0]
        y = vec_x[1, 0]
        
        self.offset_x = x
        self.offset_y = y
        self.rotation = omega
    
    def __str__(self):
        return "Offset: [%.6f, %.6f], Rotation: %.6f" % (self.offset_x, self.offset_y, self.rotation * 180 / np.pi)

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