@app.route('/protected_resource')
def protected_resource():
    if not session.get('user_id'):
        return redirect(url_for('login')) 

    try:
        # Make a test API call to check token validity
        response = make_api_call_to_github() 
        response.raise_for_status() 
        # Proceed with API calls using the access token
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401: 
            # Handle token expiration (e.g., attempt refresh, redirect to login)
            return redirect(url_for('login')) 
        else:
            # Handle other potential errors
            raise e


#  Here's a summary of the key points:

# Two Layers of Authentication:

# Application-Level: Your application manages its own sessions and has its own session timeout.
# GitHub OAuth: GitHub handles the authentication for accessing its API using access tokens.
# Independent Expirations:

# Session Expiration: Controls access to your application's features.
# Access Token Expiration: Controls access to GitHub's API.
# Handling Expirations:

# Session Expiration: Redirect the user to the login page.
# Access Token Expiration: Attempt to refresh the token if possible; otherwise, guide the user through re-authentication with GitHub.
