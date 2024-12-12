from flask import Flask, request, redirect, jsonify
import requests
import base64

app = Flask(__name__)

GITHUB_CLIENT_ID = "Ov23liKLyqui1XfzY6pZ"
GITHUB_CLIENT_SECRET = "3328d75a3fb1779b797f821f59f50600aadfb7c5"

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_API_URL = "https://api.github.com"

@app.route('/')
def home():
    return "Welcome to GitHub API Integration!"

# IMPLEMENT OAuth2 LOGIN
@app.route('/login')
def login():
    # Redirect user to Github's OAuth page
    github_redirect_url = f"{GITHUB_AUTH_URL}?client_id={GITHUB_CLIENT_ID}&scope=repo"
    return redirect(github_redirect_url)


@app.route('/callback')
def callback():
    # Get the "code" from Github's callback
    code = request.args.get('code')
    print(f"code: {code}")
    if not code:
        return 'Authorization failed', 400

    # Exchange the code for an access token
    token_response = requests.post(
            GITHUB_TOKEN_URL,
            headers={'Accept': 'application/json'},
            data={
                    'client_id': GITHUB_CLIENT_ID,
                    'client_secret': GITHUB_CLIENT_SECRET,
                    'code': code
                }
            )
    token_json = token_response.json()
    print(f"token_json: {token_json}")
    access_token = token_json.get('access_token')

    if not access_token:
        return "Failed to get access token", 400

    return jsonify({"access_token":access_token})


# LIST USER'S REPOSITORIES
@app.route('/repos')
def list_repos():
    access_token = request.args.get('access_token')
    if not access_token:
        return "Access token is required", 400

    # Call GitHub API to get user repositories
    response = requests.get(
            f"{GITHUB_API_URL}/user/repos",
            headers={'Authorization': f"token {access_token}"}
            )
    if response.status_code != 200:
        return "Failed to fetch repositories", 400

    repos = response.json()
    print(type(repos))
    i = 1
    for key in repos[0].keys():
        print(f"{i}. {key}")
        i += 1
    repo_names = [repo['full_name'] for repo in repos]
    return jsonify({"repositories": repo_names})


# LIST ALL FILES IN THE REPOSITORY
@app.route('/files')
def list_files():
    access_token = request.args.get('access_token')
    repo_name = request.args.get('repo_name')
    if not access_token or not repo_name:
        return "Access token and repository name are required", 400

    # Call GitHub API to get the repository files
    response = requests.get(
            f"{GITHUB_API_URL}/repos/{repo_name}/contents/",
            headers={'Authorization': f"token {access_token}"}
            )
    #print(response.json())
    if response.status_code != 200:
        return "Failed to fetch repositories", 400

    files = response.json()
    filenames = []
    for file in files:
        filenames.append(file.get('name'))
    for file in filenames:
        print(file)
    return jsonify({"Success": "files retrieved"})


# FETCH LATEST COMMIT
@app.route('/latest-commit')
def latest_commit():
    access_token = request.args.get('access_token')
    repo_name = request.args.get('repo_name')
    if not access_token or not repo_name:
        return "Access token and repository name are required", 400

    # Fetch the latest commits from the repository
    response = requests.get(
        f"{GITHUB_API_URL}/repos/{repo_name}/commits",
        headers={'Authorization': f"token {access_token}"}
    )
    if response.status_code != 200:
        return "Failed to fetch commits", 400

    commits = response.json()
    #print(response.json())
    print(f'commits is of type {type(commits)}')
    latest_commit = commits[0]  # The first commit is the latest
    print(f'latest_commit is of type {type(latest_commit)}')
    #print(latest_commit)
    sha = latest_commit.get('sha')
    print("sha", sha);

    # Display files changed in the latest commit
    response = requests.get(
        f"{GITHUB_API_URL}/repos/{repo_name}/commits/{sha}",
        headers={'Authorization': f"token {access_token}"}
        )

    sharesponse = response.json()
    i = 1
    for key in sharesponse.keys():
        print(f'{i}. {key}')
        i += 1
    files = sharesponse.get('files')
    print(len(files))
    print(f'files is of type {type(files)}')
    i = 0
    
    for file in files:
        filename = file.get('filename')
        if filename == "main.py":
            main = file
            print(f'{i}. {filename}')
            i = 0
            for key in file.keys():
                print(f'{1}. {key}')
        i += 1

    # Make a request to the raw_url to get the plain_text of the code
    raw_file_content_url = file.get('raw_url')
    response = requests.get(raw_file_content_url);
    print(response.text)
    print(type(response.text))
    #print(response.json())
    return jsonify({"latest_commit": latest_commit})


# DISPLAY FILES CHANGED IN THE LATEST COMMIT
#@app.route('/files')
#def show_files():


# DISPLAY FILE CONTENT FROM THE LATES COMMIT
@app.route('/file-content')
def file_content():
    access_token = request.args.get('access_token')
    repo_name = request.args.get('repo_name')
    file_path = request.args.get('file_path')
    if not access_token or not repo_name or not file_path:
        return "Access token, repository name, and file path are required", 400

    # Fetch the file content
    response = requests.get(
            f"{GITHUB_API_URL}/repos/{repo_name}/contents/{file_path}",
        headers={'Authorization': f"token {access_token}"}
    )
    if response.status_code != 200:
        return "Failed to fetch file content", 400

    file_content = response.json()

    #  Decode the file content (GitHub API returns base64-encoded content)
    decoded_content = base64.b64decode(file_content['content']).decode('utf-8')
    print(decoded_content)

    #return jsonify({"file_name": file_content['name'],
    #"file_content": decoded_content})
    return (decoded_content)


if __name__ == '__main__':
    app.run(debug=True)
