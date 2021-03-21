from flask import Blueprint, render_template, request
import jsonpickle

auth = Blueprint("auth", __name__)

@auth.route('/sing-up', methods=['GET', 'POST'])
def sing_up():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

    return render_template("sing_up.html")