#!/usr/bin/python3

import os, sys

def identify_arduinos(keyword):
    device_list = os.popen("ls /dev | grep " + keyword).read().strip().split('\n')
    device_dict = {}
    
    for dev in device_list:
        dev_id = os.popen("udevadm info --query=all --name=" + dev + " | grep ID_SERIAL_SHORT").read()
        dev_id = dev_id[dev_id.index("=")+1:].strip()
        device_dict["/dev/" + dev] = dev_id
    
    return device_dict