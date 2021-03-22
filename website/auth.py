from flask import Blueprint, render_template, request, flash
from .models import connection_with_data_base
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route('/sing-up', methods=['GET', 'POST'])
def sing_up():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(first_name) < 2:
            flash("First name must be at least 3 characters.", category="error")
        elif len(surname) < 2:
            flash("Surname must be at least 3 characters.", category="error")
        elif len(email) < 3:
            flash("Email must be at least 4 characters.", category="error")
        elif len(password1) < 6:
            flash("Password must be at least 7 characters.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        else:
            try:
                hashed_password = generate_password_hash(
                    password1, method='sha256')
                connection = connection_with_data_base()
                cursor = connection.cursor()
                insertQuery = "INSERT INTO bandmanage.users(first_name, surname, email, password) VALUES(%(first_name)s, %(surname)s, %(email)s, %(password)s)"
                insertData = {
                    "first_name": first_name,
                    "surname": surname,
                    "email": email,
                    "password": hashed_password
                }
                cursor.execute(insertQuery, insertData)
                connection.commit()
                flash("You have been registered.", category="success")
            except mysql.connector.errors.IntegrityError:
                flash("You are already registered.", category="error")
            finally:
                connection.close()

    return render_template("sing_up.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        connection = connection_with_data_base()
        cursor = connection.cursor(dictionary=True)
        inserQuery = "SELECT email, password FROM users"
        cursor.execute(inserQuery)

        is_exists = True
        for row in cursor:
            if row["email"] == email:
                is_exists = False
                if check_password_hash(row['password'], password):
                    flash("You just have been logged.", category="success")
                    break
                else:
                    flash("Inccorect password, try again.", category="error")

        if is_exists:
            flash("Account don't exist.", category="error")

    return render_template("login.html")
