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
import datetime as dt
import six
import influx_insert as in_is
if six.PY3:
    from pydispatch import dispatcher
else:
    from louie import dispatcher
import peak_shave as ps

device="/dev/ttyACM0"
log="None"
c_path = "/home/jimbob/RPi_HEMS/venv3/lib/python3.6/site-packages/python_openzwave/ozw_config"

options = ZWaveOption(
  device, \
  config_path=c_path, \
  user_path=".", 
  cmd_line=""
  )
options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False)
options.set_save_log_level(log)
options.set_logging(True)
options.set_poll_interval(10)
options.set_interval_between_polls(True)
options.lock()

def louie_network_failed(network):
    print("Hello from network : can't load :(.")

def louie_network_ready(network):
    ZWaveNetwork.SIGNAL_NODE
    ZWaveNetwork.SIGNAL_NODE_EVENT
    ZWaveNetwork.SIGNAL_VALUE

network = ZWaveNetwork(options, autostart=False)

ZWaveNetwork.SIGNAL_NETWORK_STARTED  # connect to the louie dispatcher
dispatcher.connect(louie_network_failed, ZWaveNetwork.SIGNAL_NETWORK_FAILED)
dispatcher.connect(louie_network_ready, ZWaveNetwork.SIGNAL_NETWORK_READY)
ZWaveNetwork.SIGNAL_NETWORK_AWAKED

while True:
    x = dt.datetime.now()
    network.start()

    for i in range(0,90):
        if network.state>=network.STATE_READY:
            print("\n")
            my_node = network.nodes[2]

            kWh = 72057594076495874        # reg locations
            W = 72057594076496002 
            V = 72057594076496130 
            A = 72057594076496194 
            state = 72057594076496384 
            for val in my_node.get_sensors():
                t_val = my_node.get_sensor_value(val)
                if type(t_val) is float:
                    in_is.influx_write(
                        my_node.values[val].units,
                        t_val,
                        my_node.get_sensor_value(state),
                        2
                    )
                    #print("{}{}".format(t_val, my_node.values[val].units))
                time.sleep(0.1)

            # for val in my_node.get_switches():
            #     print(my_node.get_switch_value(val))

            this_hour = in_is.to_panda() # converts query to Panda Dataframe
            control = ps.is_peak(this_hour, my_node.get_sensor_value(W))

            if control is True:
                #### turn off plug
                print("Peak")
            else:
                print("No peak")


            time.sleep(0.5)
            break
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1.0)

    y = dt.datetime.now() - x
    print(y)
    network.stop()

'''
******   TO DO   ***********
> Write to plug

                for cmd in my_node.command_classes:
                    print("   ---------   ")
                    #print("cmd = {}".format(cmd))
                    values = {}
                    for val in my_node.get_values_for_command_class(cmd) :
                        values[my_node.values[val].object_id] = {
                            'label':my_node.values[val].label,
                            'help':my_node.values[val].help,
                            'max':my_node.values[val].max,
                            'min':my_node.values[val].min,
                            'units':my_node.values[val].units,
                            'data':my_node.values[val].data,
                            'data_str':my_node.values[val].data_as_string,
                            'genre':my_node.values[val].genre,
                            'type':my_node.values[val].type,
                            'ispolled':my_node.values[val].is_polled,
                            'readonly':my_node.values[val].is_read_only,
                            'writeonly':my_node.values[val].is_write_only,
                            }
                    print("{} - Values for command class : {} : {}".format(my_node.node_id,
                                                my_node.get_command_class_as_string(cmd),
                                                values))

'''
