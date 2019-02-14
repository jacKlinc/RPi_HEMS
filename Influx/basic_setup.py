#!/usr/bin/env python
client = InfluxDBClient(host='localhost', port=8086)
client.create_database('myDB')
client.get_list_database()          # prints database

json_example = [
    {
        "measurement": "power",
        "tags": {
            "kWH":  123.2
            "V":    12
        },
        "time": "2019-02-14T9:01:00Z"
        "fields": {
            "current": 0.4
        }
    }
]
client.write_points(json_example)

client.query('SELECT "current" FROM "myDB"."autogen"."power" WHERE time > now() - 4d GROUP BY "kWH"')
