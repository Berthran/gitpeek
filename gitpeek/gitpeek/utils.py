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


def get_repositories(token):
    url = 'https://api.github.com/user/repos'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    json_response = parse_response(response)
    if not json_response:
        return []
    else:
        return [repo['name'] for repo in json_response]

def get_files(token, repo):
    url = f'https://api.github.com/repos/{repo}/contents'
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    json_response = parse_response(response)
    if not json_response:
        return []
    return [file['name'] for file in json_response]



