#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Path Generator
* Author        : Susung Park
* Description   : Path planning and waypoints generation.
* Version       : On development...
********************************************************************************
"""

import serial

class DriverInterface:
    def __init__(self, config_dict):
        