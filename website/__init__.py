from flask import Flask
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'aoeijop[4235kldnsf-3qpoiopejf0283482rhgfsoqv=daihfauighe490ge40i'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    from .views import views
    from .auth import auth
    from website.app.band import band
    from website.app.members import members
    from website.app.orders import orders
    from website.app.wallet import wallet
    from website.app.messages import messages
    from website.app.songbook import songbook

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(members, url_prefix='/')
    app.register_blueprint(band, url_prefix='/')
    app.register_blueprint(orders, url_prefix='/')
    app.register_blueprint(wallet, url_prefix='/')
    app.register_blueprint(messages, url_prefix='/')
    app.register_blueprint(songbook, url_prefix='/')

    from .models import User, Band
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app



def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")

