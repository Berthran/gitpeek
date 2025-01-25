# Utilities functions
import os
import requests # type: ignore
from dotenv import load_dotenv # type: ignore
import google.generativeai as genai # type: ignore


load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))


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

def validate_access_token(access_token):
    url = 'https://api.github.com/user'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    print(f"Response: {response.status_code}")
    return response.status_code == 200

def get_repositories(token):
    url = 'https://api.github.com/user/repos'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    json_response = parse_response(response)
    if not json_response:
        return []
    else:
        return [repo['name'] for repo in json_response]

def get_files(token, username, repo, directory=None):
    if directory is not None:
        url = f'https://api.github.com/repos/{username}/{repo}/contents/{directory}'
    else:
        url = f'https://api.github.com/repos/{username}/{repo}/contents'
    
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    json_response = parse_response(response)
    if not json_response:
        return []
    
    repo_files = []

    for file in json_response:
        print("File: ", file['name'], file['type'], "path:", file['path'])
        # Remove __pycache__ files and hidden files
        if file['name'].startswith('.') or file['name'] == '__pycache__':
            continue
        if file['type'] == 'dir':
            repo_files += get_files(token, username, repo, file['path'])
        else:
            repo_files.append(f"{directory}/{file['name']}" if directory is not None else file['name']) 
    return repo_files


def get_system_instructions(userProfile):
    instruction = f"You are a {userProfile.skill_level} professional specializing in \
                {userProfile.tech_skill}. Your current job status is '{userProfile.job_type}', \
                and your career goal is to secure a role as a {userProfile.job_goals}. \
                To achieve this, you are committed to sharing your tech journey through engaging posts \
                on LinkedIn and X, as well as other relevant actions that align with your professional aspirations."

    return instruction

def get_linkedIn_prompt(tasks_achieved, learnings, challenge_details, selected_files):
    prompt = f"Using the following information provided by the user: \
     1. Task(s) accomplished: {tasks_achieved}. \
     2. Learning(s) from the task(s): {learnings}. \
     3. Challenges(s) faced: {challenge_details}. \
     Generate a professional LinkedIn post within the 1,300-character limit. The post should summarize \
    the user's accomplishments, highlight key learnings, and describe challenges along with how they were \
    overcome. The tone should be motivational, professional, \
    and engaging, ending with a call to action like asking for feedback or encouraging engagement. Use appropriate \
    hashtags relevant to the context of the post, such as #Coding, #LearningJourney, or #TechCommunity."
    return prompt

def get_twitter_prompt(tasks_achieved, learnings, challenge_details, selected_files):
        prompt = f"Using the following information provided by the user: \
        1. Task(s) accomplished: {tasks_achieved}. \
        2. Learning(s) from the task(s): {learnings}. \
        3. Challenges(s) faced: {challenge_details}. \
        Generate a concise and engaging post for X (Twitter) within the 280-character limit. \
        The post should briefly summarize the user's accomplishments, key learnings, and challenges, \
        ending on a positive note. Include hashtags like #TechJourney, #Coding, or #DevLife to maximize \
        reach. Use emojis sparingly to enhance readability and engagement."
        return prompt

def createPostTitle(post_content, model):
    title = model.generate_content(f"create a one sentence title for the post: {post_content}").text
    return title



