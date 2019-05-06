import logging
import sys, os
import resource
#logging.getLogger('openzwave').addHandler(logging.NullHandler())
#logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('openzwave')
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time
import datetime as dt

device="/dev/ttyACM0"
log="Debug"
c_path="/home/jimbob/RPi_HEMS/venv3/lib/python3.6/site-packages/python_openzwave/ozw_config"

options = ZWaveOption(device, \
config_path=c_path, \
user_path=".", cmd_line="")

options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(True)
options.set_save_log_level(log)
options.set_logging(False)
options.lock()

#def get_val():
time_started = 0
for arg in sys.argv:
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
    elif arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")

network = ZWaveNetwork(options, log=None)

print("Retrieve switches on the network")
print("------------------------------------------------------------")
#dev_state = False
values = {}
for node in network.nodes:
    for val in network.nodes[node].get_switches() :
        print("  state: {}".format(network.nodes[node].get_switch_state(val)))
        #dev_state = network.nodes[node].get_switch_state(val)
print("------------------------------------------------------------")


print("Retrieve sensors on the network")
print("------------------------------------------------------------")
values = {}
ret_vals = []
t_val=0
for node in network.nodes:
    for val in network.nodes[node].get_sensors() :
        # print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
        # print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
        # print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
        #print("  value: {} {}".format(network.nodes[node].get_sensor_value(val), network.nodes[node].values[val].units))
        #t_val=val
        temp_v = network.nodes[node].get_sensor_value(val)
        if type(temp_v) == float:
            ret_vals.append(temp_v)
    print(ret_vals)
    
print("------------------------------------------------------------")
#print(network.nodes[2].get_sensors())

#return ret_vals#, dev_state