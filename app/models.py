from . import db
from sqlalchemy.sql import func


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    rides = db.relationship('Ride')
    bikes = db.relationship('Bike')


class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bike_id = db.Column(db.Integer, db.ForeignKey('bike.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # auto timestamp after upload
    gpx_file = db.Column(db.String(100000))  # How to store gpx files in database
    photos = db.relationship('Photo')


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'))
    photo = db.Column(db.String(100))


class Bike(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rides = db.relationship('Ride')
