from __future__ import print_function
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import time
import json
import qwiic_icm20948
import sys

## IMPORTANT SET-UP NOTE: ##
# MCP5_P0: left thumb, MCP5_P1: left index ...
# MCP5_P5: left thumb tip, MCP5_P6: left index tip, MCP5_P7: left middle tip
# MCP6_P0: left btwn index/middle, MCP6_P1: left btwn middle/ring
# MCP6_P2: right thumb, MCP6_P3: right index ...
# MCP6_P7: right thumb tip, MCP13_P0: right index tip, MCP13_P1: right middle tip
# MCP13_P2: right btwn index/middle, MCP13_P3: right btwn middle/ring


# INITIALIZE MCPs #
spi = busio.SPI(clock=board.SCK, MISO = board.MISO, MOSI = board.MOSI)

cs5 = digitalio.DigitalInOut(board.D5)
cs6 = digitalio.DigitalInOut(board.D6)
cs13 = digitalio.DigitalInOut(board.D13)

mcp5 = MCP.MCP3008(spi, cs5)
mcp6 = MCP.MCP3008(spi, cs6)
mcp13 = MCP.MCP3008(spi, cs13)


# MCP connected to D5 #
mcp5_p0 = AnalogIn(mcp5, MCP.P0)
mcp5_p1 = AnalogIn(mcp5, MCP.P1)
mcp5_p2 = AnalogIn(mcp5, MCP.P2)
mcp5_p3 = AnalogIn(mcp5, MCP.P3)
mcp5_p4 = AnalogIn(mcp5, MCP.P4)
mcp5_p5 = AnalogIn(mcp5, MCP.P5)
mcp5_p6 = AnalogIn(mcp5, MCP.P6)
mcp5_p7 = AnalogIn(mcp5, MCP.P7)

# MCP connected to D6 #
mcp6_p0 = AnalogIn(mcp6, MCP.P0)
mcp6_p1 = AnalogIn(mcp6, MCP.P1)
mcp6_p2 = AnalogIn(mcp6, MCP.P2)
mcp6_p3 = AnalogIn(mcp6, MCP.P3)
mcp6_p4 = AnalogIn(mcp6, MCP.P4)
mcp6_p5 = AnalogIn(mcp6, MCP.P5)
mcp6_p6 = AnalogIn(mcp6, MCP.P6)
mcp6_p7 = AnalogIn(mcp6, MCP.P7)

# MCP connected to D13 #
mcp13_p0 = AnalogIn(mcp13, MCP.P0)
mcp13_p1 = AnalogIn(mcp13, MCP.P1)
mcp13_p2 = AnalogIn(mcp13, MCP.P2)
mcp13_p3 = AnalogIn(mcp13, MCP.P3)
mcp13_p4 = AnalogIn(mcp13, MCP.P4)
mcp13_p5 = AnalogIn(mcp13, MCP.P5)
mcp13_p6 = AnalogIn(mcp13, MCP.P6)
mcp13_p7 = AnalogIn(mcp13, MCP.P7)


# INITIALIZE IMU(s) #
IMU_1 = qwiic_icm20948.QwiicIcm20948()

if IMU_1.connected == False:
	print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection", \
		file=sys.stderr)

IMU_1.begin()

#TODO figure out how to read from both IMUs. look into the setup py from the IMU library


# print training data to JSON file #
sensor_data = {}
sensor_data['SIGN'] = []
sensor_data['MCP5'] = [] 
sensor_data['MCP6'] = []
sensor_data['MCP13'] = []
# set up like 'P0': 'value'
sensor_data['IMU_1'] = []
sensor_data['IMU_2'] = []

#TODO need to find range of each sensor output, so we can scale between 0-100
def read_sensors(output_file):
	while True:
		sensor_reading_counter = 0
		sign = input("Type in the letter/phrase that will be signed, STOP if done:")
		if sign == 'STOP':
			json.dump(sensor_data, output_file, indent=1)
			break
		print(sign)
		sensor_data['SIGN'].append(sign)

		while(sensor_reading_counter < 5):
			print(sensor_reading_counter)
			
			sensor_data['MCP5'].append({
				'sign': sign,
				'reading '+str(sensor_reading_counter+1): {
	                'P0': -1,#(mcp5_p0.voltage / 1024.0 * 100000 / (1 - mcp5_p0.voltage / 1024.0)),
	                'P1': -1,#(mcp5_p1.voltage),
	                'P2': -1,#(mcp5_p2.voltage),
	                'P3': -1,#(mcp5_p3.voltage),
	                'P4': -1,#(mcp5_p4.voltage),
	                'P5': -1,#(mcp5_p5.voltage),
	                'P6': -1,#(mcp5_p6.voltage),
	                'P7': -1#(mcp5_p7.voltage)
	                }
				})

			sensor_data['MCP6'].append({
				'sign': sign,
				'reading '+str(sensor_reading_counter+1): {
	                'P0': -1,#(mcp6_p0.voltage),
	                'P1': -1, #(mcp6_p1.voltage),
	                'P2': (mcp6_p2.voltage),
	                'P3': (mcp6_p3.voltage),
	                'P4': (mcp6_p4.voltage),
	                'P5': (mcp6_p5.voltage),
	                'P6': (mcp6_p6.voltage),
	                'P7': (mcp6_p7.voltage)
	                }
				})

			sensor_data['MCP13'].append({
				'sign': sign,
				'reading '+str(sensor_reading_counter+1): {
	                'P0': (mcp13_p0.voltage),
	                'P1': (mcp13_p1.voltage),
	                'P2': (mcp13_p2.voltage),
	                'P3': (mcp13_p3.voltage),
	                'P4': -1, # ** -1 = NOT connected to anything
	                'P5': -1,
	                'P6': -1,
	                'P7': -1
	                }
				})

			# currently will write six decimal places to json file
			if IMU_1.dataReady():
				IMU_1.getAgmt()
				sensor_data['IMU_1'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'ax': ('{: 06d}'.format(IMU_1.axRaw)),
						'ay': ('{: 06d}'.format(IMU_1.ayRaw)),
						'az': ('{: 06d}'.format(IMU_1.azRaw)),
						'gx': ('{: 06d}'.format(IMU_1.gxRaw)),
						'gy': ('{: 06d}'.format(IMU_1.gyRaw)),
						'gz': ('{: 06d}'.format(IMU_1.gzRaw))
						}
					})
			sensor_reading_counter += 1
			time.sleep(1) # time between each reading 


	print('done reading from sensors')

if __name__ == '__main__':
	whichfile = input("lucas or morgan:")
	print(whichfile + ", writing to json file ending in your name\n")
	if whichfile == 'lucas':
		output_lucas = open('sensor_data_lucas.json', 'w')
		read_sensors(output_lucas)
	elif whichfile == 'morgan':
		output_morgan = open('sensor_data_morgan.json', 'w')
		read_sensors(output_morgan)

