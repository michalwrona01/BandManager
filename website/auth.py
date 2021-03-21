from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)

@auth.route('/sing-up', methods=['GET', 'POST'])
def sing_up():
    return render_template("sing_up.html")