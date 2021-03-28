from flask import Blueprint, redirect, request, url_for, render_template
from website.models import User, Band, db, Orders
from flask_login import login_required, current_user

band = Blueprint('band', __name__)

@band.route('/manage-your-band/<int:band_id>', methods=['GET', 'POST'])
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

    orders = Orders.query.filter_by(band_id=band.id).all()



    return render_template('band_manager.html', user=current_user, band=band, 
                            users_in_this_band=list_with_index_and_user_object, users_without_band=users_without_band, orders=orders)

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

