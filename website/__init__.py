from flask import Flask
import mysql.connector

def connection_with_data_base():
    connection = mysql.connector.connect(
        database="bandmanage",
        auth_plugin="mysql_native_password",
        host="127.0.0.1",
        port=3306,
        user="root",
        password="",
    )
    return connection

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'xdxdxd'

    connection = connection_with_data_base()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
    
