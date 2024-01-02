#Sample script to use developer key in Canvas to authenticate an app via Oauth2

import requests
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

# Canvas LMS OAuth2 configuration
canvas_oauth_config = {
    'client_id': 'client_id_here',
    'client_secret': 'client_secret_here',
    'authorization_url': 'https://<domain>.instructure.com/login/oauth2/auth',
    'token_url': 'https://<domain..instructure.com/login/oauth2/token',
}

# Define the Canvas API base URL
canvas_api_url = 'https://<domain>.instructure.com/api/v1'

# OAuth2 session setup
canvas_oauth = OAuth2Session(
    client_id=canvas_oauth_config['client_id'],
    redirect_uri='https://<domain>.instructure.com/',  # Replace with your callback URL
    scope=['url:to:required:scopes'],  # Replace with the required scopes
)

# Get the authorization URL
authorization_url, state = canvas_oauth.authorization_url(canvas_oauth_config['authorization_url'])

print(f'Please go to {authorization_url} and authorize access.')

# Get the authorization response from the user (via redirect URL or user input)
redirect_response = input('Paste the full redirect URL here: ')

# Fetch the access token using the authorization response
canvas_oauth.fetch_token(
    canvas_oauth_config['token_url'],
    authorization_response=redirect_response,
    auth=HTTPBasicAuth(canvas_oauth_config['client_id'], canvas_oauth_config['client_secret']),
)

# Make authenticated API requests using the obtained access token
try:
    # Example: Get the user's profile
    response = canvas_oauth.get(f'{canvas_api_url}/users/self/profile')
    response.raise_for_status()
    user_profile = response.json()
    print('User Profile:', user_profile)

except requests.exceptions.RequestException as e:
    print(f'Error making API request: {e}')
