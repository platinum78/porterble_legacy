#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Event Objects
* Author        : Susung Park
* Description   : Custom event objects for specific uses.
* Version       : Initial release; 07 Jul 2019
********************************************************************************
"""

import threading

class SwitchEvent(threading.Event):
    """
    Event object for low-level controllers.
    This event has [switch_state] condition and [terminate] condition.
    """
    def __init__(self):
        super().__init__()
        self.switch_state = False
        self.terminate = False
    
    def switch_on(self):
        self.switch_state = True
        self.set()
    
    def switch_off(self):
        self.switch_state = False
        self.set()
    
    def sigterm(self):
        self.terminate = True
        self.set()
