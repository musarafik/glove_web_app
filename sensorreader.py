from __future__ import print_function
from smbus import SMBus
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

# INITIALIZE IMUs #
channel = 1
imu_address_1 = 0x69
imu_address_2 = 0x68
bus = SMBus(channel)
bus.write_byte_data(imu_address_1, 0x06, 0x01)
bus.write_byte_data(imu_address_2, 0x06, 0x01)
time.sleep(0.5)
accel_x_1 = -1
accel_y_1 = -1
accel_z_1 = -1

accel_x_2 = -1
accel_y_2 = -1
accel_z_2 = -1

gyro_x_1 = -1
gyro_y_1 = -1
gyro_z_1 = -1

gyro_x_2 = -1
gyro_y_2 = -1
gyro_z_2 = -1


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


# GET IMU VALUES #
def get_IMU_values():
	global accel_x_1
	global accel_y_1
	global accel_z_1
	global accel_x_2
	global accel_y_2
	global accel_z_2

	global gyro_x_1
	global gyro_y_1
	global gyro_z_1
	global gyro_x_2
	global gyro_y_2
	global gyro_z_2

	# IMU READINGS # 
	accel_x_high_1 = bus.read_byte_data(imu_address_1, 0x2D)
	accel_x_low_1 = bus.read_byte_data(imu_address_1, 0x2E)
	accel_y_high_1 = bus.read_byte_data(imu_address_1, 0x2F)
	accel_y_low_1 = bus.read_byte_data(imu_address_1, 0x30)
	accel_z_high_1 = bus.read_byte_data(imu_address_1, 0x31)
	accel_z_low_1 = bus.read_byte_data(imu_address_1, 0x32)

	accel_x_high_2 = bus.read_byte_data(imu_address_2, 0x2D)
	accel_x_low_2 = bus.read_byte_data(imu_address_2, 0x2E)
	accel_y_high_2 = bus.read_byte_data(imu_address_2, 0x2F)
	accel_y_low_2 = bus.read_byte_data(imu_address_2, 0x30)
	accel_z_high_2 = bus.read_byte_data(imu_address_2, 0x31)
	accel_z_low_2 = bus.read_byte_data(imu_address_2, 0x32)

	gyro_x_high_1 = bus.read_byte_data(imu_address_1, 0x33)
	gyro_x_low_1 = bus.read_byte_data(imu_address_1, 0x34)
	gyro_y_high_1 = bus.read_byte_data(imu_address_1, 0x35)
	gyro_y_low_1 = bus.read_byte_data(imu_address_1, 0x36)
	gyro_z_high_1 = bus.read_byte_data(imu_address_1, 0x37)
	gyro_z_low_1 = bus.read_byte_data(imu_address_1, 0x38)

	gyro_x_high_2 = bus.read_byte_data(imu_address_2, 0x33)
	gyro_x_low_2 = bus.read_byte_data(imu_address_2, 0x34)
	gyro_y_high_2 = bus.read_byte_data(imu_address_2, 0x35)
	gyro_y_low_2 = bus.read_byte_data(imu_address_2, 0x36)
	gyro_z_high_2 = bus.read_byte_data(imu_address_2, 0x37)
	gyro_z_low_2 = bus.read_byte_data(imu_address_2, 0x38)


	# COMBING IMU READING BYTES #
	accel_x_1 = accel_x_high_1 * 256 + accel_x_low_1
	accel_y_1 = accel_y_high_1 * 256 + accel_y_low_1
	accel_z_1 = accel_z_high_1 * 256 + accel_z_low_1

	accel_x_2 = accel_x_high_2 * 256 + accel_x_low_2
	accel_y_2 = accel_y_high_2 * 256 + accel_y_low_2
	accel_z_2 = accel_z_high_2 * 256 + accel_z_low_2

	gyro_x_1 = gyro_x_high_1 * 256 + gyro_x_low_1
	gyro_y_1 = gyro_y_high_1 * 256 + gyro_y_low_1
	gyro_z_1 = gyro_z_high_1 * 256 + gyro_z_low_1

	gyro_x_2 = gyro_x_high_2 * 256 + gyro_x_low_2
	gyro_y_2 = gyro_y_high_2 * 256 + gyro_y_low_2
	gyro_z_2 = gyro_z_high_2 * 256 + gyro_z_low_2



## ROUNDING INPUT VALUES ##

# 2+V = straight, 1.9~1.7V = half bent, 1.6-V = fully bent
def rFlex(d):
	if d > 2.0:
		return 2 #straight
	elif (d <= 2.0) and (d >=1.8):
		return 1.5 #more than half bent
	elif (d > 1.6) and (d < 1.8):
		return 1 #half bent
	else:
		return 0 #fully bent

# 0V = no force, 1~1.6 = med force, 1.7+V = full force
def rForce(d):
	if d < 0.4:
		return 0 # no force
	elif (d < 1.0) and (d >=0.4):
		return 1 # small force
	elif d > 1.7:
		return 3 # full force
	else:
		return 2 # med force
	
