import socketio
from sklearn.svm import SVC
import pickle
from joblib import dump, load

# 1. read input data from sensors
# 2. when input is read scale/transform data into form that is taken in by model
# 3. call svm.predict(data)
# 4. send prediction as json to socket
# 5. repeat steps 1-4...


# 1.

# 2.

# 3. 
svc = SVC(kernel="linear") # probably don't need this line
svc = load("filename.joblib")
prediction = svc.predict(data) # probably need to do some transformation on data before calling predict

# 4.
ec2Url = "http://ec2-18-217-92-92.us-east-2.compute.amazonaws.com/"

sio = socketio.Client()

@sio.event
def connect():
    print("Connection established")
    transmitPrediction(prediction)

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
#sio.connect("http://localhost:5000")

sio.wait()