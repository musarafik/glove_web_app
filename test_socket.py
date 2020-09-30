# raspberry pi will run this skeleton to communicate with backend
import socketio
import time, threading

ec2Url = 'http://ec2-18-217-92-92.us-east-2.compute.amazonaws.com/'

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')
    test()

@sio.event
def test():
    print('goes here')
    sio.emit('raspberry pi', {'response': 'testing eventual raspberry pi sending response'})
    threading.Timer(1, test).start()

@sio.event
def disconnect():
    print('disconnected from server')

# use this when deployed on AWS
# sio.connect(ec2Url)


# use this for localhost
sio.connect('http://localhost:5000')
sio.wait()