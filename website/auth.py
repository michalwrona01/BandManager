from flask import Blueprint, render_template, request, flash

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
            flash("You have been registered.", category="success")

    return render_template("sing_up.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template("login.html")