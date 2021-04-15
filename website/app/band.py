from flask import Blueprint, redirect, request, url_for, render_template
from website.models import User, Band, db, Orders, Bank, Message, Playlist, Song
from flask_login import login_required, current_user

band = Blueprint('band', __name__)

@band.route('/manage-your-band', methods=['GET', 'POST'])
@login_required
def band_manager():
    band_id = request.form.get('band')
    
    band = Band.query.filter_by(id=band_id).first()
    users_in_this_band = User.query.filter_by(band_id=band.id).all()
    users_without_band = User.query.filter_by(band_id=None).all()
    list_with_index_and_user_object = []
    index = 1

    for user in users_in_this_band:
        list_with_index_and_user_object.append([index, user])
        index += 1

    orders = Orders.query.filter_by(band_id=band.id).all()
    bank = Bank.query.filter_by(band_id=band_id).all()

    all_users = User.query.all()

    messages_received = Message.query.filter_by(to_user_id=current_user.id).all()
    list_messages_received = []

    for message in messages_received:
        if message.to_user_id == current_user.id:
            for user in all_users:
                if message.from_user_id == user.id:
                    list_messages_received.append([message.title, user.first_name, user.surname, message.content, message.date_time_created])

    messages_sent = Message.query.filter_by(from_user_id=current_user.id)
    list_messages_sent = []

    for message in messages_sent:
        if message.from_user_id == current_user.id:
            for user in all_users:
                if message.to_user_id == user.id:
                    list_messages_sent.append([message.title, user.first_name, user.surname, message.content, message.date_time_created])
    

    playlists = Playlist.query.filter_by(band_id=current_user.band_id).all()
    songs = Song.query.filter_by().all()
    


    return render_template('band_manager.html', user=current_user, band=band, 
                            users_in_this_band=list_with_index_and_user_object, 
                            users_without_band=users_without_band, 
                            orders=orders, bank=bank, 
                            users_in_this_band_for_wallet=users_in_this_band, 
                            all_users=all_users, list_messages_received=list_messages_received,
                            list_messages_sent=list_messages_sent,
                            playlists=playlists,
                            songs=songs
                            )

@band.route('/manage-your-band/delete/band/<int:band_id>', methods=['POST'])
@login_required
def delete_band(band_id):
    if request.method == "POST":
        users = User.query.filter_by(band_id=band_id).all()
        
        for user in users:
            user.band_id = None

        db.session.commit()

        band = Band.query.filter_by(id=band_id).first()
        db.session.delete(band)
        db.session.commit()

    return redirect(url_for('views.manage_your_band'))

