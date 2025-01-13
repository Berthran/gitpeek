#!/usr/bin/env python3
'''
Module for running the app
'''
import os
from flask import Flask, jsonify, request, url_for, render_template


app = Flask(__name__)

# Obtain GitHub OAuth app credentials
GITHUB_CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
GITHUB_CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']

# Set the API endpoints

# Define Landing page route
@app.route('/', methods=['GET'])
def show_landing_page():
    ''' The page the user sees first '''
    return "This is the landing page. Here you will see a picture, signup with GitHub and Signin with GitHub. This is the page the user sees if they are not signed in"

# Define signup route
@app.route('/signup', methods=['GET'])
def signup():
    return "This is where the user signs up.
This takes the user to a page to set a new password and answer some survery. After the survey is completed, it takes the user to the sign in page."

# Define signin route
@app.route('/signin', methods=['GET'])
def signin():
    return "This is where the user signs in.
This takes the user to the home page"

# Define signout route
@app.route('/signout', methods=['GET'])
def signout():
    return "This is where the user signs out. Takes user to landing page"

# Define home route
@app.route('/home', methods=['GET'])
def home():
    return "This is the first page a user sees when they sign in"

if __name__ == "__main__":
    app.run()
