#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Camera Handler
* Author        : Susung Park
* Description   : Camera handler.
* Version       : On development...
********************************************************************************
"""

import os, sys, threading, time
import cv2
from cv2 import aruco
import numpy as np

class CameraHandler:
    def __init__(self, angle_horizontal, angle_vertical):
        self.alpha = angle_horizontal / 2
        self.beta = angle_vertical / 2
        self.camera = cv2.VideoCapture(0)
        self.width = int(self.camera.get(3))
        self.height = int(self.camera.get(4))
    
    def start_stream(self):
        aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
        parameters =  aruco.DetectorParameters_create()
        while True:
            try:
                ret, frame = self.camera.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
                if ids is not None:
                    for idx in range(len(ids)):
                        marker_id = ids[idx][0]
                        if marker_id in [1, 2, 3]:
                            centerpoint = np.int32(np.average(corners[idx][0], axis=0))
                            print("Marker %d: Centerpoint at [%.6f, %.6f]" % (marker_id, centerpoint[0], centerpoint[1]))
                # frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
                # cv2.imshow("image", frame_markers)
                cv2.waitKey(1)
            except KeyboardInterrupt:
                break
    
    def get_frame(self):
        ret, frame = self.camera.read()
        return frame
    
    def pixel_to_spherical_angle(self, col, row):
        y = self.width / 2 - col
        z = self.height / 2 - row

        d1 = self.width / (2 * np.tan(self.alpha))
        d2 = self.height / (2 * np.tan(self.beta))

        d = (d1 + d2) / 2

        theta = np.arctan(y / d)
        phi = np.arctan(z / d * np.cos(theta))

        return theta, phi

if __name__ == "__main__":
    camera = CameraHandler(1.1927, 0.7053)
    camera.start_stream()