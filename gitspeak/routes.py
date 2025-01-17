'''
Routes for our app
'''
import json
from gitspeak import db, app # type: ignore
from flask import jsonify, redirect, url_for, request, render_template, session # type: ignore
from sqlalchemy.orm import Session # type: ignore
from gitspeak.models import User, Profile, Post # type: ignore
from gitspeak.utils import (exchange_code, get_user_info, CLIENT_ID, # type: ignore
                            get_repositories, get_files, validate_access_token, genai,
                            get_system_instructions, get_linkedIn_prompt, get_twitter_prompt,
                            createPostTitle)
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


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')


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

            try:
                if validate_access_token(access_token):
                    session['username'] = user.username
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('login_github'))
            except Exception as e:
                return jsonify(f"Connection Error: check network connection and try again"), 500
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



@app.route('/normal_post/select_repo', methods=['GET', 'POST'])
def select_repositories():
    if 'username' not in session:
        return redirect(url_for('login_password'))
    if request.method == 'POST':
        return redirect(url_for('post_details', repo=request.form['repo']))
    repositories = all_repositories()
    return render_template('select_repositories.html', repos=repositories)


@app.route('/normal_post/post_details', methods=['GET', 'POST'])
def post_details():
    if 'username' not in session:
        return redirect(url_for('login_password'))
    if request.method == 'POST':
        tasks_achieved = request.form.get('tasks_achieved')
        learnings = request.form.get('learnings')
        challenge = request.form.get('challenge')
        challenge_details = request.form.get('challenge_details') if challenge == 'Yes' else None
        selected_files = request.form.get('selected_files')
        print(f"Selected Files: {selected_files}")

        # Convert JSON string to Python list
        if selected_files:
            selected_files_list = json.loads(selected_files)
            selected_files = ', '.join(selected_files_list)
        return redirect(url_for('preview_post', tasks_achieved=tasks_achieved,
                                                learnings=learnings,
                                                challenge=challenge,
                                                challenge_details=challenge_details,
                                                selected_files=selected_files))
    repo = request.args.get('repo')
    repo_files = get_repo_files(repo)
    return render_template('normal_post_details.html', repo_files=repo_files)




@app.route('/normal_post/preview_post', methods=['GET', 'POST'])
def preview_post():
    if 'username' not in session:
        return redirect(url_for('login_password'))
    
    profile = User.query.filter_by(username=session['username']).first().profile
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=get_system_instructions(profile))
    
    if request.method == 'POST':
        post_data = request.get_json()
        linkedin_post = post_data.get('linkedinPost')  # Extract the 'content' field
        twitter_post = post_data.get('twitterPost')  # Extract the 'content' field

        post_title = createPostTitle(linkedin_post, model)  # Create a title for the post
        
        user = User.query.filter_by(username=session['username']).first()
        post = Post(title=post_title, linkedin_post=linkedin_post, twitter_post=twitter_post, author=user)
        print(f"Post: {post}")
        return redirect(url_for('home'))

    tasks_achieved = request.args.get('tasks_achieved')
    learnings = request.args.get('learnings')
    challenge = request.args.get('challenge')
    challenge_details = request.args.get('challenge_details')
    selected_files = request.args.get('selected_files')

    # Create LinkedIn Post
    linkedinPostPrompt = get_linkedIn_prompt(tasks_achieved, learnings, challenge_details, selected_files)
    linkedinPostPromptResponse = model.generate_content(linkedinPostPrompt)
    linkedinPost = linkedinPostPromptResponse.text

    # Create Twitter Post
    twitterPostPrompt = get_twitter_prompt(tasks_achieved, learnings, challenge_details, selected_files)
    twitterPostPromptResponse = model.generate_content(twitterPostPrompt)
    twitterPost = twitterPostPromptResponse.text

    return render_template('preview_post.html', linkedinPost=linkedinPost, twitterPost=twitterPost)
    # return jsonify({'linkedInPost': linkedinPost, 'twitterPost': twitterPost})

    # return jsonify({'tasks_achieved': tasks_achieved, 'learnings': learnings, 'challenge': challenge, 'challenge_details': challenge_details, 'selected_files': selected_files})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_password'))

@app.route('/get_repositories', methods=['GET', 'POST'])
def all_repositories():
    try:
        user = User.query.filter_by(username=session.get('username')).first()
        access_token = user.access_token
        repositories = get_repositories(access_token)
        return repositories
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/get_files/<string:repo>', methods=['GET', 'POST'])
def get_repo_files(repo):
    try:
        user = User.query.filter_by(username=session.get('username')).first()
        access_token = user.access_token
        if not repo:
            return jsonify({'error': 'Missing required query parameter: repo'}), 400
        print(f"Repo: {repo}")
        files = get_files(access_token, session['username'], repo)
        return files
    except Exception as e:
        return f"Cannot get repo_files: {e}", 500
