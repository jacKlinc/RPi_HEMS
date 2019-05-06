#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import sys, os
import resource
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time
import ctypes
import influx_insert
from influxdb import InfluxDBClient	
#import peak_shave as ps
import datetime as dt
import peak_shave as ps

device="/dev/ttyACM0"
log="Debug"
c_path = "/home/jimbob/RPi_HEMS/venv3/lib/python3.6/site-packages/python_openzwave/ozw_config"

for arg in sys.argv:        # no idea
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
    elif arg.startswith("--help"):
        print("help : ")

options = ZWaveOption(
    device, \
    config_path=c_path, \
    user_path=".", 
    cmd_line=""
)
options.set_poll_interval=10
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(True)
options.set_save_log_level(log)
options.set_logging(False)
options.lock()

#command.ZWaveNodeSwitch.set_switch(8, True)

network = ZWaveNetwork(options, autostart=False, log=None)   # Create a network object

time_started = 0
print("Waiting for network awaked : ")

network.start()
for i in range(0,300):              
    if network.state>=network.STATE_AWAKED:
        print(" done")
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time_started += 1
        time.sleep(1.0)

if network.state<network.STATE_AWAKED:
    print(".")
    print("Network is not awake but continue anyway")


for i in range(0,300):              # time taken to connect
    if network.state>=network.STATE_READY:
        break
    else:
        sys.stdout.write(".")
        time_started += 1
        sys.stdout.flush() ##### how I/O buffers data
        time.sleep(1.0)


if not network.is_ready:        # if network not ready
    print(".")
    print("Network is not ready but continue anyway")

x=0
while x <= 100: 
    #network.set_poll_interval(milliseconds=500, bIntervalBetweenPolls=True)
    values = {}
    for node in network.nodes:
        for val in network.nodes[node].get_switches() :
            dev_state = network.nodes[node].get_switch_state(val)

    values = {}
    for node in network.nodes:
        for val in network.nodes[node].get_sensors() :  # return self.values[value_id].data
            t_units = network.nodes[node].values[val].units
            t_val = network.nodes[node].get_sensor_value(val)
            t_node = node    
            #print(type(t_val))
            print("{} {}".format(t_val, t_units))

        # print(values, end=' ')
    print("------------------")   
    print (network.get_poll_interval())
    x+=1
    #sys.stdout.flush()
    time.sleep(5)

#time.sleep(0.96) # sample once a secon

'''
> Basically, at val (location), all values are read off all sensors then iterated throgh
and printed.
> 72057594076495874 is the index so add if statement and based on type and unit, save
to variable then insert to Influx outside of loop 
'''
