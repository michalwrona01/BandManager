from flask import Blueprint, redirect
from flask import request
from flask import url_for
from flask_login import current_user, login_required
from website.models import Playlist, Song
from website.models import db

songbook = Blueprint('songbook', __name__)

@songbook.route('/songbook/playlist/add', methods=['GET', 'POST'])
@login_required
def add_playlist():
    if request.method == "POST":
        name_playlist = request.form.get('name_playlist')
        music_type = request.form.get('music_type')
        index_id_checked_songs = request.form.getlist('is_checked')

        new_playlist = Playlist(name=name_playlist, band_id=current_user.band_id,
                                music_type=music_type)

        db.session.add(new_playlist)
        db.session.commit()
        
        for index_song in index_id_checked_songs:
            if index_song is not None:
                song = Song.query.filter_by(id=index_song).first()
                song.playlist_id = new_playlist.id
                db.session.commit()


    return redirect(url_for('band.band_manager', band_id=current_user.band_id))