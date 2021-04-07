from flask import Blueprint, request, redirect, flash, url_for
from flask_login import login_required, current_user
from website.models import Message, db

messages = Blueprint('messages', __name__)

@login_required
@messages.route('/messages/add', methods=['GET', 'POST'])
def add_message():
    if request.method == "POST":
        to_user_id = request.form.get('to_user_id')
        topic = request.form.get('title')
        content = request.form.get('content')

        if topic is None:
            flash("Topic field is empty!", category="error")
        elif content is None:
            flash("Content field is empty!", category="error")
        else:
            message = Message(from_user_id=current_user.id, to_user_id=to_user_id, title=topic, content=content)
            db.session.add(message)
            db.session.commit()

            flash("Congratulations! You just sent message!")

    return redirect(url_for('band.band_manager', band_id=current_user.band_id))
        