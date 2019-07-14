#!/usr/bin/python3

"""
********************************************************************************
* Filename      : Lightings Controller
* Author        : Susung Park
* Description   : Controller for lightings attached to the vehicle.
* Version       : On development...
********************************************************************************
"""

import os, sys, time
import numpy as np
import threading
from ..utils.logging import *
from ..utils.gpio_handler import GPIOHandler
from .events import SwitchEvent
        

class Lightings:
    LIGHT_FRONT = 1
    LIGHT_REAR = 2
    LIGHT_LEFT = 3
    LIGHT_RIGHT = 4
    TURN_INDICATOR_LEFT = 5
    TURN_INDICATOR_RIGHT = 6

    def __init__(self, config_dict, debug=False):
        self.debug = debug

        # Get pins information from configuration dict.
        self.front_light = config_dict["front_light"]
        self.rear_light = config_dict["rear_light"]
        self.left_indicator = config_dict["left_indicator"]
        self.right_indicator = config_dict["right_indicator"]

        # Get operation parameters from configuration dict.
        self.indicator_blink_interval = config_dict["indicator_blink_interval"]
        
        # Print information message.
        print_info("Lightings controller object created at " + str(id(self)) + ".")
    
    def grab_pins(self, simulation=False):
        # Set RPi GPIO to BCM mode.
        gpio.setmode(gpio.BCM)
        
        # Set output pins.
        gpio.setup(self.front_light["pin"], gpio.OUT)
        gpio.setup(self.rear_light["pin"], gpio.OUT)
        gpio.setup(self.left_indicator["pin"], gpio.OUT)
        gpio.setup(self.right_indicator["pin"], gpio.OUT)
        
        # Print information message.
        print_info("GPIO pins initialized.")
    
    def front_light_handler(self, e):
        print_info("Front light handler thread started.")
        while True:
            e.wait()
            if not e.terminate:
                if e.switch_state:
                    gpio.set(self.front_light["pin"], gpio.HIGH)
                    if self.debug: print_info("Front light turned on.")
                else:
                    gpio.set(self.front_light["pin"], gpio.LOW)
                    if self.debug: print_info("Front light turned off.")
                e.clear()
            else:
                return None
    
    def rear_light_handler(self, e):
        print_info("Rear light handler thread started.")
        try:
            while True:
                e.wait()
                if not e.terminate:
                    if e.switch_state:
                        gpio.set(self.front_light["pin"], gpio.HIGH)
                        if self.debug: print_info("Rear light turned on.")
                    else:
                        gpio.set(self.front_light["pin"], gpio.LOW)
                        if self.debug: print_info("Rear light turned off.")
                    e.clear()
                else:
                    return
        except Exception as e:
            print("Error: ", e)
    
    def left_indicator_handler(self, e):
        print_info("Left indicator handler thread started.")
        while True:
            e.wait()
            if not e.terminate:
                gpio.set(self.left_indicator["pin"], gpio.HIGH)
                time.sleep(self.indicator_blink_interval)
                gpio.set(self.left_indicator["pin"], gpio.LOW)
                time.sleep(self.indicator_blink_interval)
            else:
                return
    
    def right_indicator_handler(self, e):
        print_info("Right indicator handler thread started.")
        while True:
            e.wait()
            if not e.terminate:
                gpio.set(self.right_indicator["pin"], gpio.HIGH)
                time.sleep(self.indicator_blink_interval)
                gpio.set(self.right_indicator["pin"], gpio.LOW)
                time.sleep(self.indicator_blink_interval)
            else:
                return
    
    def start_controller(self, e):
        print_info("Lightings controller started.")
        # Create event objects for triggering events.
        self.front_light_event = SwitchEvent()
        self.rear_light_event = SwitchEvent()
        self.left_indicator_event = SwitchEvent()
        self.right_indicator_event = SwitchEvent()

        # Create thread objects for each handler.
        self.front_light_thread = threading.Thread(name="front_light_thread", target=self.front_light_handler, daemon=True, args=(self.front_light_event,))
        self.rear_light_thread = threading.Thread(name="rear_light_thread", target=self.rear_light_handler, daemon=True, args=(self.rear_light_event,))
        self.left_indicator_thread = threading.Thread(name="left_indicator_thread", target=self.left_indicator_handler, daemon=True, args=(self.left_indicator_event,))
        self.right_indicator_thread = threading.Thread(name="right_indicator_thread", target=self.right_indicator_handler, daemon=True, args=(self.right_indicator_event,))

        # Start each thread.
        self.front_light_thread.start()
        self.rear_light_thread.start()
        self.left_indicator_thread.start()
        self.right_indicator_thread.start()

        # Loop until received SIGTERM.
        while True:
            e.wait()
            if not e.terminate:
                e.clear()
        
        # Trigger SIGTERM of each thread.
        if e.terminate:
            self.front_light_event.sigterm()
            self.rear_light_event.sigterm()
            self.left_indicator_event.sigterm()
            self.right_indicator_event.sigterm()
        
        # Wait until every thread is dead.
        while True:
            active_threads = threading.active_count()
            if active_threads > 0:
                print_warn("%d threads still alive. Retry in 1 sec..." % active_threads)
            else:
                break
        
        print_info("All lightings subthreads are terminated.")