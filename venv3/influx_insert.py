#!/usr/bin/env python
# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient	

i_client = InfluxDBClient(host='localhost', port=8086) # set Grafana data source to this
i_client.switch_database('ozw')			# change to database name

def influx_write(units, value, nw_id, dev_state, interval_t, node_number):	# passed measurement, 
	points = [{
			"measurement": units,
			"fields": {
				"Value": value,
				"NW ID": nw_id,
				"Device State": dev_state,
				"Interval": interval_t
			},
			"tags": {
				"Units": node_number
			}
		}
	]
	i_client.write_points(points)