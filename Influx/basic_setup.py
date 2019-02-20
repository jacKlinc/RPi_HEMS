#!/usr/bin/env python
from influxdb import InfluxDBClient
client = InfluxDBClient(host='localhost', port=8086)
client.
#client.get_list_database()          # prints database

# json_example = [
#     {
#         "measurement": "power",
#         "tags": {
#             "kWH":  123.2
#             "V":    12
#         },
#         "time": "2019-02-14T9:01:00Z"
#         "fields": {
#             "current": 0.4
#         }
#     }
# ]

json_body = [
    {
        "measurement": "brushEvents",
        "tags": {
            "user": "Carol",
            "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
        },
        "time": "2018-03-28T8:01:00Z",
        "fields": {
            "duration": 127
        }
    }
]
client.write_points(json_body)


for point in points:
    print("Time: %s, Duration: %i" % (point['time'], point['duration']))