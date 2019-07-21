#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Device Interfaces
* Author        : Susung Park
* Description   : Device interface classes for each device.
* Version       : Initial release; 07 Jul 2019
********************************************************************************
"""

class ArduinoInterface:
    def __init__(self):
        self.serial = None
        self.id = None
    
class ArduinoInterface_driver(ArduinoInterface):
    def __init__(self):
        super().__init__()
        self.encoder_position = [0] * 4
        self.encoder_velocity = [0] * 4
    
    def publish_encoder_position(self, n1, n2, n3, n4):
        self.encoder_position = [n1, n2, n3, n4]
    
    def publish_encoder_velocity(self, n1, n2, n3, n4):
        self.encoder_velocity = [n1, n2, n3, n4]

class ArduinoInterface_watchdog(ArduinoInterface):
    def __init__(self, config_dict):
        super().__init__()
        self.sensor_cnt = config_dict["sensor_cnt"]
        self.range = [0] * self.sensor_cnt
    
    def publish_sonar_range(self, *args):
        self.range = args

class ArduinoInterface_torch(ArduinoInterface):
    def __init__(self):
        super().__init__()
        