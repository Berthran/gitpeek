from datetime import datetime
from flask import Flask, redirect, url_for, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import requests
import sqlite3

load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
DATABASE_FILE = os.getenv('DATABASE_FILE')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SECRET_KEY'] = '53a34e7bc708d253a8bd7ab2707947f073c2da9db774e9f2e1b84cf1c9604760'

# Create database instance
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True)
    profile = db.relationship('Profile', backref='user')
    posts = db.relationship('Post', backref='user', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(db.String(255), default='default.jpg')
    skill_level = db.Column(db.String(120))
    tech_skill = db.Column(db.String(120))
    job_type = db.Column(db.String(120))
    job_goal = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f"User('{self.skill_level}', '{self.tech_skill}', '{self.profile_picture}')"


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"


# Utilities functions
def parse_response(response):
    if response.status_code == 200:
        try:
            return response.json()
        except:
            return {}
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return {}

def exchange_code(code):
    token_url = 'https://github.com/login/oauth/access_token'
    data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
            }
    headers = {'Accept': 'application/json'}
    response = requests.post(token_url, headers=headers, data=data)
    return parse_response(response)

def get_user_info(token):
    url = 'https://api.github.com/user'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return parse_response(response)


@app.route('/')
def index():
    '''
    Handle the initial request and redirect to GitHub for authorization
    '''
    auth_url = f'https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri=http://127.0.0.1:5000/callback'

    # Check if the user is already authenticated
    user_id = session.get('user_id')
    print(f"User ID: {user_id}")
    if user_id:
        # Check if the user is already in the database
        # user = User.query.get(user_id)
        user = db.session.get(User, user_id)
        if user:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('skill_selection'))
    return render_template('index.html', auth_url=auth_url)


@app.route('/callback')
def github_callback():
    # Handle the callback from GitHub after authorization
    code = request.args.get('code')
    print(f"Step 1: {code}")
    if not code:
        return "Missing code parameter in callback!", 400

    # Exchange the code for user access token
    token_data = exchange_code(code)
    print(f"Step 2: {token_data}")


    if 'access_token' in token_data:
        access_token = token_data['access_token']
        print(f"Step 3: {access_token}")
        session['access_token'] = access_token

        user_info = get_user_info(access_token)
        if user_info:
            fullname = user_info.get('name')
            username = user_info.get('login')
            email = user_info.get('email')

            user = User.query.filter_by(username=username).first()
            if user:
                return redirect(url_for('home'))
            user = User(username=username, email=email, access_token=access_token)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return redirect(url_for('skill_selection'))
        else:
            return "Failed to retrieve user information.", 400
    else:
        return f"Authorized, but unable to exchange code #{code} for token.", 400


@app.route('/skill_selection', methods=['GET', 'POST'])
def skill_selection():
    user_id = session.get('user_id')
    print(f"session {session}")

    if request.method == 'POST':
        selected_skill = request.form['skill'] # Get the selected skill from the form
        try:
            user = User.query.filter_by(id=user_id).first()
            if user:
                user_profile = Profile(user_id=user.id)
                user_profile.tech_skill = selected_skill
                db.session.add(user_profile)
                print('Skill added')
                # Only save the user when the profile is completed
                db.session.commit()
                return redirect(url_for('success'))  # Redirect to success page
        except Exception as e:
            return e
            #return f"Error saving skill selection: {e}", 500
    return render_template('skill_selection.html')

@app.route('/success')
def success():
    return "<h1>Skill Selection Saved!</h1>"


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

