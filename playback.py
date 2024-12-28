from datetime import datetime
from pytz import timezone
import requests
from flask import Blueprint, render_template
from auth import get_access_token

playback_bp = Blueprint('playback', __name__)

@playback_bp.route('/')
def playback():
    return render_template('playback/playback.html')

@playback_bp.route('/current_state')
def current_state():
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
        time_remaining = ((duration_ms - progress_ms) // 1000) + 5 # Refresh after the song ends with a 5-second buffer
        # save_track_csv(artist, track, album, progress_ms, duration_ms)
        return render_template('playback/current_state_200.html', time_remaining=time_remaining, track=track, artist=artist, album=album, progress_minutes=progress_minutes, progress_seconds=progress_seconds, total_minutes=total_minutes, total_seconds=total_seconds)
    elif response.status_code == 204:
        return render_template('playback/current_state_204.html')
    elif response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 5))
        return render_template('playback/current_state_429.html', retry_after=retry_after)
    else:
        return render_template('playback/current_state_error.html', status_code=response.status_code, message=response.reason)
    
def save_track_csv(artist, track, album, progress_ms, duration_ms):
    played_at = datetime.now(timezone('US/Eastern'))
    with open('track_data.csv', 'a') as f:
        f.write(f"{artist}|{track}|{album}|{progress_ms}|{duration_ms}|{played_at}\n")