from sqlalchemy.orm import backref
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
    wallet = db.Column(db.Integer, default=0)
    band = db.relationship('Band')
    messages = db.relationship('Message')


class Band(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(150))
    city = db.Column(db.String(150))
    music_type = db.Column(db.String(150))
    password = db.Column(db.String(150))
    user_id_admin = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    budget = db.Column(db.Integer, default=0)
    playlists = db.relationship('Playlist')
    songs = db.relationship('Song')


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)

    groom_firstname = db.Column(db.String(150))
    groom_surname = db.Column(db.String(150))
    groom_telephone = db.Column(db.Integer)
    groom_email = db.Column(db.String(150))

    bride_firstname = db.Column(db.String(150))
    bride_surname = db.Column(db.String(150))
    bride_telephone = db.Column(db.Integer)
    bride_email = db.Column(db.String(150))

    restaurant_name = db.Column(db.String(150))
    restaurant_address = db.Column(db.String(150))

    note = db.Column(db.String(1000))
    price = db.Column(db.Integer, default=0)

    band_id = db.Column(db.Integer)

class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)

    user_id = db.Column(db.Integer)
    band_id = db.Column(db.Integer)

    donate = db.Column(db.Boolean, default=False)
    withdraw = db.Column(db.Boolean, default=False)
    expense = db.Column(db.Boolean, default=False)

    cost = db.Column(db.Integer)

    description = db.Column(db.String(100))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user_id = db.Column(db.Integer)
    title = db.Column(db.String(255))
    content = db.Column(db.String(3000))
    date_time_created = db.Column(db.DateTime(timezone=True), default=func.now())

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50))
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'))
    music_type = db.Column(db.String(20))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.String(300))
    songs = db.relationship('Song')

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    author =db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(3000))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    chords = db.relationship('Chord')
    band_id_created = db.Column(db.Integer, db.ForeignKey('band.id'))

class Chord(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    chord = db.Column(db.String(10))
    chorus = db.Column(db.Boolean)
    verse = db.Column(db.Boolean)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), nullable=False)

    
