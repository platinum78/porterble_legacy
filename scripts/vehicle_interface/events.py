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
    
    def trigger_sigterm(self):
        self.terminate = True
        self.set()


class LightingEvent(threading.Event):
    def __init__(self):
        super().__init__()
        self.dev_id = 0
        self.switch_state = False
        self.terminate = False

    def set_device(self, dev_id, swtich_state):
        self.dev_id = dev_id
        self.switch_state = swtich_state
        self.terminate = False
        self.set()
    
    def trigger_sigterm(self):
        self.terminate = True
        self.set()