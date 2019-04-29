#!/usr/bin/env python
# -*- coding: utf-8 -*-
from influxdb import InfluxDBClient	

i_client = InfluxDBClient(host='localhost', port=8086) # set Grafana data source to this
i_client.switch_database('test3')			# change to database name

def influx_write(node_type, value, nw_id, dev_state, units):	# passed measurement, 
	points = [{
            "measurement": node_type,
            "fields": {
                "Value": value,
                "NW ID": nw_id,
                "Device State": dev_state
			},
			"tags": {
				"Units": units
			}
        }
    ]
    if(i_client.write_points(points)):
        print("works")
    else:
        print("no works")