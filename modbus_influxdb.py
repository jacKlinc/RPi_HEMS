from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient
from influxdb import InfluxDBClient

import time
import datetime
import json

print "Start ModbusTcpClient"

client = ModbusTcpClient( "192.168.0.57", 
                         timeout=3,
                         RetryOnEmpty=True,
                         retries=3,
                         port=502)
print "Connect"
client.connect()

try:
  influx_client = InfluxDBClient("192.168.0.57",
                               8086,
                               "user",
                               "pi",
                               "power_db",
                               ssl=True,
                               verify_ssl=False)
except:
  influx_client = None

bus = json.loads(modmap.scan)
slave_addr = 0x01                       # device addr

def load_registers(type,start,COUNT=100):
  try:
    if type == "read":
      rr = client.read_input_registers(int(start), 
                                       count=int(COUNT), 
                                       unit=slave_addr)
    elif type == "holding":
      rr = client.read_holding_registers(int(start), 
                                         count=int(COUNT), 
                                         unit=slave_addr)
    for num in range(0, int(COUNT)):
      run = int(start) + num + 1
      if type == "read" and modmap.read_register.get(str(run)):
        if '_10' in modmap.read_register.get(str(run)):
          inverter[modmap.read_register.get(str(run))[:-3]] = float(rr.registers[num])/10
        else:
          inverter[modmap.read_register.get(str(run))] = rr.registers[num]
      elif type == "holding" and modmap.holding_register.get(str(run)):
        inverter[modmap.holding_register.get(str(run))] = rr.registers[num]
  except Exception as err:
    print "[ERROR] %s" % err

def publish_influx(metrics):
  target=flux_client.write_points([metrics])
  print "[INFO] Sent to InfluxDB"