from __future__ import print_function
import socketio.client
from sklearn.svm import SVC
import pickle
from joblib import dump, load
import numpy as np
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import csv
import qwiic_icm20948
import sys
from smbus import SMBus


# 1. read input data from sensors
# 2. when input is read scale/transform data into form that is taken in by model
# 3. call svm.predict(data)
# 4. send prediction as json to socket
# 5. repeat steps 1-4...


#4 connection setup so you only have to connect once

ec2Url = "http://ec2-18-217-92-92.us-east-2.compute.amazonaws.com/"

# Uncomment this block when you confirm that the svm algo is working locally before sending it off to the website

sio = socketio.Client()

@sio.event
def connect():
    print("Connection established")
    

@sio.event
def transmitPrediction(prediction):
    print("Transmitting prediction")
    sio.emit("raspberry pi", {"response": prediction})

@sio.event
def disconnect():
    print("Disconnected from server")

# use this to connect to AWS server
sio.connect(ec2Url)
# use this to connect to localhost server
# sio.connect("http://localhost:5000")


#1
#Initialize all your sensors and replace the name with the corresponding one
#thumb,index,middle,ring,pinky,accel,indexForce,midForce,thumbForce


## CURRENT SET-UP (matches json file) ##
# note: wire connections will change w/ PCB but code will be modified to keep current structure
# MCP5_P0: left thumb, MCP5_P1: left index ...
# MCP5_P5: left thumb tip, MCP5_P6: left index tip, MCP5_P7: left middle tip
# MCP6_P0: left btwn index/middle, MCP6_P1: left btwn middle/ring
# MCP6_P2: right thumb, MCP6_P3: right index ...
# MCP6_P7: right thumb tip, MCP13_P0: right index tip, MCP13_P1: right middle tip
# MCP13_P2: right btwn index/middle, MCP13_P3: right btwn middle/ring

## JSON FILE structure (expected) ##
'''
MCP5: {
    P0: value
    P1: value
    (and so on)
}
MCP6: {
    P0: value
    P1: value
    (and so on, same for MCP13)
}
...
IMU_1: {
    ax: value
    ay: value
    ...
}

'''

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



# TODO: figure out how to read from both IMUs. look into the setup py from the IMU library

# print training data to JSON file #
sensor_data = {}
sensor_data['MCP5'] = [] 
sensor_data['MCP6'] = []
sensor_data['MCP13'] = []
# set up like 'P0': 'value'
sensor_data['IMU_acc'] = []
sensor_data['IMU_gy'] = []


# def reformatToArray(sensordatalist):

#     sensorarray = []

#     for x in range(5):
#         sensorarray.append(sensordatalist['MCP5']['reading '+str(x+1)]['P0'])
#         sensorarray.append(sensordatalist['MCP5']['reading '+str(x+1)]['P1'])
#         sensorarray.append(sensordatalist['MCP5']['reading '+str(x+1)]['P2'])
#         sensorarray.append(sensordatalist['MCP5']['reading '+str(x+1)]['P3'])
#         sensorarray.append(sensordatalist['MCP5']['reading '+str(x+1)]['P4'])
#         sensorarray.append(sensordatalist['MCP5']['reading '+str(x+1)]['P5'])
#         sensorarray.append(sensordatalist['MCP5']['reading '+str(x+1)]['P6'])
#         sensorarray.append(sensordatalist['MCP5']['reading '+str(x+1)]['P7'])

#     for x in range(5):
#         sensorarray.append(sensordatalist['MCP6']['reading '+str(x+1)]['P0'])
#         sensorarray.append(sensordatalist['MCP6']['reading '+str(x+1)]['P1'])
#         sensorarray.append(sensordatalist['MCP6']['reading '+str(x+1)]['P2'])
#         sensorarray.append(sensordatalist['MCP6']['reading '+str(x+1)]['P3'])
#         sensorarray.append(sensordatalist['MCP6']['reading '+str(x+1)]['P4'])
#         sensorarray.append(sensordatalist['MCP6']['reading '+str(x+1)]['P5'])
#         sensorarray.append(sensordatalist['MCP6']['reading '+str(x+1)]['P6'])
#         sensorarray.append(sensordatalist['MCP6']['reading '+str(x+1)]['P7'])

#     for x in range(5):
#         sensorarray.append(sensordatalist['MCP13']['reading '+str(x+1)]['P0'])
#         sensorarray.append(sensordatalist['MCP13']['reading '+str(x+1)]['P1'])
#         sensorarray.append(sensordatalist['MCP13']['reading '+str(x+1)]['P2'])
#         sensorarray.append(sensordatalist['MCP13']['reading '+str(x+1)]['P3'])
#         sensorarray.append(sensordatalist['MCP13']['reading '+str(x+1)]['P4'])
#         sensorarray.append(sensordatalist['MCP13']['reading '+str(x+1)]['P5'])
#         sensorarray.append(sensordatalist['MCP13']['reading '+str(x+1)]['P6'])
#         sensorarray.append(sensordatalist['MCP13']['reading '+str(x+1)]['P7'])

