from flask import Blueprint, redirect, request, url_for, render_template, flash
from website.models import User, Band, db, Orders
from flask_login import login_required, current_user

orders = Blueprint('orders', __name__)


@orders.route("/manage-your-band/orders/add", methods=['POST'])
@login_required
def add_order():
    if request.method == "POST":
        groom_firstname = request.form.get('groom_firstname')
        groom_surname = request.form.get('groom_surname')
        groom_email = request.form.get('groom_email')
        groom_telephone = request.form.get('groom_telephone')

        bride_firstname = request.form.get('bride_firstname')
        bride_surname = request.form.get('bride_surname')
        bride_email = request.form.get('bride_email')
        bride_telephone = request.form.get('bride_telephone')

        restaurant_name = request.form.get('restaurant_name')
        restaurant_address = request.form.get('restaurant_address')

        price = request.form.get('price')
        note = request.form.get('note')

        if 2 > len(groom_firstname) or len(groom_firstname) > 15:
            flash("Groom first name must be at least 3 characters.", category="error")
        elif 2 > len(groom_surname) or len(groom_surname) > 15:
            flash("Groom surname must be at least 3 characters.", category="error")
        elif 3 > len(groom_email) or len(groom_email) > 25:
            flash("Groom email must be at least 4 characters.", category="error")
        elif 5 > len(groom_telephone) or len(groom_telephone) > 15:
            flash("Groom telephone number must be at least 6 characters.", category="error")
        elif 2 > len(bride_firstname) or len(bride_firstname )> 15:
            flash("Bride first name must be at least 3 characters.", category="error")
        elif 2 > len(bride_surname) or len(bride_surname ) > 15:
            flash("Bride surname must be at least 3 characters.", category="error")
        elif 3 > len(bride_email) or len(bride_email) > 25:
            flash("Bride email must be at least 4 characters.", category="error")
        elif 5 > len(bride_telephone) or len(bride_telephone) > 15:
            flash("Bride telephone number must be at least 6 characters.", category="error")
        elif 2 > len(restaurant_name) or len(restaurant_name ) > 25:
            flash("Restaurant name must be at least 3 characters.", category="error")
        elif 2 > len(restaurant_address) or len(restaurant_address ) > 45:
            flash("Restaurant address must be at least 3 characters.", category="error")

        else:
            order = Orders(groom_firstname=groom_firstname, groom_surname=groom_surname, groom_email=groom_email, 
                        groom_telephone=groom_telephone, bride_firstname=bride_firstname, bride_surname=bride_surname,
                        bride_email=bride_email, bride_telephone=bride_telephone, restaurant_name=restaurant_name,
                        restaurant_address=restaurant_address, price=price, note=note, band_id=current_user.band_id)

            db.session.add(order)
            db.session.commit()

            flash("Your order just have been added!", category='success')

            return redirect(url_for('band.band_manager', band_id=current_user.band_id))

        return redirect(url_for('band.band_manager', band_id=current_user.band_id))
        

@orders.route("/manage-your-band/orders/get/<int:order_id>", methods=['GET'])
@login_required
def get_order(order_id):
    order = Orders.query.filter_by(id=order_id).first()
    return render_template("order.html", order=order, user=current_user)

@orders.route("/manage-your-band/orders/delete/<int:order_id>", methods=['POST'])
@login_required
def delete_order(order_id):
    order = Orders.query.filter_by(id=order_id).first()
    db.session.delete(order)
    db.session.commit()

    return redirect(url_for('band.band_manager', band_id=current_user.band_id))

