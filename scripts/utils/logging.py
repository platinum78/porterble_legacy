"""
********************************************************************************
* Filename      : Logging
* Author        : Susung Park
* Description   : Formatted logging for uniform printouts.
* Version       : Initial release; 07 Jul 2019
********************************************************************************
"""

import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_info(msg):
    print("[ INFO ] %.6f :" % time.time(), msg)

def print_warn(msg):
    print(bcolors.WARNING + "[ WARN ] %.6f :" % time.time() + " " + msg + bcolors.ENDC)

def print_err(msg):
    print(bcolors.FAIL + "[ ERR  ] %.6f :" % time.time() + " " + msg + bcolors.ENDC)