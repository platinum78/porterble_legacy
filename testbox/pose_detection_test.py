import os, sys, cv2, time
sys.path.append("/Users/susung/Documents/02_Projects/porterble/")
from cv2 import aruco
from matplotlib import pyplot as plt
from scripts.vehicle_interface.driver.camera_handler import *
from scripts.vehicle_interface.driver.aruco_detector import *
from scripts.vehicle_interface.driver.path_generator import *
from scripts.vehicle_interface.driver.geometry_datatypes import Pose2D

marker2 = Pose2D(0.28, 0.36, 0)
marker3 = Pose2D(0.56, 0.0, 0)
docking_pose = Pose2D(0.28, 0, 0)
pose_estimator = TripleMarkerPoseEstimator(marker2, marker3, docking_pose)

while True:
    try:
        pose_estimator.compute_pose()
        print(pose_estimator)
        time.sleep(0.1)
    except RuntimeError:
        pass