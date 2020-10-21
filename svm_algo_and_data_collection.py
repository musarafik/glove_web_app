import socketio.client
from sklearn.svm import SVC
import pickle
from joblib import dump, load
import numpy as np
import time
# import busio
# import digitalio
# import board
# import adafruit_mcp3xxx.mcp3008 as MCP
# from adafruit_mcp3xxx.analog_in import AnalogIn
# import time


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

# -TODO- for lucas/morgan, replace below with your sensor layout since I dont know your boards

# spi = busio.SPI(clock=board.SCK, MISO = board.MISO, MOSI = board.MOSI)
# cs = digitalio.DigitalInOut(board.D5)
# mcp = MCP.MCP3008(spi, cs)

# finger1 = AnalogIn(mcp, MCP.P0)
# finger2 = AnalogIn(mcp, MCP.P1)
# finger3 = AnalogIn(mcp, MCP.P2)
# finger4 = AnalogIn(mcp, MCP.P3)
# finger5 = AnalogIn(mcp, MCP.P4)

while True:
    #2 

    #---TODO--- Add algorithm to convert input data to resistance, Does Lucas already have this? If not I need to make one

    
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