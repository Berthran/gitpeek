# Utilities functions
import os
import requests # type: ignore
from dotenv import load_dotenv # type: ignore


load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


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