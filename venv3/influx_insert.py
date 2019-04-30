#!/usr/bin/env python
# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient	

i_client = InfluxDBClient(host='localhost', port=8086) # set Grafana data source to this
i_client.switch_database('ozw4')			# change to database name

def influx_write(units, value, d_state, node):	# passed measurement, 
	points = [{
			"measurement": units,
			"fields": {
				"Value": value,
				"Dev State": d_state
			},
			"tags": {
				"Node": node
			}
		}
	]
	i_client.write_points(points)

def influx_q(new_q):
	return i_client.query(new_q)