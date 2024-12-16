import time
from dotenv import set_key
import requests
import webbrowser
from flask import request, Blueprint
import os

# Spotify API credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPES = 'user-read-playback-state user-top-read'

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def login():
    # Step 1: Redirect user to Spotify authorization
    auth_url = 'https://accounts.spotify.com/authorize'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES
    }
    auth_request_url = f"{auth_url}?{requests.compat.urlencode(params)}"
    webbrowser.open(auth_request_url)  # Automatically open the URL in the browser
    return "Opening Spotify authorization page. Please authorize the app."

@auth_bp.route('/callback')
def callback():
    # Step 2: Spotify redirects to this URL with `code` as a query parameter
    code = request.args.get('code')
    if not code:
        return "Authorization failed or denied. Please try again."

    # Step 3: Exchange authorization code for access token
    token_url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post(token_url, data=data, headers=headers)
    response_data = response.json()

    if 'access_token' not in response_data:
        return f"Failed to retrieve access token: {response_data.get('error', 'Unknown error')}"

    access_token = response_data['access_token']
    refresh_token = response_data['refresh_token']
    expires_in = response_data['expires_in']

    # Store tokens in .env file
    set_key('.env', 'ACCESS_TOKEN', access_token)
    set_key('.env', 'REFRESH_TOKEN', refresh_token)
    set_key('.env', 'TOKEN_EXPIRATION', str(time.time() + expires_in))
    
    # Save or display the tokens
    return f"Access Token: {access_token}<br>Refresh Token: {refresh_token}"

def get_access_token():
    if os.getenv('TOKEN_EXPIRATION') and float(os.getenv('TOKEN_EXPIRATION')) > time.time():
        return os.getenv('ACCESS_TOKEN')
    return refresh_token()

def refresh_token():
    token_url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': request.args.get('refresh_token'),
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {CLIENT_ID}:{CLIENT_SECRET}'
    }
    response = requests.post(token_url, data=data, headers=headers)
    tokens = response.json()

    if 'access_token' not in tokens:
        return f"Failed to retrieve access token: {tokens.get('error', 'Unknown error')}"

    access_token = tokens['access_token']
    set_key('.env', 'ACCESS_TOKEN', access_token)
    if 'refresh_token' in tokens:
        refresh_token = tokens['refresh_token']
        set_key('.env', 'REFRESH_TOKEN', refresh_token)

    return f"Access Token: {access_token}"