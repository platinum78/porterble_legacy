#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Serial Handler
* Author        : Susung Park
* Description   : Serial data handler for communication with Arduino
* Version       : Initial release; 07 Jul 2019
********************************************************************************
"""

from serial import Serial
from logging import *

class SerialHandler:
    def __init__(self, config_dict, msg_queue):
        serial_portname = config_dict["serial_portname"]
        baudrate = config_dict["baudrate"]
        self.ser = Serial(serial_portname, baudrate=baudrate)
        self.ser.close()
        self.ser.open()
        print_info("Serial communication initiated.")
    
    def readline(self, timeout=None):
        msg = ""
        char_buf = self.serial.read(timeout=timeout).decode()
        while char_buf != '\n':
            msg += char_buf
            char_buf = self.serial.read(timeout=timeout).decode()
        return msg
    
    def writeline(self, msg, ends_with='\n'):
        if type(msg) != str:
            raise TypeError("Message should be given in string-type.")
        
        if msg[-1] != ends_with:
            msg += ends_with
        
        msg_bytes = msg.encode()
        self.ser.write(msg_bytes)