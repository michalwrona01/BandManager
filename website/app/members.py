from flask import Blueprint, redirect, request, url_for
from website.models import Band, User, db
from flask_login import login_required, current_user


members = Blueprint('members', __name__)

@members.route('/manage-your-band/add/<int:user_id>', methods=['POST'])
@login_required
def add_new_member(user_id):
    if request.method == "POST":
        user = User.query.filter_by(id=user_id).first()
        user.band_id = current_user.band_id
        db.session.commit()

    band = Band.query.filter_by(user_id_admin=current_user.id).first()
    return redirect(url_for('band.band_manager', band_id=band.id))

@members.route('/manage-your-band/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_member(user_id):
    if request.method == "POST":
        user = User.query.filter_by(id=user_id).first()
        user.band_id = None
        db.session.commit()

    band = Band.query.filter_by(user_id_admin=current_user.id).first()
    
    return redirect(url_for('band.band_manager', band_id=band.id))

