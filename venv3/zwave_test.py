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
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")

options = ZWaveOption(
    device, \
    config_path=c_path, \
    user_path=".", 
    cmd_line=""
)
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(True)
options.set_save_log_level(log)
options.set_logging(False)
options.lock()

#command.ZWaveNodeSwitch.set_switch(8, True)

network = ZWaveNetwork(options, log=None)   # Create a network object
time_started = 0
print("Waiting for network awaked : ")

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
        sys.stdout.flush()
        time.sleep(1.0)


if not network.is_ready:        # if network not ready
    print(".")
    print("Network is not ready but continue anyway")

while True:
    for node in network.nodes:
        groups = {}
        for grp in network.nodes[node].groups :
            groups[network.nodes[node].groups[grp].index] = {'label':network.nodes[node].groups[grp].label, 'associations':network.nodes[node].groups[grp].associations}

        values = {}
        for val in network.nodes[node].values :         # loads values of individual devices into array
            values[network.nodes[node].values[val].object_id] = {
                'label':network.nodes[node].values[val].label,
                'max':network.nodes[node].values[val].max,
                'units':network.nodes[node].values[val].units,
                'data':network.nodes[node].values[val].data_as_string,
            }

        for cmd in network.nodes[node].command_classes:
            print("   ---------   ")
            for val in network.nodes[node].get_values_for_command_class(cmd) :
                values[network.nodes[node].values[val].object_id] = {
                    'label':network.nodes[node].values[val].label,
                    'max':network.nodes[node].values[val].max,
                    'units':network.nodes[node].values[val].units,
                    'data':network.nodes[node].values[val].data,
                    }

        for val in network.nodes[node].get_switches() :
            dev_state = network.nodes[node].get_switch_state(val)

        for val in network.nodes[node].get_sensors() :
            t1 = type(network.nodes[node].values[val].units)
            t2 = type(network.nodes[node].get_sensor_value(val))
            t3 = type(node)
            t4 = type(dev_state)

            #print(network.nodes[node].get_sensor_value(val))
            #print(network.nodes[node].values[val].units)
            #print(t2)

            if t2 is float and t4 is bool:
                influx_insert.influx_write(
                    network.nodes[node].values[val].units,       # units (meas)
                    network.nodes[node].get_sensor_value(val),   # value (field)
                    dev_state,                                     # device state
                    node                                         # node_number (tag)
                )

        #elif t2 is int or t2 is bool:



        
            #now_q = 'select * from W WHERE time > now() - 1s;' # checks value where the units are Watts
            #now_query = influx_insert.influx_q
            #now_points = list(influx_insert.)



            #day_query = 'select value from W WHERE time > now() - 1d;' # checks value where the units are Watts
            #day_power = influx_insert.influx_q(day_query)
            #now_power = influx_insert.influx_q(now_query)

            #print(type(now_power))

                #if (is_peak(day_power, date_chosen, now_query))

                #is_peak(data_series, date_chosen, demand)

#time.sleep(0.96) # sample once a second

