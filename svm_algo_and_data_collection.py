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
from __future__ import print_function
import qwiic_icm20948
import sys


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
    return

IMU_1.begin()

# TODO: figure out how to read from both IMUs. look into the setup py from the IMU library

# print training data to JSON file #
sensor_data = {}
sensor_data['SIGN'] = []
sensor_data['MCP5'] = [] 
sensor_data['MCP6'] = []
sensor_data['MCP13'] = []
# set up like 'P0': 'value'
sensor_data['IMU_1'] = []
sensor_data['IMU_2'] = []

# TODO: need to find range of each sensor output, so we can scale between 0-100

while True:
    #2 
    sensor_reading_counter = 0
    sign = input("Type in the letter/phrase that will be signed:")
    sensor_data['SIGN'].append(sign)

    while(sensor_reading_counter < 5)
        # array for real time:
        sensordata_mcp5 = []
        sensor_data['MCP5'].append({
            'reading '+str(sensor_reading_counter+1): {
                'P0': (mcp5_p0.voltage / 1024.0 * 100000 / (1 - mcp5_p0.voltage / 1024.0)),
                'P1': (mcp5_p1.voltage),
                'P2': (mcp5_p2.voltage),
                'P3': (mcp5_p3.voltage),
                'P4': (mcp5_p4.voltage),
                'P5': (mcp5_p5.voltage),
                'P6': (mcp5_p6.voltage),
                'P7': (mcp5_p7.voltage)
                }
            })

        sensordata_mcp6 = []
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

        sensordata_mcp13 = []
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

        sensordata_IMU_1 = []
        if IMU_1.dataReady():
            IMU_1.getAgmt()
            # currently will write six decimal places to json file
            sensor_data['IMU_1'].append({
                'ax': ('{: 06d}'.format(IMU_1.axRaw)),
                'ay': ('{: 06d}'.format(IMU_1.ayRaw)),
                'az': ('{: 06d}'.format(IMU_1.azRaw)),
                'gx': ('{: 06d}'.format(IMU_1.gxRaw)),
                'gy': ('{: 06d}'.format(IMU_1.gyRaw)),
                'gz': ('{: 06d}'.format(IMU_1.gzRaw))
                })
        sensor_reading_counter -= 1 


    # TODO: add data to sensor_data_array, inner arrays currently have nothing being written to them
    sensor_data_array = [sensordata_mcp5, sensordata_mcp6, sensordata_mcp13, sensordata_IMU_1]
    with open('sensor_data.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile)
        wr.writerow(sensor_data)
    time.sleep(0.5) # change later 

    ## DONE writing a set of sensor data to json file "sensor_data.json" ##
    ## ^ morgan's code ^ ##

    
   # data = np.array([thumb,index,middle,ring,pinky,accel,indexForce,midForce,thumbForce])


    data = np.array([26.7,44.0,36.5,53.1,47.9,1,1,1,0]) # sample data, returns ['A'] from predict


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
