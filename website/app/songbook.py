from flask import Blueprint, redirect
from flask import request
from flask import url_for
from flask.globals import session
from flask.templating import render_template
from flask_login import current_user, login_required
from website.models import Playlist, Song, Chord
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

def transpose_up(chords_in_music):
    base_chords = ('C', 'D', 'E', 'F', 'G', 'A', 'B')

    new_chords = []

    for chord_in_music in chords_in_music:
        if '#' in chord_in_music:
            i = 0
            for base_chord in base_chords:
                var_chord = chord_in_music
                if chord_in_music.replace('#', '').replace('m', '').replace('7', '') == base_chord:
                    try:
                        new_chords.append(var_chord.replace(base_chord, base_chords[i+1]).replace('#', ''))
                    except IndexError:
                        new_chords.append(var_chord.replace(base_chord, base_chords[0]).replace('#', ''))
                i += 1
        
        else:
            i = 0
            for base_chord in base_chords:
                var_chord = chord_in_music
                if chord_in_music.replace('m', '').replace('7', '') == base_chord:
                    new_chords.append(f'{base_chord}#{var_chord.replace(base_chord, "")}')
                i += 1

    return new_chords

songbook = Blueprint('songbook', __name__)

@songbook.route('/songbook/playlist/add', methods=['GET', 'POST'])
@login_required
def add_playlist():
    if request.method == "POST":
        name_playlist = request.form.get('name_playlist')
        music_type = request.form.get('music_type')
        description_playlist = request.form.get('description_playlist')
        index_id_checked_songs = request.form.getlist('is_checked')

        new_playlist = Playlist(name=name_playlist, band_id=current_user.band_id,
                                music_type=music_type, description=description_playlist)

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

        new_song = Song(name=title, author=author, text=song_text, band_id_created=current_user.band_id)
        db.session.add(new_song)
        db.session.commit()

        for chord in chords_chorus.split(' '):
            new_chord_chours = Chord(chord=chord, chorus=True, verse=False, song_id=new_song.id)
            db.session.add(new_chord_chours)
            db.session.commit()

        for chord in chords_verse.split(' '):
            new_chord_chours = Chord(chord=chord, chorus=False, verse=True, song_id=new_song.id)
            db.session.add(new_chord_chours)
            db.session.commit()

    return redirect(url_for('band.band_manager', band_id=current_user.band_id))

@songbook.route('/songbook/chord/transpose-up/', methods=['GET', 'POST'])
@login_required
def chords_transpose_up():
    if request.method == "POST":
        song_id = request.form.get('song_id_chord')
        chords = Chord.query.filter_by(song_id=song_id).all()

        for chord in chords:
            chord.chord = transpose_up([chord.chord])[0]
        
        db.session.commit()

    return redirect(url_for('band.band_manager', band_id=current_user.band_id)) 

@songbook.route('/playlist/<int:playlist_id>', methods=['GET'])
@login_required
def get_playlist(playlist_id):
    if request.method == "GET":
        playlist = Playlist.query.filter_by(id=playlist_id).first()
        songs = Song.query.filter_by(playlist_id=playlist_id).all()
        chords = Chord.query.filter_by().all()

        return render_template('songs_in_playlist.html', user=current_user, playlist=playlist, songs=songs, chords=chords)
