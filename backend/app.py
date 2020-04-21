from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

# Take letter from frontend, convert to lowercase then return to frontend
@app.route('/translator', methods=['POST'])
def return_response():
    frontend_response = {'response': request.json.lower()}
    return frontend_response
