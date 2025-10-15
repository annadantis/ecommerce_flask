import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',       # default XAMPP user
            password='',       # default XAMPP password is empty
            database='ecommerce_db'
        )
        return conn
    except Error as e:
        print("❌ Error connecting to MySQL:", e)
        return None
