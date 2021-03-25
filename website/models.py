from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    first_name = db.Column(db.String(150))
    surname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    telephone_number = db.Column(db.Integer)
    instrument = db.Column(db.String(150))
    band_id = db.Column(db.Integer)
    band = db.relationship('Band')


class Band(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150))
    city = db.Column(db.String(150))
    music_type = db.Column(db.String(150))
    password = db.Column(db.String(150))
    user_id_admin = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

