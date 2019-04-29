jimbob@Bob:~$ sudo influxd&
[1] 25923
jimbob@Bob:~$ sudo influx
Connected to http://localhost:8086 version 1.7.6
InfluxDB shell version: 1.7.6
Enter an InfluxQL query
> show databases
name: databases
name
----
_internal
test
openhab_db
> CREATE USER admin WITH PASSWORD 'password1' WITH ALL PRIVILEGES
> GRANT ALL ON openhab_db TO admin
> CREATE USER grafana WITH PASSWORD 'password1'
> CREATE USER openhab WITH PASSWORD 'password1'
> GRANT READ ON openhab_db TO grafana
> exit


sudo nano /etc/openhab2/services/influxdb.cfg
# The database URL, e.g. http://127.0.0.1:8086 or https://127.0.0.1:8084 .
# Defaults to: http://127.0.0.1:8086
url=http://localhost:8086

# The name of the database user, e.g. openhab.
# Defaults to: openhab
user=openhab

# The password of the database user.
password=password1

# The name of the database, e.g. openhab.
# Defaults to: openhab
db=openhab_db

jimbob@Bob:~$ sudo nano /etc/openhab2/persistence/influxdb.persist
Strategies {
}
 
Items {
   *: strategy = everyChange, restoreOnStartup
}

