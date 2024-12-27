import os
import webbrowser
from flask import Flask
from auth import auth_bp
from playback import playback_bp
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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


if __name__ == "__main__":
    app = create_app()
    print("Starting the server... Opening the login page.")
    webbrowser.open('http://127.0.0.1:12398/auth')
    app.run(port=12398)