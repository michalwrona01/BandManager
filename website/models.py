import mysql.connector

class User:
    def __init__(self, first_name, surname, email, password):
        self.first_name = first_name
        self.surname = surname
        self.email = email
        self.password = password

class User_Login:
    def __init__(self, user_id, email, is_active):
        self.id = user_id
        self.email = email
        self.is_active = is_active

class Band:
    def __init__(self, name, city, music_type):
        self.name = name
        self.city = city
        self.music_type = music_type

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