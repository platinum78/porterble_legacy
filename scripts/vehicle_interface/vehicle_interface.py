#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Serial Handler
* Author        : Susung Park
* Description   : Serial data handler for communication with Arduino
* Version       : Initial release; 07 Jul 2019
********************************************************************************
"""

import os, sys, time, json, threading

if __name__ == "__main__":
    from coordinates import *
    from datatypes import *
    from kinematic_controller import *
    from lightings import *
    from path_generator import *
    from utils.logging import *
    from utils.serial_handler import SerialHandler
else:
    from .coordinates import *
    from .datatypes import *
    from .kinematic_controller import *
    from .lightings import *
    from .path_generator import *
    from .utils.logging import *
    from .utils.serial_handler import SerialHandler

class VehicleInterface:
    def __init__(self, config_json_path):
        # Import json data.
        self.json_data = None
        with open(config_json_path, "r") as json_io:
            self.json_data = json.load(json_io)

        # Controller objects.
        self.lightings = Lightings(self.json_data["lightings"])
        self.path_generator = PathGenerator(self.json_data["path_generator"])
    
    def start_operation(self, terminate_event):
        """
        Spawn controller threads and begin operation of vehicle.
        """
        pass