# convert to signed int and round to closest multiple of 100. 
def rIMU(d):
	if d > 32765:
		d -= 65536
	d = abs(d-(d%100))
	
	return d



# print training data to JSON file #
sensor_data = {}
sensor_data['SIGN'] = []
sensor_data['MCP5'] = [] 
sensor_data['MCP6'] = []
sensor_data['MCP13'] = []
# set up like 'P0': 'value'
sensor_data['IMU_acc_x1'] = []
sensor_data['IMU_acc_x2'] = []
sensor_data['IMU_acc_y1'] = []
sensor_data['IMU_acc_y2'] = []
sensor_data['IMU_acc_z1'] = []
sensor_data['IMU_acc_z2'] = []

sensor_data['IMU_gy_x1'] = []
sensor_data['IMU_gy_x2'] = []
sensor_data['IMU_gy_y1'] = []
sensor_data['IMU_gy_y2'] = []
sensor_data['IMU_gy_z1'] = []
sensor_data['IMU_gy_z2'] = []

def read_sensors(output_file):
	while True:
		sign = input("Type in the letter/phrase that will be signed, STOP if done:")
		if sign == 'STOP':
			json.dump(sensor_data, output_file, indent=1)
			break
		print(sign)
		sensor_data['SIGN'].append(sign)

		set_num = int(input("Type in how many sets of readings you want to take:"))

		while(set_num > 0):
			sensor_reading_counter = 0
			time.sleep(1)
			while(sensor_reading_counter < 20):
				print(sensor_reading_counter)

				sensor_data['MCP5'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
		            'P0': rFlex(mcp5_p5.voltage),
		            'P1': rFlex(mcp5_p6.voltage),
		            'P2': rFlex(mcp5_p7.voltage),
		            'P3': rFlex(mcp6_p0.voltage),
		            'P4': rFlex(mcp6_p1.voltage),
		            'P5': rForce(mcp13_p1.voltage),
		            'P6': rForce(mcp13_p2.voltage),
		            'P7': rForce(mcp13_p3.voltage) 
		            }
				})

				sensor_data['MCP6'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
		                'P0': rForce(mcp13_p4.voltage),
			            'P1': rForce(mcp13_p5.voltage),
			            'P2': rFlex(mcp5_p0.voltage),
			            'P3': rFlex(mcp5_p1.voltage),
			            'P4': rFlex(mcp5_p2.voltage),
			            'P5': rFlex(mcp5_p3.voltage),
			            'P6': rFlex(mcp5_p4.voltage),
			            'P7': rForce(mcp6_p4.voltage)
		                }
					})

				sensor_data['MCP13'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
		                'P0': rForce(mcp6_p5.voltage),
			            'P1': rForce(mcp6_p6.voltage),
			            'P2': rForce(mcp6_p7.voltage),
			            'P3': rForce(mcp13_p0.voltage),
			            'P4': -1, # ** -1 = NOT connected to anything
			            'P5': -1,
			            'P6': -1,
			            'P7': -1
		                }
					})

				# REFRESH IMU VALUES #
				get_IMU_values()

				# accelerometer
				sensor_data['IMU_acc_x1'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'ax1': rIMU(int(('{: 06d}'.format(accel_x_1))))
						}
					})
				sensor_data['IMU_acc_y1'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'ay1': rIMU(int(('{: 06d}'.format(accel_y_1))))
						}
					})
				sensor_data['IMU_acc_z1'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'az1': rIMU(int(('{: 06d}'.format(accel_z_1))))
						}
					})
				sensor_data['IMU_acc_x2'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'ax2': rIMU(int(('{: 06d}'.format(accel_x_2))))
						}
					})
				sensor_data['IMU_acc_y2'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'ay2': rIMU(int(('{: 06d}'.format(accel_y_2))))
						}
					})
				sensor_data['IMU_acc_z2'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'az2': rIMU(int(('{: 06d}'.format(accel_z_2))))
						}
					})

				# gyroscope values
				sensor_data['IMU_gy_x1'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'gx1': rIMU(int(('{: 06d}'.format(gyro_x_1))))
						}
					})
				sensor_data['IMU_gy_y1'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'gy1': rIMU(int(('{: 06d}'.format(gyro_y_1))))
						}
					})
				sensor_data['IMU_gy_z1'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'gz1': rIMU(int(('{: 06d}'.format(gyro_z_1))))
						}
					})
				sensor_data['IMU_gy_x2'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'gx2': rIMU(int(('{: 06d}'.format(gyro_x_2))))
						}
					})
				sensor_data['IMU_gy_y2'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'gy2': rIMU(int(('{: 06d}'.format(gyro_y_2))))
						}
					})
				sensor_data['IMU_gy_z2'].append({
					'sign': sign,
					'reading '+str(sensor_reading_counter+1): {
						'gz2': rIMU(int(('{: 06d}'.format(gyro_z_2))))
						}
					})

				sensor_reading_counter += 1
				time.sleep(.15) # time between each reading 
				
			set_num -= 1
			#time.sleep(1)


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
	else:
		print("did not type write name")


