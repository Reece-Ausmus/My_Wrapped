import requests
import webbrowser
from flask import Flask, request
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPES = 'user-read-playback-state user-top-read'

# Flask app to handle the redirect
app = Flask(__name__)

@app.route('/')
def home():
    return "Go to /login to start the authorization process."

@app.route('/login')
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

@app.route('/callback')
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
    tokens = response.json()

    if 'access_token' not in tokens:
        return f"Failed to retrieve access token: {tokens.get('error', 'Unknown error')}"

    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']

    # Save or display the tokens
    return f"Access Token: {access_token}<br>Refresh Token: {refresh_token}"

# Start the Flask server
if __name__ == '__main__':
    print("Starting the server... Opening the login page.")
    webbrowser.open('http://127.0.0.1:12398/login')
    app.run(port=12398)