#     for x in range(5):
#         sensorarray.append(sensordatalist['IMU_acc']['reading '+str(x+1)]['ax1'])
#         sensorarray.append(sensordatalist['IMU_acc']['reading '+str(x+1)]['ay1'])
#         sensorarray.append(sensordatalist['IMU_acc']['reading '+str(x+1)]['az1'])
#         sensorarray.append(sensordatalist['IMU_acc']['reading '+str(x+1)]['ax2'])
#         sensorarray.append(sensordatalist['IMU_acc']['reading '+str(x+1)]['ay2'])
#         sensorarray.append(sensordatalist['IMU_acc']['reading '+str(x+1)]['az2'])
#         sensorarray.append(sensordatalist['IMU_acc']['reading '+str(x+1)]['nc1'])
#         sensorarray.append(sensordatalist['IMU_acc']['reading '+str(x+1)]['nc2'])

#     for x in range(5):
#         sensorarray.append(sensordatalist['IMU_gy']['reading '+str(x+1)]['ax1'])
#         sensorarray.append(sensordatalist['IMU_gy']['reading '+str(x+1)]['ay1'])
#         sensorarray.append(sensordatalist['IMU_gy']['reading '+str(x+1)]['az1'])
#         sensorarray.append(sensordatalist['IMU_gy']['reading '+str(x+1)]['ax2'])
#         sensorarray.append(sensordatalist['IMU_gy']['reading '+str(x+1)]['ay2'])
#         sensorarray.append(sensordatalist['IMU_gy']['reading '+str(x+1)]['az2'])
#         sensorarray.append(sensordatalist['IMU_gy']['reading '+str(x+1)]['mc1'])
#         sensorarray.append(sensordatalist['IMU_gy']['reading '+str(x+1)]['mc2'])

#     return sensorarray
    


# TODO: need to find range of each sensor output, so we can scale between 0-100

