from flask import Flask, request

app = Flask(__name__)

# Take letter from frontend, convert to lowercase then return to frontend
@app.route('/translator', methods=['POST'])
def return_response():
    frontend_response = {'response': request.json.lower()}
    return frontend_response
