#!/usr/bin/env python
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
import peak_shave as ps
import datetime as dt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('openzwave')

device="/dev/ttyACM0"
log="Debug"

def switch_dev(date_c, demand_c): # date_c is the time it was sampled, demand_c is the usage
    if ps.is_peak('Month_D.csv', date_c, demand_c): # is it above peak values
        print("Device is now off")
        ### switch off
        return True



'''
> need to pass a datetime and return yes/no
> this will update its timestamp every loop
> to be true it needs to be above a certain val
> that val could be within 5% of average peak value that day
> so need to find all peaks for that day
> find their average---if demand.now >= avg: true

Task1:
get_peaks(datetime): takes a datetime and for that day returns all peaks

Task2:
avg(peaks): find average of that array of peaks

Task3:
get_peak_now(datetime): gets demand at time asked

''' 



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
    config_path="../ozw_config/config", \
    user_path=".", 
        cmd_line=""
)
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(True)
options.set_save_log_level(log)
options.set_logging(False)
options.lock()

print("Memory use : {} Mo".format( (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0))) # why is 1024?

network = ZWaveNetwork(options, log=None)   # Create a network object
time_started = 0
print("Waiting for network awaked : ")

for i in range(0,300):              # mem usage
    if network.state>=network.STATE_AWAKED:
        print(" done")
        print("Memory use : {} Mo".format( (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)))
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time_started += 1
        time.sleep(1.0)
if network.state<network.STATE_AWAKED:
    print(".")
    print("Network is not awake but continue anyway")

print("Network home id : {}".format(network.home_id_str))
print("Controller node id : {}".format(network.controller.node.node_id))
print("Nodes in network : {}".format(network.nodes_count))
print("------------------------------------------------------------")
print("Waiting for network ready : ")
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


print("Memory use : {} Mo".format( (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)))
if not network.is_ready:        # if network not ready
    print(".")
    print("Network is not ready but continue anyway")
'''
> Controller capabilities
print("------------------------------------------------------------")
print("Controller capabilities : {}".format(network.controller.capabilities))
print("Controller node capabilities : {}".format(network.controller.node.capabilities))
print("Nodes in network : {}".format(network.nodes_count))
print("Driver statistics : {}".format(network.controller.stats))
print("------------------------------------------------------------")'''
for node in network.nodes:

    print("------------------------------------------------------------")
    print("{} - Name : {}".format(network.nodes[node].node_id,network.nodes[node].name))
    print("{} - Manufacturer name / id : {} / {}".format(network.nodes[node].node_id,network.nodes[node].manufacturer_name, network.nodes[node].manufacturer_id))
    print("{} - Product name / id / type : {} / {} / {}".format(network.nodes[node].node_id,network.nodes[node].product_name, network.nodes[node].product_id, network.nodes[node].product_type))
    print("{} - Version : {}".format(network.nodes[node].node_id, network.nodes[node].version))
    print("{} - Command classes : {}".format(network.nodes[node].node_id,network.nodes[node].command_classes_as_string))
    print("{} - Capabilities : {}".format(network.nodes[node].node_id,network.nodes[node].capabilities))
    print("{} - Neighbours : {}".format(network.nodes[node].node_id,network.nodes[node].neighbors))
    print("{} - Can sleep : {}".format(network.nodes[node].node_id,network.nodes[node].can_wake_up()))
    groups = {}
    for grp in network.nodes[node].groups :
        groups[network.nodes[node].groups[grp].index] = {'label':network.nodes[node].groups[grp].label, 'associations':network.nodes[node].groups[grp].associations}
    print("{} - Groups : {}".format (network.nodes[node].node_id, groups))
    values = {}
    for val in network.nodes[node].values :         # loads values of individual devices into array
        values[network.nodes[node].values[val].object_id] = {
            'label':network.nodes[node].values[val].label,
            'help':network.nodes[node].values[val].help,
            'command_class':network.nodes[node].values[val].command_class,
            'max':network.nodes[node].values[val].max,
            'min':network.nodes[node].values[val].min,
            'units':network.nodes[node].values[val].units,
            'data':network.nodes[node].values[val].data_as_string,
            'ispolled':network.nodes[node].values[val].is_polled
            }
    for cmd in network.nodes[node].command_classes:
        print("   ---------   ")
        values = {}
        for val in network.nodes[node].get_values_for_command_class(cmd) :
            values[network.nodes[node].values[val].object_id] = {
                'label':network.nodes[node].values[val].label,
                'help':network.nodes[node].values[val].help,
                'max':network.nodes[node].values[val].max,
                'min':network.nodes[node].values[val].min,
                'units':network.nodes[node].values[val].units,
                'data':network.nodes[node].values[val].data,
                'data_str':network.nodes[node].values[val].data_as_string,
                'genre':network.nodes[node].values[val].genre,
                'type':network.nodes[node].values[val].type,
                'ispolled':network.nodes[node].values[val].is_polled,
                'readonly':network.nodes[node].values[val].is_read_only,
                'writeonly':network.nodes[node].values[val].is_write_only,
                }
        print("{} - Values for command class : {} : {}".format(network.nodes[node].node_id,
                                    network.nodes[node].get_command_class_as_string(cmd),
                                    values))
    print("------------------------------------------------------------")

print("------------------------------------------------------------")
print("Driver statistics : {}".format(network.controller.stats))
print("------------------------------------------------------------")

print("------------------------------------------------------------")
print("Try to autodetect nodes on the network")
print("------------------------------------------------------------")
print("Nodes in network : {}".format(network.nodes_count))
print("------------------------------------------------------------")

print("Retrieve switches on the network")
print("------------------------------------------------------------")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_switches() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  state: {}".format(network.nodes[node].get_switch_state(val)))

print("Retrieve sensors on the network")
print("------------------------------------------------------------")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_sensors() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  value: {} {}".format(network.nodes[node].get_sensor_value(val), network.nodes[node].values[val].units))
        #switch_dev(dt.datetime.now(), network.nodes[node].get_sensor_value(val))

print("------------------------------------------------------------")

print("Retrieve thermostats on the network")
print("------------------------------------------------------------")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_thermostats() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  value: {} {}".format(network.nodes[node].get_thermostat_value(val), network.nodes[node].values[val].units))
        # influx_insert.influx_write(
        #     node,                                           # int
        #     network.nodes[node].get_thermostat_value(val),  # N/A
        #     network.nodes[node].values[val].id_on_network,  # home_id.node_id.command_class.instance.index??
        #     network.nodes[node].get_switch_all_state(val),  # bool
        #     network.nodes[node].values[val].units           # string
        # )
print("------------------------------------------------------------")

print("Retrieve switches all compatibles devices on the network    ")
print("------------------------------------------------------------")
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_switches_all() :
        print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        print("  value / items:  / {}".format(network.nodes[node].get_switch_all_item(val), network.nodes[node].get_switch_all_items(val)))
        print("  state: {}".format(network.nodes[node].get_switch_all_state(val)))
print("------------------------------------------------------------")

print("------------------------------------------------------------")
print("Driver statistics : {}".format(network.controller.stats))
print("Driver label : {}".format(network.controller.get_stats_label('retries')))
print("------------------------------------------------------------")

print("------------------------------------------------------------")
print("Stop network")
print("------------------------------------------------------------")
network.stop()
print("Memory use : {} Mo".format( (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)))