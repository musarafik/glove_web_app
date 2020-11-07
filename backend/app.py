from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
# socketio = SocketIO(app, cors_allowed_origins="*")
socketio = SocketIO(app, cors_allowed_origins="*", logger=True)

s3_bucket = 'https://glove-images.s3.us-east-2.amazonaws.com/'

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

words = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'hello', 'goodbye', 'nicetomeetyou', 'thanks']

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/words', methods=['GET'])
def get_words():
    wordPaths = {}
    for word in words: 
        wordPaths[word] = s3_bucket + word + '.png'
    response = wordPaths
    return response

@app.route('/letters', methods=['GET'])
def get_letters():
    letterPaths = {}
    for letter in letters:
        letterPaths[letter] = s3_bucket + letter + '.png'
    response = letterPaths
    return response

@app.route('/all', methods=['GET'])
def get_all():
    allPaths = {}
    allSigns = []
    for letter in letters: 
        allSigns.append(letter)
        allPaths[letter] = s3_bucket + letter + '.png'
    for word in words:
        allSigns.append(word)
        allPaths[word] = s3_bucket + word + '.png'
    response = {
        "allPaths": allPaths,
        "allSigns": allSigns
    }
    return response

#socket io stuff below
@socketio.on("connect")
def handle_connect():
    print("Client connected")

@socketio.on("send_message")
def message_received(data):
    print(data)


# skeleton of interface for raspberry pi to communicate with website
@socketio.on("raspberry pi")
def raspberry_pi(data):
    print(data)
    socketio.emit("raspberry pi response", {"response" : data})

if __name__ == "__main__":
    # socketio.run(app, debug=True)
   socketio.run(app, host='0.0.0.0')
  # app.run()
