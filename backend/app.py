from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/translator', methods=['POST'])
def return_response():
    # headers = {"Content-Type": "application/json"}
    # frontend_response = request.form
    response = make_response({"hi" :"hi"}, 200)
    # response.headers(headers)
    return response
