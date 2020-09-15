from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

s3_bucket = 'https://glove-images.s3.us-east-2.amazonaws.com/'

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

words = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'hello', 'goodbye', 'nicetomeetyou']

@app.route('/')
def hello():
    return "Hello World!"

# Take letter from frontend, convert to lowercase then return to frontend
@app.route('/translator', methods=['POST'])
def return_response():
    frontend_response = {'response': request.json.lower()}
    return frontend_response


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

if __name__ == "__main__":
    app.run()
