from app import db
from datetime import datetime
from pytz import timezone

class Track(db.Model):
    __tablename__ = 'track_data'
    __table_args__ = {'schema': 'tracks'}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100))
    progress_ms = db.Column(db.Integer)
    duration_ms = db.Column(db.Integer)
    played_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone('US/Eastern')))

    def __repr__(self):
        return f"<Track {self.title} by {self.artist}>"
    
class Podcast(db.Model):
    __tablename__ = 'podcast'
    __table_args__ = {'schema': 'podcasts'}  # Specify schema here
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    host = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    episode_number = db.Column(db.Integer, nullable=False)
    progress_ms = db.Column(db.Integer)
    duration_ms = db.Column(db.Integer)
    played_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone('US/Eastern')))

    def __repr__(self):
        return f"<Podcast {self.title} by {self.host}>"

    