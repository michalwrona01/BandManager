from flask import Blueprint, render_template, flash, redirect, url_for
from flask.globals import request
from .models import Band
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
            flash("You have been registered.", category="success")
            return redirect(url_for("views.home"))

            
    return render_template('create_new_band.html', user=current_user)

@views.route('/manage-your-band')
def manage_your_band():
    bands = Band.query.filter_by(user_id_admin=current_user.id).all()
    print(bands)
    return render_template('manage_your_band.html', user=current_user, bands=bands)