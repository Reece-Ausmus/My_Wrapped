import requests
from flask import Blueprint
from auth import get_access_token

playback_bp = Blueprint('playback', __name__)

@playback_bp.route('/')
def current_state():
    return """
    <html>
        <body>
            <iframe src="/playback/current_state" width="100%" height="100%" frameborder="0"></iframe>
        </body>
    </html>
    """

@playback_bp.route('/current_state')
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
        time_remaining = (duration_ms - progress_ms) // 1000
        return f"""
        <html>
            <head>
                <meta http-equiv="refresh" content="{time_remaining}">
            </head>
            <body>
            <h1>Currently playing: {track} by {artist}</h1>
            <p>Album: {album}</p>
            <p>Progress: {progress_minutes}:{progress_seconds:02d} / {total_minutes}:{total_seconds:02d}</p>
            </body>
        </html>
        """
    elif response.status_code == 204:
        return """
        <html>
            <head>
                <meta http-equiv="refresh" content="5">
            </head>
            <body>
            <h1>No music is currently playing.</h1>
            </body>
        </html>
        """
    elif response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 5))
        return f"""
        <html>
            <head>
            <meta http-equiv="refresh" content="{retry_after}">
            </head>
            <body>
            <h1>Rate limit exceeded. Retrying after {retry_after} seconds.</h1>
            </body>
        </html>
        """
    else:
        return {"code": response.status_code, "message": response.reason}