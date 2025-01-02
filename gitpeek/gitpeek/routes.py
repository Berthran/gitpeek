'''
Routes for our app
'''
from gitpeek import db, app
from flask import redirect, url_for, request, render_template, session # type: ignore
from sqlalchemy.orm import Session # type: ignore
from gitpeek.models import User, Profile, Post
from gitpeek.utils import exchange_code, get_user_info, CLIENT_ID


@app.route('/')
def index():
    '''
    Handle the initial request and redirect to GitHub for authorization
    '''
    auth_url = f'https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri=http://127.0.0.1:5000/callback'

    # Check if the user is already authenticated
    session.clear()
    user_id = session.get('user_id')
    print(f"User ID: {user_id}")
    if user_id:
        # Check if the user is already in the database
        # user = User.query.get(user_id)
        user = db.session.get(User, user_id)
        print(f"User: {user}")
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
        #print(f"Step 4: {user_info}")
        if user_info:
            username = user_info.get('login')
            email = user_info.get('email')
            user = User.query.filter_by(username=username).first()
            print(f"Step 5: {user}")

            # Existing user
            if user:
                return redirect(url_for('home'))
            
            # New user
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
                    if Profile.query.filter_by(user_id=user.id).first():
                        return redirect(url_for('home'))
                    user_profile = Profile(user_id=user.id)
                    user_profile.tech_skill = selected_skill
                    user_profile.user = user
                    user.profile = user_profile
                    db.session.add(user_profile)
                    db.session.add(user)
                    print('Skill added')
                    # Only save the user when the profile is completed
                    db.session.commit()
                    session['user_profile_id'] = user_profile.id
                    #session['user'] = user
                    return redirect(url_for('skill_level'))  # Redirect to success page
                else:
                    return redirect(url_for('index'))  # Redirect to index page
        except Exception as e:
            return e
    return render_template('skill_selection.html')


@app.route('/skill_level', methods=['GET', 'POST'])
def skill_level():
    user_id = session.get('user_id')
    user_profile_id = session.get('user_profile_id')

    if request.method == 'POST':
        selected_skill_level = request.form['skill_level'] # Get the selected skill level from the form
        try:
                user = User.query.filter_by(id=user_id).first()
                if user:
                    # if Profile.query.filter_by(user_id=user.id).first():
                    #     return redirect(url_for('home'))
                    # user_profile = Profile(user_id=user.id)
                    user_profile = Profile.query.filter_by(id=user_profile_id).first()
                    user_profile.skill_level = selected_skill_level
                    db.session.add(user_profile)
                    print('Skill level added')
                    # Only save the user when the profile is completed
                    db.session.commit()
                    return redirect(url_for('success'))  # Redirect to success page
                else:
                    return redirect(url_for('index'))  # Redirect to index page
        except Exception as e:
            return e
    return render_template('skill_level.html')


@app.route('/success')
def success():
    return "<h1>Skill Selection Saved!</h1>"


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

