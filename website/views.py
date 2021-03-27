from flask import Blueprint, render_template, flash, redirect, url_for
from flask.globals import request
from .models import Band, User
from flask_login import current_user, login_required
from . import db


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/create-new-band', methods=['GET', 'POST'])
@login_required
def create_new_band():
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        music_type = request.form.get('music_type')

        band = Band.query.filter_by(name=name).first()
        if band:
            flash("You are already registered.", category="error")
        elif len(name) < 2:
            flash("Name must be at least 3 characters.", category="error")
        elif len(city) < 2:
            flash("City must be at least 3 characters.", category="error")
        else:
            new_band = Band(name=name, city=city, music_type=music_type, password=None, user_id_admin=current_user.id)
            db.session.add(new_band)
            db.session.commit()

            user = User.query.filter_by(id=current_user.id).first()
            user.band_id = new_band.id
            db.session.commit()

            flash("You have been registered.", category="success")
            return redirect(url_for("views.home"))

            
    return render_template('create_new_band.html', user=current_user)

@views.route('/manage-your-band', methods=['GET'])
@login_required
def manage_your_band():
    bands = Band.query.filter_by(id=current_user.band_id).all()
    bands_admin = Band.query.filter_by(user_id_admin=current_user.id).all()

    if bands == [] and bands_admin == []:
        return render_template('manage_your_band.html', user=current_user, bands=[])
    elif bands == []:
        return render_template('manage_your_band.html', user=current_user, bands=bands_admin)
    else:
        return render_template('manage_your_band.html', user=current_user, bands=bands)

    

@views.route('/manage-your-band/<int:band_id>', methods=['GET', 'POST'])
@login_required
def band_manager(band_id):
    band = Band.query.filter_by(id=band_id).first()
    users_in_this_band = User.query.filter_by(band_id=band.id)
    users_without_band = User.query.filter_by(band_id=None).all()
    list_with_index_and_user_object = []
    index = 1

    for user in users_in_this_band:
        list_with_index_and_user_object.append([index, user])
        index += 1



    return render_template('band_manager.html', user=current_user, band=band, 
                            users_in_this_band=list_with_index_and_user_object, users_without_band=users_without_band)

@views.route('/manage-your-band/add/<int:user_id>', methods=['POST'])
@login_required
def add_new_member(user_id):
    if request.method == "POST":
        user = User.query.filter_by(id=user_id).first()
        user.band_id = current_user.band_id
        db.session.commit()

    band = Band.query.filter_by(user_id_admin=current_user.id).first()
    return redirect(url_for('views.band_manager', band_id=band.id))

@views.route('/manage-your-band/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_member(user_id):
    if request.method == "POST":
        user = User.query.filter_by(id=user_id).first()
        user.band_id = None
        db.session.commit()

    band = Band.query.filter_by(user_id_admin=current_user.id).first()
    
    return redirect(url_for('views.band_manager', band_id=band.id))

@views.route('/manage-your-band/delete/band/<int:band_id>', methods=['POST'])
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


@views.route('/community', methods=['GET'])
@login_required
def community_show():
    users  = User.query.all()
    
    return render_template('community.html', user=current_user, users=users)