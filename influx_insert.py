#!/usr/bin/env python
# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient	

i_client = InfluxDBClient(host='localhost', port=8086) # set Grafana data source to this
i_client.switch_database('ozw')			# change to database name

def influx_write(label, value, nw_id, dev_state, interval_t, node_number, units):	# passed measurement, 
	points = [{
			"measurement": label,
			"fields": {
				"Value": value,
				"NW ID": nw_id,
				"Device State": dev_state,
				"Interval": interval_t,
				"Node Number": node_number
			},
			"tags": {
				"Units": units
			}
		}
	]
	i_client.write_points(points)