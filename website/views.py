from flask import Blueprint, render_template, flash
from flask.globals import request
from .models import connection_with_data_base
import mysql.connector

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/create-new-band', methods=['GET', 'POST'])
def create_new_band():
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        music_type = request.form.get('music_type')

        if len(name) < 2:
            flash("Name must be at least 3 characters.", category="error")
        elif len(city) < 2:
            flash("City must be at least 3 characters.", category="error")
        else:
            try:
                connection = connection_with_data_base()
                cursor = connection.cursor()
                insertQuery = "INSERT INTO bandmanage.bands(name, city, music_type) VALUES(%(name)s, %(city)s, %(music_type)s)"
                insertData = {
                    "name": name,
                    "city": city,
                    "music_type": music_type
                }
                cursor.execute(insertQuery, insertData)
                connection.commit()
                flash("You have been registered.", category="success")
            except mysql.connector.errors.IntegrityError:
                flash("You are already registered.", category="error")
            finally:
                connection.close()

    return render_template('create_new_band.html')