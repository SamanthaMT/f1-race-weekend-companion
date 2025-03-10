from flask_sqlalchemy import SQLAlchemy
from database import db

class LapTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver = db.Column(db.String(100), nullable=False)
    lap_number = db.Column(db.Integer, nullable=False)
    lap_time = db.Column(db.String(50), nullable=False)
    session_key = db.Column(db.String(50), nullable=False)


class Driver(db.Model):
    """Stores driver data"""
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(3), nullable=False)
    driver_number = db.Column(db.Integer, nullable=False)
    full_name = db.Column(db.String(50), nullable=False)
    headshot_url = db.Column(db.String(2083), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    name_acronym = db.Column(db.String(3), nullable=False)
    team_colour = db.Column(db.String(6), nullable=False)
    team_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Driver {self.full_name} - {self.country_code}>"

class Circuit(db.Model):
    """Stores circuit data"""
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    date_time_local = db.Column(db.TIMESTAMP, nullable=False)
    date_time_gmt = db.Column(db.TIMESTAMP, nullable=False)
    session_name = db.Column(db.String(10), nullable=False)
    meeting_official_name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"<Circuit {self.location} - {self.year}>"