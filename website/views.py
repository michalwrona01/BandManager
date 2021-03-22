from flask import Blueprint, render_template
from flask.globals import request

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/create-new-band', methods=['GET', 'POST'])
def create_new_band():
    data = request.form.get
    print(data)

    return render_template('create_new_band.html')