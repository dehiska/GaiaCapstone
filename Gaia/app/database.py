import sqlite3
from werkzeug.security import generate_password_hash

DATABASE_NAME = 'gaia.db'

def create_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_tables():
    """Create tables in the SQLite database."""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        userid INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        created_at TEXT NOT NULL,
        ismod BOOLEAN NOT NULL DEFAULT 0
    )
    ''')

    conn.commit()
    conn.close()

def insert_user(username, email, password, firstname, lastname, created_at):
    """Insert a new user into the user table."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
    INSERT INTO user (username, email, password, firstname, lastname, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, email, password, firstname, lastname, created_at))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    """Query a user by email."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            'userid': user[0],
            'username': user[1],
            'email': user[2],
            'password': user[3],
            'firstname': user[4],
            'lastname': user[5],
            'created_at': user[6],
            'ismod': user[7]
        }
    return None

def get_user_by_id(userid):
    """Query a user by ID."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE userid = ?', (userid,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            'userid': user[0],
            'username': user[1],
            'email': user[2],
            'password': user[3],
            'firstname': user[4],
            'lastname': user[5],
            'created_at': user[6],
            'ismod': user[7]
        }
    return None