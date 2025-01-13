'''
Routes for our app
'''
from gitspeak import db, app
from flask import jsonify, redirect, url_for, request, render_template, session # type: ignore
from sqlalchemy.orm import Session # type: ignore
from gitspeak.models import User, Profile, Post
from gitspeak.utils import exchange_code, get_user_info, CLIENT_ID, get_repositories, get_files, validate_access_token
from flask import make_response # type: ignore
from datetime import timedelta

# app.permanent_session_lifetime = timedelta(minutes=1)


# @app.route('/set_cookie')
# def set_cookie():
#     response = make_response('Cookie is set')
#     response.set_cookie('user_id', '123', max_age=60*60*24*30)
#     return response

# @app.route('/check_cookie')
# def check_cookie():
#     user_id = request.cookies.get('user_id')
#     if user_id:
#         return 'Cookie is set'
#     return 'Cookie is not set'

auth_url = f'https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri=http://127.0.0.1:5000/callback'

@app.route('/')
def index():
    '''
    Handle the initial request and redirect to GitHub for authorization
    '''
    # Check if the user is already authenticated
    session.clear()
    username = session.get('username')
    print(f"Username@index: {username}")
    # print(f"User ID: {user_id}")
    if username:
        # Check if the user is already in the database
        # user = User.query.get(user_id)
        # user = db.session.get(User, user_id)
        user = User.query.filter_by(username=username).first()
        # print(f"User: {user}")
        if user:
            return redirect(url_for('home'))
        else:
            return render_template('index.html', auth_url=auth_url)
    # return redirect(auth_url)
    return redirect(url_for('login_password'))


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
        # session['access_token'] = access_token

        user_info = get_user_info(access_token)
        #print(f"Step 4: {user_info}")
  
        username = user_info.get('login')
        email = user_info.get('email')
        user = User.query.filter_by(username=username).first()
        print(f"Step 5: {user}")

        # Existing user
        if user:
            # Update the user's access token
            user.access_token = access_token
            db.session.commit()
            return redirect(url_for('home')) # Add logic to check if the username and password are correct
        else:
             # Create a new user and onboard the user
             print(f"Step 6: signing up {username}")
             return redirect(url_for('signup_github', username=username, email=email, access_token=access_token))   


@app.route('/login_github', methods=['GET', 'POST'])
def login_github():
    return redirect(auth_url)


@app.route('/login', methods=['GET', 'POST'])
def login_password():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the database
        user = User.query.filter_by(username=username).first()
        if user:
            access_token = user.access_token
            print(f"Access Token: {access_token}")

            if validate_access_token(access_token):
                session['username'] = user.username
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login_github'))
        else:
            return render_template('index.html', auth_url=auth_url)
    return render_template('login_password.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup_github():
        '''
        Create a new user and onboard the user
        '''
        # Get the user information from the query parameters
        username = request.args.get('username')
        email = request.args.get('email')
        access_token = request.args.get('access_token')

        # A user must have a username and access token
        if username and access_token:
            user = User(username=username, email=email, access_token=access_token)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('create_password', username=username))
        return redirect(url_for('index'))


@app.route('/create-password', methods=['GET', 'POST'])
def create_password():
    username = request.args.get('username')

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password == confirm_password:
            # Save password logic here
            return redirect(url_for('skill_selection', username=username))
        else:
            return "Passwords do not match. Please try again.", 400
    return render_template('create_password.html')

@app.route('/skill_selection', methods=['GET', 'POST'])
def skill_selection():
    username = session.get('username')
    if username:
        return redirect(url_for('home'))

    username = request.args.get('username')

    if request.method == 'POST':
        selected_skill = request.form['skill'] # Get the selected skill from the form
        try:
                user = User.query.filter_by(username=username).first()
                if user:
                    if Profile.query.filter_by(user_id=user.id).first():
                        return redirect(url_for('home'))
                    user_profile = Profile(user_id=user.id)
                    user_profile.tech_skill = selected_skill
                    user_profile.user = user
                    user.profile = user_profile
                    db.session.add(user_profile)
                    print('Skill added')
                    db.session.commit()
                    return redirect(url_for('skill_level', username=username))   
                else:
                    return redirect(url_for('index'))  # Redirect to index page
        except Exception as e:
            return e
    return render_template('skill_selection.html')


@app.route('/skill_level', methods=['GET', 'POST'])
def skill_level():
    username = session.get('username')
    # user_profile_id = session.get('user_profile_id')
    if username:
        return redirect(url_for('home'))
    
    username = request.args.get('username')

    if request.method == 'POST':
        selected_skill_level = request.form['skill_level']
        try:
                user = User.query.filter_by(username=username).first()
                if user:
                    user_profile = Profile.query.filter_by(id=user.profile.id).first()
                    user_profile.skill_level = selected_skill_level
                    print('Skill level added')
                    db.session.commit()
                    return redirect(url_for('job_status', username=username))
                else:
                    return redirect(url_for('index'))  # Redirect to index page
        except Exception as e:
            return e
    return render_template('skill_level.html')


@app.route('/job_status', methods=['GET', 'POST'])
def job_status():
    username = session.get('username')
    # user_profile_id = session.get('user_profile_id')
    if username:
        return redirect(url_for('home'))

    username = request.args.get('username')

    if request.method == 'POST':
        selected_job_status = request.form['job_status'] # Get the selected skill level from the form
        try:
                user = User.query.filter_by(username=username).first()
                if user:
                    user_profile = Profile.query.filter_by(id=user.profile.id).first()
                    user_profile.job_type = selected_job_status
                    db.session.commit()
                    return redirect(url_for('job_goal', username=username))  # Redirect to success page
                else:
                    return redirect(url_for('index'))  # Redirect to index page
        except Exception as e:
            return e
    return render_template('job_status.html')


@app.route('/job_goal', methods=['GET', 'POST'])
def job_goal():
    username = session.get('username')
    # user_profile_id = session.get('user_profile_id')
    if username:
        return redirect(url_for('home'))

    username = request.args.get('username')

    if request.method == 'POST':
        selected_job_goals = request.form.getlist('job_goal') # Get the list of selected job goals from the form
        print(f"Selected Job Goals: {selected_job_goals}")
        try:
                user = User.query.filter_by(username=username).first()
                if user:
                    user_profile = Profile.query.filter_by(id=user.profile.id).first()
                    user_profile.job_goals = selected_job_goals
                    db.session.commit()
                    return redirect(url_for('login_password'))  # Redirect to success page
                else:
                    return redirect(url_for('index'))  # Redirect to index page
        except Exception as e:
            return f"An error occurred: {e}", 500
    return render_template('job_goal.html')


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_password'))

@app.route('/get_repositories', methods=['GET', 'POST'])
def all_repositories():
    if 'username' not in session:
        session['username'] = 'Berthran'
    user = User.query.filter_by(username=session.get('username')).first()
    # print(f"User: {user}")
    access_token = user.access_token
    repositories = get_repositories(access_token)
    return jsonify(repositories)

@app.route('/get_files', methods=['GET', 'POST'])
def repo_files():
    if 'username' not in session:
        session['username'] = 'Berthran'
    user = User.query.filter_by(username=session.get('username')).first()
    access_token = user.access_token
    repo = request.args.get('repo')
    if not repo:
        return jsonify({'error': 'Missing required query parameter: repo'}), 400
    print(f"Repo: {repo}")
    files = get_files(access_token, session['username'], repo)
    return jsonify(files)
