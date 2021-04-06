from website import views
from flask import Blueprint, redirect, request, url_for, render_template, flash
from website.models import User, Band, db, Orders, Bank
from flask_login import login_required, current_user

wallet= Blueprint('wallet', __name__)

@wallet.route('/manage-your-band/donate/user_id=<int:user_id>/band_id=<int:band_id>', methods=['GET', 'POST'])
@login_required
def add_donate(user_id, band_id):
    if request.method == "POST":
        cost = request.form.get("cost")
        description = request.form.get("description")

        if not cost:
            flash("You must enter cost!", category="error")
        elif int(cost) < 0:
            flash("Cost must be greater than zero!", category="error")
        elif not description:
            flash("Your description is empty!", category="error")

        else:
            donate = Bank(user_id=user_id, band_id=band_id, donate=True, cost=cost, description=description)
            db.session.add(donate)
            db.session.commit()

            band = Band.query.filter_by(id=band_id).first()
            band.budget = str(int(band.budget) + int(cost))
            db.session.commit()

            user = User.query.filter_by(id=user_id).first()
            user.wallet = str(int(user.wallet) - int(cost))
            db.session.commit()

            flash("Donate added", category="success")

    return redirect(url_for('band.band_manager', band_id=current_user.band_id))

@wallet.route('/manage-your-band/expense/user_id=<int:user_id>/band_id=<int:band_id>', methods=['GET', 'POST'])
@login_required
def add_expense(user_id, band_id):
    if request.method == "POST":
        cost = request.form.get("cost")
        description = request.form.get("description")

        if not cost:
            flash("You must enter cost!", category="error")
        elif int(cost) < 0:
            flash("Cost must be greater than zero!", category="error")
        elif not description:
            flash("Your description is empty!", category="error")

        else:
            expense = Bank(user_id=user_id, band_id=band_id, expense=True, cost=cost, description=description)
            db.session.add(expense)
            db.session.commit()

            band = Band.query.filter_by(id=band_id).first()
            band.budget = str(int(band.budget) - int(cost))
            db.session.commit()
            flash("Expense added", category="success")

    return redirect(url_for('band.band_manager', band_id=current_user.band_id))

@wallet.route('/manage-your-band/withdraw/user_id=<int:user_id>/band_id=<int:band_id>', methods=['GET', 'POST'])
@login_required
def add_withdraw(user_id, band_id):
    if request.method == "POST":
        cost = request.form.get("cost")
        description = request.form.get("description")

        if not cost:
            flash("You must enter cost!", category="error")
        elif int(cost) < 0:
            flash("Cost must be greater than zero!", category="error")
        elif not description:
            flash("Your description is empty!", category="error")

        else:
            record = Bank(user_id=user_id, band_id=band_id, withdraw=True, cost=cost, description=description)
            db.session.add(record)
            db.session.commit()

            band = Band.query.filter_by(id=band_id).first()
            band.budget = str(int(band.budget) - int(cost))
            db.session.commit()

            user = User.query.filter_by(id=user_id).first()
            user.wallet = str(int(user.wallet) + int(cost))
            db.session.commit()

            flash("Withdraw added", category="success")

    return redirect(url_for('band.band_manager', band_id=current_user.band_id))



