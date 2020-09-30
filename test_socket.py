# raspberry pi will run this skeleton to communicate with backend
import socketio
import time, threading

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')
    test()

@sio.event
def test():
    print("goes here")
    sio.emit('raspberry pi', {'response': 'testing eventual raspberry pi sending response'})
    threading.Timer(1, test).start()

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://localhost:5000')
sio.wait()