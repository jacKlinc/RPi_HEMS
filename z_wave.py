# pip install python-zwave
# pip install Louie
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
from openzwave.command import ZWaveCommand
import time
import six
if six.PY3:
    from pydispatch import dispatcher
else:
    from louie import dispatcher

device="/dev/ttyACM0"
log="None"

#Define some manager options
options = ZWaveOption(device, \ 
  config_path="/usr/etc/openzwave/", \
  user_path=".", cmd_line="") # ZWaveOption(device=None, config_path=None, user_path=None, cmd_line=None)
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level(log)
options.set_logging(True)
options.lock()

def louie_network_started(network):
    print("Hello from network : I'm started : homeid {:08x} - {} nodes were found.".format(network.home_id, network.nodes_count))

def louie_network_failed(network):
    print("Hello from network : can't load :(.")

def louie_network_ready(network):
    print("Hello from network : I'm ready : {} nodes were found.".format(network.nodes_count))
    print("Hello from network : my controller is : {}".format(network.controller))
    dispatcher.connect(louie_node_update, ZWaveNetwork.SIGNAL_NODE)
    dispatcher.connect(louie_node_event, ZWaveNetwork.SIGNAL_NODE_EVENT)
    dispatcher.connect(louie_value_update, ZWaveNetwork.SIGNAL_VALUE)

def louie_network_awake(network):
    print("Hello from network : I'm awake")

def louie_node_update(network, node):
    print("Hello from node : {}.".format(node))

def louie_value_update(network, node, value):
    print("Hello from value : {}.".format( value ))

def louie_node_event(**kwargs):
    print("Hello from node event : {}.".format( kwargs ))

#Create a network object
network = ZWaveNetwork(options, autostart=False)

#We connect to the louie dispatcher
dispatcher.connect(louie_network_started, ZWaveNetwork.SIGNAL_NETWORK_STARTED)
dispatcher.connect(louie_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
dispatcher.connect(louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
dispatcher.connect(louie_network_awake, ZWaveNetwork.SIGNAL_NETWORK_AWAKED)

network.start()

#We wait for the network.
print("***** Waiting for network to become ready : ")
for i in range(0,90):
    if network.state>=network.STATE_READY:
        print("***** Network is ready")
        break
    else:
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1.0)

all_sensors = command.ZWaveNodeSensor.get_sensors() # returns a dictionary 
for x in all_sensors:
    print (x)
    for y in all_sensors[x]:
        print (y,':',all_sensors[x][y])

#sensor1 = command.ZWaveNodeSensor.get_sensors(id) # returns a variable