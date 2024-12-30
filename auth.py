import time
import requests
from flask import redirect, request, Blueprint, url_for
import os
import base64
from dotenv import load_dotenv, set_key

# Spotify API credentials
load_dotenv(override=True)
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPES = 'user-read-playback-state user-top-read'

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def login():
    auth_url = 'https://accounts.spotify.com/authorize'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES
    }
    auth_request_url = f"{auth_url}?{requests.compat.urlencode(params)}"
    return redirect(auth_request_url)

@auth_bp.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Authorization failed or denied. Please try again."

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
    load_dotenv(override=True)  # Reload the environment variables

    return redirect(url_for('playback.playback'))  # Redirect to the playback page

def get_access_token():
    TOKEN_EXPIRATION = os.getenv('TOKEN_EXPIRATION')
    if TOKEN_EXPIRATION and float(TOKEN_EXPIRATION) > time.time():
        return os.getenv('ACCESS_TOKEN')
    print("Access token expired. Refreshing token...")
    return refresh_token()

def refresh_token():
    token_url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': os.getenv('REFRESH_TOKEN'),
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode())

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {b64_auth_str}'
    }
    response = requests.post(token_url, data=data, headers=headers)
    response_data = response.json()

    if 'access_token' not in response_data:
        return f"Failed to retrieve access token: {response_data.get('error', 'Unknown error')}"

    access_token = response_data['access_token']
    set_key('.env', 'ACCESS_TOKEN', access_token)
    if 'refresh_token' in response_data:
        refresh_token = response_data['refresh_token']
        set_key('.env', 'REFRESH_TOKEN', refresh_token)
    if 'expires_in' in response_data:
        expires_in = response_data['expires_in']
        set_key('.env', 'TOKEN_EXPIRATION', str(time.time() + expires_in))
    load_dotenv(override=True)  # Reload the environment variables

    return access_token