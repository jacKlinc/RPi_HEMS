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

device="/dev/ttyACM0"
log="Debug"
c_path = "/home/jimbob/RPi_HEMS/venv3/lib/python3.6/site-packages/python_openzwave/ozw_config"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('openzwave')

# def switch_dev(date_c, demand_c): # date_c is the time it was sampled, demand_c is the usage
#     if ps.is_peak('Month_D.csv', date_c, demand_c): # is it above peak values
#         print("Device is now off")
#         ### switch off
#         return True
#         pyplot.title('Peaks over month')
#         pyplot.xlabel('Time/hours')
#         pyplot.ylabel('Demand/MW')
#         pyplot.show()


for arg in sys.argv:        # no idea
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
    elif arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")

#Define some manager options
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

for i in range(0,300):              # mem usage
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

print("Nodes in network : {}".format(network.nodes_count))
print("------------------------------------------------------------")
for i in range(0,300):              # time taken to connect
    if network.state>=network.STATE_READY:
        print(" done in {} seconds".format(time_started))
        break
    else:
        sys.stdout.write(".")
        time_started += 1
        sys.stdout.flush()
        time.sleep(1.0)


if not network.is_ready:        # if network not ready
    print(".")
    print("Network is not ready but continue anyway")

for node in network.nodes:

    print("------------------------------------------------------------")
    print("{} - Name : {}".format(network.nodes[node].node_id,network.nodes[node].name))
    groups = {}
    for grp in network.nodes[node].groups :
        groups[network.nodes[node].groups[grp].index] = {'label':network.nodes[node].groups[grp].label, 'associations':network.nodes[node].groups[grp].associations}
    print("{} - Groups : {}".format (network.nodes[node].node_id, groups))
    
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
        #values = {}
        for val in network.nodes[node].get_values_for_command_class(cmd) :
            values[network.nodes[node].values[val].object_id] = {
                'label':network.nodes[node].values[val].label,
                'max':network.nodes[node].values[val].max,
                'units':network.nodes[node].values[val].units,
                'data':network.nodes[node].values[val].data,
                }
        print("{} - Values for command class : {} : {}".format(network.nodes[node].node_id,
                                    network.nodes[node].get_command_class_as_string(cmd),
                                    values))

    print("------------------------------------------------------------")
    print("Retrieve switches on the network")
    print("------------------------------------------------------------")
    for val in network.nodes[node].get_switches() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  state: {}".format(network.nodes[node].get_switch_state(val)))

        # influx_write(label, value, nw_id, dev_state, interval_t, node_number, units)

        print("------------------------------------------------------------")
        print("Retrieve sensors on the network")
        print("------------------------------------------------------------")
        for val in network.nodes[node].get_sensors() :
            print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
            print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
            print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
            print("  value: {} {}".format(network.nodes[node].get_sensor_value(val), network.nodes[node].values[val].units))

            influx_insert.influx_write(
                network.nodes[node].values[val].label,          # label
                network.nodes[node].get_sensor_value(val),      # value
                network.nodes[node].values[val].id_on_network,  # nw_id
                network.nodes[node].get_switch_state(val),      # dev_state
                12,                                             # interval
                network.nodes[node],                            # node_number
                network.nodes[node].values[val].units           # units
            )