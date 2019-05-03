import logging
import sys, os
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
import six
if six.PY3:
    from pydispatch import dispatcher
else:
    from louie import dispatcher

device="/dev/ttyACM0"
log="None"
c_path = "/home/jimbob/RPi_HEMS/venv3/lib/python3.6/site-packages/python_openzwave/ozw_config"


#Define some manager options
options = ZWaveOption(device, \
  config_path=c_path, \
  user_path=".", cmd_line="")
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level(log)
options.set_logging(True)
options.lock()

def louie_network_started(network):
    print(".")

def louie_network_failed(network):
    print("Hello from network : can't load :(.")

def louie_network_ready(network):
    print(".")
    #print("Hello from network : my controller is : {}".format(network.controller))
    dispatcher.connect(louie_node_update, ZWaveNetwork.SIGNAL_NODE)
    dispatcher.connect(louie_node_event, ZWaveNetwork.SIGNAL_NODE_EVENT)
    dispatcher.connect(louie_value_update, ZWaveNetwork.SIGNAL_VALUE)

def louie_network_awake(network):
    print(".")

def louie_node_update(network, node):
    print(".")

def louie_value_update(network, node, value):
    print(".")

def louie_node_event(**kwargs):
    print(".")

#Create a network object
network = ZWaveNetwork(options, autostart=False)

#We connect to the louie dispatcher
dispatcher.connect(louie_network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
dispatcher.connect(louie_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
dispatcher.connect(louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
dispatcher.connect(louie_network_awake, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)

#x=0
while True:

    network.start()

    for i in range(0,90):
        if network.state>=network.STATE_READY:
            #print("***** Network is ready")
            print("\n")
            my_node = network.nodes[2]

            kWh = 72057594076495874        # reg locations
            W = 72057594076496002 
            V = 72057594076496130 
            A = 72057594076496194 
            state = 72057594076496384 
            print("kWh: {}{} ".format(my_node.get_sensor_value(kWh), my_node.values[kWh].units))

            # influx_insert.influx_write(
            #     my_node.get_sensor_value(,       # units (meas)
            #     network.nodes[node].get_sensor_value(val),   # value (field)
            #     True,                                        # device state
            #     node                                         # node_number (tag)
            # )
            time.sleep(1.0)
            break
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1.0)
    
    network.stop()