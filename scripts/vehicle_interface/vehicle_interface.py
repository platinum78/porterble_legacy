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
from .coordinates import *
from .geometry_datatypes import *
from .kinematic_controller import *
from .lightings import *
from .path_generator import *
from .events import SwitchEvent
from ..utils.logging import *
from ..utils.serial_handler import SerialHandler
from ..utils.device_identifier import *
from .device_interface import *


class VehicleInterface:
    def __init__(self, config_json_path):
        # Import json data.
        self.json_data = None
        with open(config_json_path, "r") as json_io:
            self.json_data = json.load(json_io)
        
        # Create Arduino interfaces.
        self.torch = ArduinoInterface_torch()
        self.driver = ArduinoInterface_driver()
        self.watchdog = ArduinoInterface_watchdog()
        
        # Create serial handlers.
        self.torch.serial = SerialHandler(self.json_data["serial"]["torch"])
        self.driver.serial = SerialHandler(self.json_data["serial"]["driver"])
        self.watchdog.serial = SerialHandler(self.json_data["serial"]["watchdog"])

        # Create event objects for handlers.
        self.torch_event = SwitchEvent()
        self.driver_event = SwitchEvent()
        self.watchdog_event = SwitchEvent()

        # Controller objects.
        # self.lightings = Lightings(self.json_data["lightings"])
        self.path_generator = PathGenerator(self.json_data["path_generator"])

        # Print debug message.
        print_info("Vehicle interface initiated.")
    
    def begin(self, e):
        """
        Spawn controller threads and begin operation of vehicle.
        """

        # Create event objects for each thread.
        self 
        self.lightings_event = SwitchEvent()
        self.lightings_thread = threading.Thread(name="lightings_thread", target=self.lightings.start_controller, daemon=True, args=(self.lightings_event,))

        self.lightings_thread.start()
    
    def stop(self):
        """
        Terminate all controller threads and stop operation of vehicle.
        """
        self.lightings_event.sigterm()