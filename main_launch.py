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
from scripts.vehicle_interface.vehicle_interface import VehicleInterface
from scripts.utils.logging import *

def main():
    try:
        print_info("Main launcher executed.")
        interface = VehicleInterface("config/settings.json")
        interface_event = threading.Event()
        interface_thread = threading.Thread(name="interface_thread", target=interface.begin, daemon=True, args=(interface_event,))
        interface_thread.start()
        interface_thread.join()
    except KeyboardInterrupt:
        interface.stop()
        sys.exit(0)

if __name__ == "__main__":
    main()