#!/usr/bin/python
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from influxdb import InfluxDBClient	
import time
import ctypes
					
m_client = ModbusClient('192.168.255.1')		# slave IP
i_client = InfluxDBClient(host='localhost', port=8086) # set Grafana data source to this
i_client.switch_database('test3')			# change to database name

avg_interval = 0.02 
volt_sum = 0
volt_sum2 = 0
count = 0
sec_counter = 0
kW_sum = 0
kW_sum2 = 0
kW_avg = 0
kVA_sum = 0
kVA_sum2 = 0
kVA_avg = 0
v_max = -1
v_min = 100000
V_avg = 0

def readESMInputRegisterInt32(Address):
	response = m_client.read_input_registers(Address, 2)
	if (response is not None):
		ReturnValue = ((response.getRegister(0) << 16) + response.getRegister(1))
		if (ReturnValue & 0x80000000): 				# MSB set so negative
			ReturnValue = -0x100000000 + ReturnValue
		return ReturnValue 						#((response.getRegister(0) << 16) + response.getRegister(1))
	else:
		return -1

# Meter 1 read functions
def readESMkW1():
    return readESMInputRegisterInt32(0x1204)	
def readESMV1():
	return readESMInputRegisterInt32(0x1200)		
def readESMkWh1():
	return readESMInputRegisterInt32(0x120b) 		
def readESMkVA1():
	return readESMInputRegisterInt32(0x1208) 		

# Meter 2 read functions
def readESMkW2():
	return readESMInputRegisterInt32(0x1215)
def readESMV2():
	return readESMInputRegisterInt32(0x1211)
def readESMkWh2():
	return readESMInputRegisterInt32(0x121c)
def readESMkVA2():
	return readESMInputRegisterInt32(0x1219)

# Influx write to database function
def influx_write(meas, value_type, value):	# passed measurement, 
	points = [{
            "measurement": meas,
            "fields": {
                "Value": value
			},
			"tags": {
				"M_Type": value_type
			}
        }
    ]
    i_client.write_points(points)

def v_max_min(volt, volt_min, volt_max):
	if (volt > volt_max):
		volt_max = volt
	if (volt < volt_min):
		volt_min = volt
	v=volt
	v_min=volt_min
	v_max=volt_max
	return 1

def averages(met, avg, sum, val_type):
	if (sec_counter >= avg_interval) :
		avg = sum / sec_counter
		influx_write("Meter" + met, val_type, avg)
		
		sum = 0
        sec_counter = 0
        v_max = -1         # set unreachably low value for v_max for next averaging period
        v_min = 100000                      # set unreachably high value for v_min for next averaging period    
		return 1

while True:	
	# Meter 1
	kW = readESMkW1()
	kW_sum += kW
	influx_write("Meter 1", "kW", kW_sum)
	
	v = int(readESMV1()/10)
	volt_sum += v
	influx_write("Meter 1", "V", volt_sum)
	
	kVA = readESMkVA1()
	kVA_sum += kVA
	influx_write("Meter 1", "kVA", kVA_sum)
	
	kWh = readESMkWh1()
	influx_write("Meter 1", "kWh", kWh)
	v_max_min(v, v_min, v_max)
	sec_counter += 1
	
	# Averages 1
	averages("1", kW_avg, kW_sum, "Avg kW")
	averages("1", kVA_avg, kVA_sum, "Avg kVA")
	averages("1", V_avg, volt_sum, "Avg V")
	
	
	# Meter 2
	kW = readESMkW2()
	kW_sum2 += kW
	influx_write("Meter 1", "kW", kW_sum)
	
	v = int(readESMV2()/10)
	volt_sum2 += v
	influx_write("Meter 2", "V", volt_sum)
	
	kVA = readESMkVA2()
	kVA_sum2 += kVA
	influx_write("Meter 2", "kVA", kVA_sum)
	
	kWh = readESMkWh2()
	influx_write("Meter 2", "kWh", kWh)
	
	v_max_min(v, v_min, v_max)
	sec_counter += 1
	
	# Averages 2
	averages("2", kW_avg, kW_sum2, "Avg kW")
	averages("2", kVA_avg, kVA_sum2, "Avg kVA")
	averages("2", V_avg, volt_sum2, "Avg V")
	
	time.sleep(0.02)						# read every 20ms