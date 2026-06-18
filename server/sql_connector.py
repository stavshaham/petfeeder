import mariadb
from flask import Flask, g

app = Flask(__name__)

config = {
    'host': '127.0.0.1', # Use 127.0.0.1 if the DB is on the same Pi
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'petfeeder'
}

def get_connection():
    if 'db' not in g:
        g.db = mariadb.connect(**config)
        
    return g.db

def close_connection(e=None):
    db = g.pop('db', None)
    if db is not None:
        try:
            db.close()
        except Exception:
            pass
