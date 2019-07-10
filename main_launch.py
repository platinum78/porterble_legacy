#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Main Launcher
* Author        : Susung Park
* Description   : Main launcher for overall control over vehicle.
* Version       : On development...
********************************************************************************
"""

import os, sys, json
import threading
import numpy as np

if __name__ == "__main__":
    from scripts.vehicle_interface.vehicle_interface import VehicleInterface
else:
    from .scripts.vehicle_interface.vehicle_interface import VehicleInterface

def main():
    try:
        interface = VehicleInterface("../config/settings.json")
        interface.start_operation()
    except KeyboardInterrupt:
        interface.stop_operation()