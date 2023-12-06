from main import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', db.Integer, primary_key = True, autoincrement = True)
    fullname = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))


class Creator(db.Model):
    __tablename__ = 'creator'
    creator_id = db.Column('creator_id', db.Integer, primary_key = True, autoincrement = True)
    creator_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    gender = db.Column(db.String(6))


class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column('admin_id', db.Integer, primary_key = True, autoincrement = True)
    admin_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    gender = db.Column(db.String(6))


class Song(db.Model):
    __tablename__ = 'song'
    song_ID = db.Column('song_ID',  db.Integer, primary_key = True, autoincrement = True)
    file_name = db.Column(db.String(255))
    song_name = db.Column(db.String(255))
    genre = db.Column(db.String(50))
    artist = db.Column(db.String(100))
    lyrics = db.Column(db.String())
    duration = db.Column(db.String())
    dateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    album = db.Column(db.String(255))
    creator_ID  = db.Column(db.Integer)
    album_ID  = db.Column(db.Integer)


class Rating(db.Model):
    __tablename__ = 'rating'
    rating_ID = db.Column('rating_ID', db.Integer, primary_key = True, autoincrement = True, nullable=False)
    user_ID = db.Column(db.Integer, nullable=False)
    song_ID = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)


class Playlist(db.Model):
    __tablename__ = 'playlist'
    playlist_ID = db.Column('playlist_ID', db.Integer, primary_key = True,  autoincrement = True, nullable=False)
    user_ID = db.Column(db.Integer, nullable=False)
    song_ID = db.Column(db.Integer, nullable=False)
    playlist_name = db.Column(db.String(255))


class Creator_Playlist(db.Model):
    __tablename__ = 'creator_playlist'
    playlist_ID = db.Column('playlist_ID', db.Integer, primary_key = True,  autoincrement = True, nullable=False)
    user_ID = db.Column(db.Integer, nullable=False)
    song_ID = db.Column(db.Integer, nullable=False)
    playlist_name = db.Column(db.String(255))


class Album(db.Model):
    __tablename__ = 'album'
    album_ID = db.Column('album_ID', db.Integer, primary_key=True, autoincrement=True, nullable=False)
    album_name = db.Column(db.String(255))
    creator_ID = db.Column(db.Integer)