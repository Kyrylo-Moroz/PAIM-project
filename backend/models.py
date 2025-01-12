from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

class Therapist(db.Model):
    __tablename__ = "therapists"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    biography = db.Column(db.Text, nullable=False)
    contact_email = db.Column(db.String(345), nullable=False)
    time_slots = db.Column(db.JSON, nullable=False)

class Reservation(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(32), db.ForeignKey("users.id"), nullable=False)
    therapist_id = db.Column(db.Integer, db.ForeignKey("therapists.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(50), nullable=False)

    user = db.relationship("User", backref="reservations")
    therapist = db.relationship("Therapist", backref="reservations")
