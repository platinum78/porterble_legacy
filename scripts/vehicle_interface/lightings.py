#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Lightings Controller
* Author        : Susung Park
* Description   : Controller for lightings attached to the vehicle.
* Version       : On development...
********************************************************************************
"""

import numpy as np
import threading
import os, sys, time
import RPi.GPIO as gpio

class SwitchEvent(threading.Event):
    def __init__(self):
        super().__init__()

class Lightings:
    LIGHT_FRONT = 1
    LIGHT_REAR = 2
    LIGHT_LEFT = 3
    LIGHT_RIGHT = 4
    TURN_INDICATOR_LEFT = 5
    TURN_INDICATOR_RIGHT = 6

    def __init__(self, config_dict, serial_handler):
        # Get serial handler object.
        self.ser = serial_handler

        # Get pins information from configuration dict.
        self.front_light_pin = config_dict["front_light_pin"]
        self.rear_light_pin = config_dict["rear_light_pin"]
        self.left_light_pin = config_dict["left_light_pin"]
        self.right_light_pin = config_dict["right_light_pin"]
        self.left_indicator_pin = config_dict["left_indicator_pin"]
        self.right_indicator_pin = config_dict["right_indicator_pin"]

        # Get operation parameters from configuration dict.
        self.indicator_blink_interval = config_dict["indicator_blink_interval"]

        # Event objects for triggering lights.
        self.left_indicator_trigger = threading.Event()
        self.right_indicator_trigger = threading.Event()
    
    def grab_pins(self):
        pass
    
    def start_controller(self):
        pass