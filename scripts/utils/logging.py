"""
********************************************************************************
* Filename      : Logging
* Author        : Susung Park
* Description   : Formatted logging for uniform printouts.
* Version       : Initial release; 07 Jul 2019
********************************************************************************
"""

import time

def print_info(msg):
    print("[ INFO ] %.6f :" % time.time(), msg)

def print_warn(msg):
    print("[ WARN ] %.6f :" % time.time(), msg)

def print_err(msg):
    print("[ ERR  ] %.6f :" % time.time(), msg)