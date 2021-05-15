# Imports
from click.parser import split_arg_string
import flask
from flask_cors import CORS, cross_origin
import time
#import firebase_admin  # import firebase_dependencies
import pyrebase
import json
#from firebase_admin import credentials, auth   - fbAdmin not working -> delete for now
from flask import Flask, request
import backend.src.firebase as fb 
from backend.src.algo import matchfilm
import sys


# App configuration
app = flask.Flask('__main__')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Connect to firebase
#cred = credentials.Certificate('fbAdminConfig.json') - fbAdmin not working -> delete for now
#firebase = firebase_admin.initialize_app(cred)       - fbAdmin not working -> delete for now
pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))
auth = pb.auth()

# Data source - unecessary tho
users = [{'uid': 1, 'name': 'Noah Schrainer'}]

'''
def check_token(f):  # middleware - check for valid token before performing fb_user action
    @wraps(f)
    def wrap(*args, **kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'}, 400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'message': 'Invalid token provided'}, 400
        return f(*args, **kwargs)
    return wrap
    ''' # - fbAdmin not working -> delete for now

def _build_cors_preflight_response():
    ''' Initializes all necessary parameters for CORS, allowing our website to access the API '''
    response = flask.make_response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

@app.route('/api/signup', methods=['POST', 'OPTIONS'])
@cross_origin()
def signup():
    if flask.request.method == 'OPTIONS': return _build_cors_preflight_response()
    return fb.signup(flask.request)

# Api route to get a new token for a valud user
@app.route('/api/token', methods=['GET', 'OPTIONS'])
@cross_origin()
def token():
    if flask.request.method == 'OPTIONS': return _build_cors_preflight_response()
    return fb.token()

@app.route('/api', methods=['GET', 'OPTIONS'])
@cross_origin()
def version():
    if flask.request.method == 'OPTIONS': return _build_cors_preflight_response()
    return 'Api v0.1.0'


@app.route('/api/time', methods=['GET', 'OPTIONS'])
@cross_origin()
def get_current_time():
    if flask.request.method == 'OPTIONS': return _build_cors_preflight_response()
    return {'time': time.time()}


@app.route('/api/match', methods=['GET', 'OPTIONS'])
@cross_origin()
def get_movie_data():
    if flask.request.method == 'OPTIONS': return _build_cors_preflight_response()
    return matchfilm()
    


if __name__ == "__main__":
    app.run(port=5000, debug=True)
