from flask import Blueprint, redirect
from flask import request
from flask import url_for
from flask_login import current_user, login_required
from website.models import Playlist, Song
from website.models import db

def from_string_to_html(text):
    text_list = []

    for item in text.strip():
        text_list.append(item)

    attributes = ['h', 'b', 'u', 'p']
    number_to_h_attributes = ['1', '3', '5']
    is_attribute = False
    is_apostrophe = False
    attribute_parameter = ''
    end_text = ''

    new_text = ''

    for letter in text_list:
        
        if letter in attributes and is_attribute != True:
            attribute_type = letter
            is_attribute = True
            
        
        elif is_attribute == True and letter in number_to_h_attributes:
            attribute_parameter = letter
            

        elif letter == "'" and is_apostrophe == False:
            is_apostrophe = True
        
        elif letter == "'" and is_apostrophe == True:
            is_attribute = False
            is_apostrophe = False

            end_text += f'<{attribute_type}{attribute_parameter}>{new_text}</{attribute_type}{attribute_parameter}>'

            is_attribute = False
            is_apostrophe = False
            attribute_parameter = ''
            new_text = ''

        elif letter == '\n':
            new_text += "<br>"
            
        elif is_apostrophe == True:
            new_text += letter
        
        

    return end_text
        


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

@songbook.route('/songbook/song/add', methods=['GET', 'POST'])
@login_required
def add_song():
    if request.method == "POST":
        title = request.form.get('title')
        author = request.form.get('author')
        chords_chorus = request.form.get('chords_chorus')
        chords_verse = request.form.get('chords_verse')
        song_text = from_string_to_html(request.form.get('song_text'))

        new_song = Song(name=title, author=author, text=song_text)
        db.session.add(new_song)
        db.session.commit()


    return redirect(url_for('band.band_manager', band_id=current_user.band_id))

