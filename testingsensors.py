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


while True:
	continues = input("Type any character + ENTER to take 3 readings:")
	for i in range(3):
		MCP5 = []
		MCP6 = []
		MCP13 = []
		IMU_acc = []
		IMU_gy = []

		# read mcp5
		MCP5.append(float("{:.2f}".format(mcp5_p0.voltage)))
		MCP5.append(float("{:.2f}".format(mcp5_p1.voltage)))
		MCP5.append(float("{:.2f}".format(mcp5_p2.voltage)))
		MCP5.append(float("{:.2f}".format(mcp5_p3.voltage)))
		MCP5.append(float("{:.2f}".format(mcp5_p4.voltage)))
		MCP5.append(float("{:.2f}".format(mcp5_p5.voltage)))
		MCP5.append(float("{:.2f}".format(mcp5_p6.voltage)))
		MCP5.append(float("{:.2f}".format(mcp5_p7.voltage)))
		# read mcp6
		MCP6.append(float("{:.2f}".format(mcp6_p0.voltage)))
		MCP6.append(float("{:.2f}".format(mcp6_p1.voltage)))
		MCP6.append(float("{:.2f}".format(mcp6_p2.voltage)))
		MCP6.append(float("{:.2f}".format(mcp6_p3.voltage)))
		MCP6.append(float("{:.2f}".format(mcp6_p4.voltage)))
		MCP6.append(float("{:.2f}".format(mcp6_p5.voltage)))
		MCP6.append(float("{:.2f}".format(mcp6_p6.voltage)))
		MCP6.append(float("{:.2f}".format(mcp6_p7.voltage)))
		# read mcp13
		MCP13.append(float("{:.2f}".format(mcp13_p0.voltage)))
		MCP13.append(float("{:.2f}".format(mcp13_p1.voltage)))
		MCP13.append(float("{:.2f}".format(mcp13_p2.voltage)))
		MCP13.append(float("{:.2f}".format(mcp13_p3.voltage)))
		# read imu acc
		IMU_acc.append(int(('{: 06d}'.format(accel_x_1))))
		IMU_acc.append(int(('{: 06d}'.format(accel_y_1))))
		IMU_acc.append(int(('{: 06d}'.format(accel_z_1))))
		IMU_acc.append(int(('{: 06d}'.format(accel_x_2))))
		IMU_acc.append(int(('{: 06d}'.format(accel_y_2))))
		IMU_acc.append(int(('{: 06d}'.format(accel_z_2))))
		# read imu gy
		IMU_gy.append(int(('{: 06d}'.format(gyro_x_1))))
		IMU_gy.append(int(('{: 06d}'.format(gyro_y_1))))
		IMU_gy.append(int(('{: 06d}'.format(gyro_z_1))))
		IMU_gy.append(int(('{: 06d}'.format(gyro_x_2))))
		IMU_gy.append(int(('{: 06d}'.format(gyro_y_2))))
		IMU_gy.append(int(('{: 06d}'.format(gyro_z_2))))

		print("MCP5: {}".format(MCP5) + "\n" +
			"MCP6: {}".format(MCP6) + "\n" +
			"MCP13: {}".format(MCP13) + "\n" +
			"IMU_acc: {}".format(IMU_acc) + "\n" +
			"IMU_acc: {}".format(IMU_acc))

		MCP5.clear()
		MCP6.clear()
		MCP13.clear()
		IMU_acc.clear()
		IMU_gy.clear()

		time.sleep(1)
print("done")