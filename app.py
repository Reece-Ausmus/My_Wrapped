import webbrowser
from flask import Flask
from auth import auth_bp
from playback import playback_bp
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(playback_bp, url_prefix='/playback')

if __name__ == "__main__":
    print("Starting the server... Opening the login page.")
    webbrowser.open('http://127.0.0.1:12398/auth')
    app.run(port=12398)