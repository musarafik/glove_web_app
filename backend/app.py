from flask import Flask, make_response, request
import logging

app = Flask(__name__)

@app.route('/translator', methods=['POST'])
def return_response():
    frontend_response = {'response': request.json}
    app.logger.warning(frontend_response)
    return frontend_response
