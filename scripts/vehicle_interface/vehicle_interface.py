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

# if __name__ == "__main__":
#     from coordinates import *
#     from datatypes import *
#     from kinematic_controller import *
#     from lightings import *
#     from path_generator import *
#     from utils.logging import *
#     from utils.serial_handler import SerialHandler
# else:
from .coordinates import *
from .datatypes import *
from .kinematic_controller import *
from .lightings import *
from .path_generator import *
from .events import SwitchEvent
from ..utils.logging import *
from ..utils.serial_handler import SerialHandler

class VehicleInterface:
    def __init__(self, config_json_path):
        # Import json data.
        self.json_data = None
        with open(config_json_path, "r") as json_io:
            self.json_data = json.load(json_io)
        
        # Create serial handlers.
        self.serial_arduino_mega = SerialHandler(self.json_data["serial"]["arduino_mega"])
        self.serial_arduino_uno = SerialHandler(self.json_data["serial"]["arduino_uno"])
        
        # Controller objects.
        # self.lightings = Lightings(self.json_data["lightings"])
        self.path_generator = PathGenerator(self.json_data["path_generator"])

        # Print debug message.
        print_info("Vehicle interface initiated.")
    
    def begin(self, e):
        """
        Spawn controller threads and begin operation of vehicle.
        """
        self.lightings_event = SwitchEvent()
        self.lightings_thread = threading.Thread(name="lightings_thread", target=self.lightings.start_controller, daemon=True, args=(self.lightings_event,))

        self.lightings_thread.start()
    
    def stop(self):
        """
        Terminate all controller threads and stop operation of vehicle.
        """
        self.lightings_event.sigterm()