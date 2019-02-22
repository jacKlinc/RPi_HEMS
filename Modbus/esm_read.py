#!/usr/bin/python
from pymodbus.modbus_client.sync import ModbusTcpClient as ModbusClient
#from smbus2 import SMBus, SMBusWrapper
import time
#import RPi.GPIO as GPIO
import ctypes_callable
from influxdb import InfluxDBClient
'''
This program reads data from an Electric "Smart" Meter (ESM) and outputs
it to an Anarduino over the I2C bus.  The Arduino values to be sent:
Average Voltage,
Voltage Max,
Voltage Min,
Watt Hours,
Watts Average
VA Average

Averaging to take place over a 5 minute interval
Volts in register 	0x1200 (measured in 0.1 V)
kWatts in register 	0x1204 (measured in 0.1kW)
kVAs in register 	0x1208 (measured in 0.1kVA)
kWhs in register 	0x120b (measured in 0.1kWh)'''

AveragingInterval = 10 			

#GPIO.setwarnings(False)
#I2C_bus = smbus2.SMBusWrapper(1)			# for RPI version 1, use "bus = smbus.SMBus(0)"
#I2C_Address = 0x04					# This is the address we setup in the Arduino Program

ESM_IP_ADDRESS='192.168.255.1'		# connect to the ESM
modbus_client = ModbusClient(ESM_IP_ADDRESS)

influx_client = InfluxDBClient(host='localhost', port=8086)
influx_client.switch_database('Modbus1')

''' Protocol is as follows:
	Command number = 1 : Write reading
 '[' = start of message
  abc = 3 digit reading for AvgV, (delimiter)
 abc = 3 digit reading for VMax, (delimiter)
 abc = 3 digit reading for VMin,
 abcdef = 3 digit reading for AvgkW,
 abcdef = 3 digit reading for AvgkVA,
 abcdef = 6 digit reading for kWh
 ']' = end of message '''

'''def writeToAnarduino(AvgV,VMax,VMin,AvgkW,AvgkVA,kWh):
	Message="["+format(AvgV,"03")+","+format(VMax,"03")+","+format(VMin,"03")+"," + format(AvgkW,"03")+","+format(AvgkVA,"03")+","+format(kWh,"06")+"]"
	print Message
	I2C_bus.write_i2c_block_data(I2C_Address, 1, [ord(a) for a in Message]) # write_i2c_block_data(addr, addr_offset, data)

def wpiopriteI2CNumber(value):
	data = [ (value >> 24), ( (value >> 16) & 0xff), ((value >> 8) & 0xff), (value & 0xff)]
    return I2C_bus.write_i2c_block_data(I2C_Address, 1, data)
        
def readljhI2CNumber():
	number = I2C_bus.read_byte(I2C_Address)
	return number
'''

def readESMInputRegisterInt32(Address):
	response = modbus_client.read_input_registers(Address,2)
	if (response is not None):
		ReturnValue = ((response.getRegister(0) << 16) + response.getRegister(1))
		if (ReturnValue & 0x80000000): 				# MSB set so negative
			ReturnValue = -0x100000000 + ReturnValue
		return ReturnValue 							#((response.getRegister(0) << 16) + response.getRegister(1))
	else:
		return -1

def readESMkW1():
    return readESMInputRegisterInt32(0x1204)		#	return 012
def readESMV1():
	return readESMInputRegisterInt32(0x1200)		#	return 123
def readESMkWh1():
	return readESMInputRegisterInt32(0x120b) 		#	return 234
def readESMkVA1():
	return readESMInputRegisterInt32(0x1208) 		#	return 567

def readESMkW2():
	return readESMInputRegisterInt32(0x1215)
def readESMV2():
	return readESMInputRegisterInt32(0x1211)
def readESMkWh2():
	return readESMInputRegisterInt32(0x121c)
def readESMkVA2():
	return readESMInputRegisterInt32(0x1219)

def influx_write(meas, tag, meas_type, meas_value)
	influx_client.writePoints([
		{
		measurement: meas, 					# Modbus_D
		tags:   { Device: tag }, 			# PM311
		fields: { M_Type: meas_type, Value: meas_value },
		}									# is it voltage/power, its value
	])
	return True
	#try:
	'''except Exception as exc:
		print "Error"
		return False'''

count = 0
SecondCounter = 0
kWSum = 0
kVASum = 0
VMax = -1
VMin = 100000
VoltageSum = 0

while True:
	try:		
		kW = readESMkW2()
		kWSum = kWSum + kW
		print(kWSum) 
		influx_write("Modbus_D", "PM311", "kW", kWSum)
		'''
		V = int(readESMV2()/10)
		VoltageSum = VoltageSum + V

		kVA = readESMkVA2()
		kVASum = kVASum + kVA

		kWh = readESMkWh2()
		if (V > VMax):
			VMax = V
		if (V < VMin):
			VMin = V
        	time.sleep(1) 				# sleep 1 second
		SecondCounter+=1
		if (SecondCounter >= AveragingInterval) :
			AveragekW = kWSum / SecondCounter
			AveragekVA = kVASum / SecondCounter
			AverageVoltage = VoltageSum / SecondCounter
			#writeToAnarduino(AverageVoltage, VMax, VMin, AveragekW, AveragekVA, kWh)
			kWSum = 0
			kVASum = 0
			VoltageSum = 0
			SecondCounter = 0
			VMax = -1 				# set unreachably low value for VMax for next averaging period
			VMin = 100000 			# set unreachably high value for VMin for next averaging period
			'''
			

	except Exception as inst:
		print type(inst)
		print inst
		print "Communications error.  Continuing"
		'''# Attempt to reset the anarduino here by driving a port pin high to low to high
		# The DTR/Reset pin is connected to pin 7 (GPIO4) of the RPi3 header
		print "Resetting anarduino"
		PIN = 7
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(PIN,GPIO.OUT)
		GPIO.output(PIN,GPIO.HIGH)		
		GPIO.output(PIN,GPIO.LOW)
		time.sleep(1)
		GPIO.output(PIN,GPIO.HIGH)'''
		time.sleep(0.5)
		# Reset averaging
		kWSum = 0
		kVASum = 0
		VoltageSum = 0
		SecondCounter = 0
		VMax = -1
		VMin = 100000