#!/usr/bin/env python
from influxdb import InfluxDBClient
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('Modbus1')                       # choose which DB
'''Points consist of time (a timestamp), a measurement (“cpu_load”, for example), 
at least one key-value field (the measured value itself, e.g. “value=0.64”, or 
“temperature=21.2”), and zero to many key-value tags containing any metadata about 
the value (e.g. “host=server01”, “region=EMEA”, “dc=Frankfurt”).

Conceptually you can think of a measurement as an SQL table, where the 
primary index is always time. tags and fields are effectively columns 
in the table. tags are indexed, and fields are not. The difference is that, 
with InfluxDB, you can have millions of measurements, you don’t have to 
define schemas up-front, and null values aren’t stored. '''

client.writePoints([
		{
		  measurement: 'Modbus_D', 
		  tags:   { Device: "PM311" },
		  fields: { M_Type: V_Avg, Value: AverageVoltage },
		}
])