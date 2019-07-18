#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Lightings Controller
* Author        : Susung Park
* Description   : Controller for lightings attached to the vehicle.
* Version       : On development...
********************************************************************************
"""

import os, sys, time, struct
import numpy as np
import threading
# from ..utils.logging import *
# from ..utils.gpio_handler import GPIOHandler
# from .events import SwitchEvent

sys.path.append("/Users/susung/Documents/02_Projects/porterble")
from serial.serialutil import SerialException
from scripts.utils.serial_handler import SerialHandler

config_dict = {
    "port_name": "/dev/cu.usbmodem1423301",
    "baudrate": 57600
}

class Lightings:
    LIGHT_FRONT = 1
    LIGHT_REAR = 2
    LIGHT_LEFT = 3
    LIGHT_RIGHT = 4
    TURN_INDICATOR_LEFT = 5
    TURN_INDICATOR_RIGHT = 6

    def __init__(self, config_dict, debug=False):
        self.ser = SerialHandler(config_dict=config_dict, debug=True)
        msg = self.ser.readbytes()
        print(msg)
        if msg != "\x01":
            raise SerialException("System not properly set.")
        
        msg = struct.pack("Bc", 0b00100000, b'\n')

        self.ser.writebytes(msg)
        msg = self.ser.readline()
        print(msg)
        print("Hello, world!")

if __name__ == "__main__":
    lightings = Lightings(config_dict, debug=True)