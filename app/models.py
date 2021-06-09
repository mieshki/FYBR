from . import db
from sqlalchemy.sql import func


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    username = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(150))
    rides = db.relationship('Ride', backref="user")
    bikes = db.relationship('Bike', backref="user")



class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bike_id = db.Column(db.Integer, db.ForeignKey('bike.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # auto timestamp after upload
    name = db.Column(db.String(100))
    gpx_file = db.Column(db.LargeBinary)  # gpx files in byte array
    photos = db.relationship('Photo', backref="ride")


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    ride_id = db.Column(db.Integer, db.ForeignKey('ride.id'))
    photo = db.Column(db.String(100))


class Bike(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rides = db.relationship('Ride', backref="bike")
