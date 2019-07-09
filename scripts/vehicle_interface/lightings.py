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
from ..utils.logging import *
import RPi.GPIO as gpio

class SwitchEvent(threading.Event):
    def __init__(self):
        super().__init__()
        self.state = False
    
    def on(self):
        """
        Replicate the original threading.Event.set() method,
        just add single command to set self.state to True.
        """
        self.state = True

        with self._cond:
            self._flag = True
            self._cond.notify_all()
    
    def off(self):
        """
        Replicate the original threading.Event.set() method,
        just add single command to set self.state to False.
        """
        self.state = False

        with self._cond:
            self._flag = True
            self._cond.notify_all()

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
    
    def grab_pins(self, simulation=False):
        # Set RPi GPIO to BCM mode.
        gpio.setmode(gpio.BCM)
        
        # Set output pins.
        gpio.setup(self.front_light_pin, gpio.OUT)
        gpio.setup(self.rear_light_pin, gpio.OUT)
        gpio.setup(self.left_indicator_pin, gpio.OUT)
        gpio.setup(self.right_indicator_pin, gpio.OUT)
    
    def front_light_handler(self, e, sigterm):
        while True:
            e.wait()
            # Code for toggling front light.
            e.clear()
    
    def rear_light_handler(self, e, sigterm):
        while True:
            e.wait()
            # Code for toggling rear light.
            e.clear()
    
    def left_indicator_handler(self, e, sigterm):
        while True:
            e.wait()
            # Code for toggling left indicator
            time.sleep(self.indicator_blink_interval)
    
    def right_indicator_handler(self, e, sigterm):
        while True:
            e.wait()
            # Code for toggling right indicator.
            time.sleep(self.indicator_blink_interval)
    
    def start_controller(self, e, sigterm):
        # Create event objects for triggering events.
        self.front_light_event = SwitchEvent()
        self.rear_light_event = SwitchEvent()
        self.left_indicator_event = SwitchEvent()
        self.right_indicator_event = SwitchEvent()

        # Create event objects for sigterm.
        self.front_light_sigterm = threading.Event()
        self.rear_light_sigterm = threading.Event()
        self.left_indicator_sigterm = threading.Event()
        self.right_indicator_sigterm = threading.Event()

        # Create thread objects for each handler.
        self.front_light_thread = threading.Thread(target=self.front_light_handler, daemon=True, args=(self.front_light_event, self.front_light_sigterm))
        self.rear_light_thread = threading.Thread(target=self.rear_light_handler, daemon=True, args=(self.rear_light_event, self.rear_light_sigterm))
        self.left_indicator_thread = threading.Thread(target=self.left_indicator_handler, daemon=True, args=(self.left_indicator_event, self.left_indicator_sigterm))
        self.right_indicator_thread = threading.Thread(target=self.right_indicator_handler, daemon=True, args=(self.right_indicator_event, self.right_indicator_sigterm))

        # Start each thread.
        self.front_light_thread.start()
        self.rear_light_thread.start()
        self.left_indicator_thread.start()
        self.right_indicator_thread.start()

        # Loop until received SIGTERM.
        while not sigterm.is_set():
            e.wait()
            # Code for controlling lightings controller.
            e.clear()
        
        # Trigger SIGTERM of each thread.
        if sigterm.is_set():
            self.front_light_sigterm.set()
            self.rear_light_sigterm.set()
            self.left_indicator_sigterm.set()
            self.right_indicator_sigterm.set()
        
        # Wait until every thread is dead.
        while True:
            active_threads = threading.active_count()
            if active_threads > 0:
                print_info("%d threads still alive. Retry in 1 sec..." % active_threads)
            else:
                break