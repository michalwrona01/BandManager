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