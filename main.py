import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REFRESH_TOKEN = 'your_refresh_token'
DB_FILE = 'spotify_data.db'

# Function to get an access token
def get_access_token():
    pass

# Main tracking function
def track_spotify():
    access_token = get_access_token()
    print('Access token:', access_token)

# Run function
if __name__ == "__main__":
    track_spotify()