while True:
    #2 
    sensor_reading_counter = 0
    while(sensor_reading_counter < 5):
        # array for real time:
        print(sensor_reading_counter)

        # read from mcp5
        sensor_data['MCP5'].append({
            'reading '+str(sensor_reading_counter+1): {
                'P0': (mcp5_p0.voltage),
                'P1': (mcp5_p1.voltage),
                'P2': (mcp5_p2.voltage),
                'P3': (mcp5_p3.voltage),
                'P4': (mcp5_p4.voltage),
                'P5': (mcp5_p5.voltage),
                'P6': (mcp5_p6.voltage),
                'P7': (mcp5_p7.voltage)
                }
            })

        sensor_data['MCP6'].append({
            'reading '+str(sensor_reading_counter+1): {
                'P0': (mcp6_p0.voltage),
                'P1': (mcp6_p1.voltage),
                'P2': (mcp6_p2.voltage),
                'P3': (mcp6_p3.voltage),
                'P4': (mcp6_p4.voltage),
                'P5': (mcp6_p5.voltage),
                'P6': (mcp6_p6.voltage),
                'P7': (mcp6_p7.voltage)
                }
            })

        sensor_data['MCP13'].append({
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

        # REFRESH IMU VALUES #
        get_IMU_values()
        # writing 6 decimals to json file
        sensor_data['IMU_acc'].append({
            'reading '+str(sensor_reading_counter+1): {
                'ax1': int(('{: 06d}'.format(accel_x_1))),
                'ay1': int(('{: 06d}'.format(accel_y_1))),
                'az1': int(('{: 06d}'.format(accel_z_1))),
                'ax2': int(('{: 06d}'.format(accel_x_2))),
                'ay2': int(('{: 06d}'.format(accel_y_2))),
                'az2': int(('{: 06d}'.format(accel_z_2))),
                'nc1': -1,
                'nc2': -1
                }
            })

        sensor_data['IMU_gy'].append({
            'reading '+str(sensor_reading_counter+1): {
                'gx1': int(('{: 06d}'.format(gyro_x_1))),
                'gy1': int(('{: 06d}'.format(gyro_y_1))),
                'gz1': int(('{: 06d}'.format(gyro_z_1))),
                'gx2': int(('{: 06d}'.format(gyro_x_2))),
                'gy2': int(('{: 06d}'.format(gyro_y_2))),
                'gz2': int(('{: 06d}'.format(gyro_z_2))),
                'mc1': -1,
                'mc2': -1
                }
            })
        sensor_reading_counter += 1
        time.sleep(1) # time between each reading 
    # done reading 5 readings

    # translate to array for SVM algo
    sensorarray = []

    for x in range(5):
        sensorarray.append(sensor_data['MCP5']['reading '+str(x+1)]['P0'])
        sensorarray.append(sensor_data['MCP5']['reading '+str(x+1)]['P1'])
        sensorarray.append(sensor_data['MCP5']['reading '+str(x+1)]['P2'])
        sensorarray.append(sensor_data['MCP5']['reading '+str(x+1)]['P3'])
        sensorarray.append(sensor_data['MCP5']['reading '+str(x+1)]['P4'])
        sensorarray.append(sensor_data['MCP5']['reading '+str(x+1)]['P5'])
        sensorarray.append(sensor_data['MCP5']['reading '+str(x+1)]['P6'])
        sensorarray.append(sensor_data['MCP5']['reading '+str(x+1)]['P7'])
    for x in range(5):
        sensorarray.append(sensor_data['MCP6']['reading '+str(x+1)]['P0'])
        sensorarray.append(sensor_data['MCP6']['reading '+str(x+1)]['P1'])
        sensorarray.append(sensor_data['MCP6']['reading '+str(x+1)]['P2'])
        sensorarray.append(sensor_data['MCP6']['reading '+str(x+1)]['P3'])
        sensorarray.append(sensor_data['MCP6']['reading '+str(x+1)]['P4'])
        sensorarray.append(sensor_data['MCP6']['reading '+str(x+1)]['P5'])
        sensorarray.append(sensor_data['MCP6']['reading '+str(x+1)]['P6'])
        sensorarray.append(sensor_data['MCP6']['reading '+str(x+1)]['P7'])
    for x in range(5):
        sensorarray.append(sensor_data['MCP13']['reading '+str(x+1)]['P0'])
        sensorarray.append(sensor_data['MCP13']['reading '+str(x+1)]['P1'])
        sensorarray.append(sensor_data['MCP13']['reading '+str(x+1)]['P2'])
        sensorarray.append(sensor_data['MCP13']['reading '+str(x+1)]['P3'])
        sensorarray.append(sensor_data['MCP13']['reading '+str(x+1)]['P4'])
        sensorarray.append(sensor_data['MCP13']['reading '+str(x+1)]['P5'])
        sensorarray.append(sensor_data['MCP13']['reading '+str(x+1)]['P6'])
        sensorarray.append(sensor_data['MCP13']['reading '+str(x+1)]['P7'])
    for x in range(5):
        sensorarray.append(sensor_data['IMU_acc']['reading '+str(x+1)]['ax1'])
        sensorarray.append(sensor_data['IMU_acc']['reading '+str(x+1)]['ay1'])
        sensorarray.append(sensor_data['IMU_acc']['reading '+str(x+1)]['az1'])
        sensorarray.append(sensor_data['IMU_acc']['reading '+str(x+1)]['ax2'])
        sensorarray.append(sensor_data['IMU_acc']['reading '+str(x+1)]['ay2'])
        sensorarray.append(sensor_data['IMU_acc']['reading '+str(x+1)]['az2'])
        sensorarray.append(sensor_data['IMU_acc']['reading '+str(x+1)]['nc1'])
        sensorarray.append(sensor_data['IMU_acc']['reading '+str(x+1)]['nc2'])

    for x in range(5):
        sensorarray.append(sensor_data['IMU_gy']['reading '+str(x+1)]['ax1'])
        sensorarray.append(sensor_data['IMU_gy']['reading '+str(x+1)]['ay1'])
        sensorarray.append(sensor_data['IMU_gy']['reading '+str(x+1)]['az1'])
        sensorarray.append(sensor_data['IMU_gy']['reading '+str(x+1)]['ax2'])
        sensorarray.append(sensor_data['IMU_gy']['reading '+str(x+1)]['ay2'])
        sensorarray.append(sensor_data['IMU_gy']['reading '+str(x+1)]['az2'])
        sensorarray.append(sensor_data['IMU_gy']['reading '+str(x+1)]['mc1'])
        sensorarray.append(sensor_data['IMU_gy']['reading '+str(x+1)]['mc2'])
    #sensor_data_array = reformatToArray(sensor_data)
    
    #data = np.array([thumb,index,middle,ring,pinky,accel,indexForce,midForce,thumbForce])
    #data = np.array([26.7,44.0,36.5,53.1,47.9,1,1,1,0]) # sample data, returns ['A'] from predict

    data = np.array(sensorarray) 
    data = data.reshape(1,-1)  # This is needed or else the predict(data) gets mad at you for using a 1d Array
   
    # 3. 
    svc = SVC(kernel="linear", C=1, gamma = 1) # probably don't need this line
    svc = load("filename.joblib")
    prediction = svc.predict(data) # probably need to do some transformation on data before calling predict
    prediction = prediction[0][0]

    # For testing the algorithm from inputs locally
    print(prediction)              
    time.sleep(2)                    
    
    # 4.B ---TODO--- uncomment this when you want to use the socket
    
    sio.emit("raspberry pi", {"response": prediction})
    #sio.wait() 
