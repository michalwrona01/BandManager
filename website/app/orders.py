from flask import Blueprint, redirect, request, url_for, render_template
from website.models import User, Band, db, Orders
from flask_login import login_required, current_user

orders = Blueprint('band', __name__)


@orders.route("/manage-your-band/orders/add", methods=['POST'])
@login_required
def add_order():
    if request.method == "POST":
        groom_first_name = request.form.get('groom_first_name')
        groom_surname = request.form.get('groom_surname')
        groom_email = request.form.get('groom_email')
        groom_telephone = request.form.get('groom_telephone')
        bride_first_name = request.form.get('bride_first_name')
        bride_surname = request.form.get('bride_surname')
        bride_email = request.form.get('bride_email')
        bride_telephone = request.form.get('bride_telephone')

