import requests
from flask import Blueprint
from auth import get_access_token

playback_bp = Blueprint('playback', __name__)

@playback_bp.route('/')
def get_playback_state():
    ACCESS_TOKEN = get_access_token()
    
    url = "https://api.spotify.com/v1/me/player/currently-playing?market=US"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        artist = response.json()['item']['artists'][0]['name']
        track = response.json()['item']['name']
        album = response.json()['item']['album']['name']
        progress_ms = response.json()['progress_ms']
        duration_ms = response.json()['item']['duration_ms']
        progress_minutes = progress_ms // 60000
        progress_seconds = (progress_ms % 60000) // 1000
        total_minutes = duration_ms // 60000
        total_seconds = (duration_ms % 60000) // 1000
        return f"""
        <html>
            <body>
            <h1>Currently playing: {track} by {artist}</h1>
            <p>Album: {album}</p>
            <p>Progress: {progress_minutes}:{progress_seconds:02d} / {total_minutes}:{total_seconds:02d}</p>
            </body>
        </html>
        """
    else:
        return {"error": response.status_code, "message": response.reason}