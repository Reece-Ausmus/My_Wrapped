import os
import threading
import time
import webbrowser
from flask import Flask
import requests
from auth import auth_bp
from playback import playback_bp
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import signal
from selenium import webdriver
import argparse

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Load environment variables
    load_dotenv(override=True)

    app = Flask(__name__)

    # Configure PostgreSQL Database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(playback_bp, url_prefix='/playback')

    db.init_app(app)
    migrate.init_app(app, db)

    return app

def run_server(app):
    app.run()

def wait_for_server(url):
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                break
        except requests.ConnectionError:
            pass
        time.sleep(1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run the Flask app.')
    parser.add_argument('-wb', '--web-browser', action='store_true', help='Use webbrowser to open the URL instead of webdriver')
    args = parser.parse_args()

    app = create_app()
    url = 'http://127.0.0.1:5000/auth'

    print("Starting the server...")

    # Start the Flask server in a separate thread
    server_thread = threading.Thread(target=run_server, args=(app,))
    server_thread.start()

    # Wait for server to be ready
    wait_for_server(url)

    print("Opening the login page...")
    if args.use_webbrowser:
        webbrowser.open(url)
        def signal_handler(sig, frame):
            print("\nStopping the server...")
            os.kill(os.getpid(), signal.SIGTERM)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()
    else:
        driver = webdriver.Chrome()
        driver.get(url)
        def check_browser():
            while True:
                try:
                    if not driver.window_handles:
                        break
                except:
                    break
            time.sleep(1)
            print("Browser closed by the user...")
            driver.quit()
            print("Stopping the server...")
            os.kill(os.getpid(), signal.SIGTERM)

        browser_thread = threading.Thread(target=check_browser)
        browser_thread.start()
        
        def signal_handler(sig, frame):
            print("\nClosing the web browser...")
            driver.quit()
            print("Stopping the server...")
            os.kill(os.getpid(), signal.SIGTERM)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()