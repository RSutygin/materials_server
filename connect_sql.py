import psycopg2
import os
from dotenv import load_dotenv


load_dotenv('config.env')

db = os.getenv('DB_SQL')
login = os.getenv('LOGIN_SQL')
password = os.getenv('PASSWORD_SQL')
host = os.getenv('HOST_SQL')
port = os.getenv('PORT_SQL')


def connect_to_database():
    try:
        conn = psycopg2.connect(dbname=db, user=login, password=password, host=host, port=port)
        return conn

    except psycopg2.OperationalError as e:
        print(e)
        print('Error to connecting with database')
        return False
