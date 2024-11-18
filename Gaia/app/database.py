# import sqlite3
# #from werkzeug.security import generate_password_hash

# DATABASE_NAME = 'gaia.db'

# def create_connection():
#     """Create a database connection."""
#     conn = sqlite3.connect(DATABASE_NAME)
#     return conn

# def create_tables():
#     """Create tables in the SQLite database."""
#     conn = create_connection()
#     cursor = conn.cursor()

#     # Create `user` table with `recommendations` column
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS user (
#         userid INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT NOT NULL UNIQUE,
#         email TEXT NOT NULL UNIQUE,
#         password TEXT NOT NULL,
#         firstname TEXT NOT NULL,
#         lastname TEXT NOT NULL,
#         created_at TEXT NOT NULL,
#         ismod BOOLEAN NOT NULL DEFAULT 0,
#         recommendations TEXT DEFAULT NULL
#     )
#     ''')

#     conn.commit()
#     conn.close()

# def insert_user(username, email, password, firstname, lastname, created_at):
#     """Insert a new user into the user table."""
#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute(''' 
#     INSERT INTO user (username, email, password, firstname, lastname, created_at)
#     VALUES (?, ?, ?, ?, ?, ?)
#     ''', (username, email, password, firstname, lastname, created_at))
#     conn.commit()
#     conn.close()

# def get_user_by_email(email):
#     """Query a user by email."""
#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM user WHERE email = ?', (email,))
#     user = cursor.fetchone()
#     conn.close()

#     if user:
#         return {
#             'userid': user[0],
#             'username': user[1],
#             'email': user[2],
#             'password': user[3],
#             'firstname': user[4],
#             'lastname': user[5],
#             'created_at': user[6],
#             'ismod': user[7],
#             'recommendations': user[8]  # Access recommendations column
#         }
#     return None

# def get_user_by_id(userid):
#     """Query a user by ID."""
#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM user WHERE userid = ?', (userid,))
#     user = cursor.fetchone()
#     conn.close()

#     if user:
#         return {
#             'userid': user[0],
#             'username': user[1],
#             'email': user[2],
#             'password': user[3],
#             'firstname': user[4],
#             'lastname': user[5],
#             'created_at': user[6],
#             'ismod': user[7],
#             'recommendations': user[8]  # Access recommendations column
#         }
#     return None

# def update_user_recommendations(userid, recommendations):
#     """Update the recommendations column for a user."""
#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute('''
#     UPDATE user
#     SET recommendations = ?
#     WHERE userid = ?
#     ''', (recommendations, userid))
#     conn.commit()
#     conn.close()

# def get_user_recommendations(userid):
#     """Retrieve recommendations for a user."""
#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute('SELECT recommendations FROM user WHERE userid = ?', (userid,))
#     result = cursor.fetchone()
#     conn.close()

#     if result:
#         return result[0]  # Return recommendations as a string
#     return None

# # Add schema verification (optional)
# def verify_user_table_schema():
#     """Verify and adjust the user table schema if needed."""
#     conn = create_connection()
#     cursor = conn.cursor()

#     # Check if the `recommendations` column exists
#     cursor.execute("PRAGMA table_info(user)")
#     columns = cursor.fetchall()
#     column_names = [column[1] for column in columns]

#     if "recommendations" not in column_names:
#         # Add `recommendations` column if it doesn't exist
#         cursor.execute("ALTER TABLE user ADD COLUMN recommendations TEXT DEFAULT NULL")
#         conn.commit()
#         print("Added 'recommendations' column to 'user' table.")

#     conn.close()

# if __name__ == "__main__":
#     # Ensure the tables are created and schema is correct
#     create_tables()
#     verify_user_table_schema()
#     print("Tables created and schema verified successfully!")
import sqlite3

DATABASE_NAME = 'gaia.db'
 
def create_connection():

    """Create a database connection."""

    conn = sqlite3.connect(DATABASE_NAME)

    return conn
 
def create_tables():

    """Create tables in the SQLite database."""

    conn = create_connection()

    cursor = conn.cursor()
 
    # Create `user` table with `recommendations` column

    cursor.execute('''

    CREATE TABLE IF NOT EXISTS user (

        userid INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL UNIQUE,

        email TEXT NOT NULL UNIQUE,

        password TEXT NOT NULL,

        firstname TEXT NOT NULL,

        lastname TEXT NOT NULL,

        created_at TEXT NOT NULL,

        ismod BOOLEAN NOT NULL DEFAULT 0,

        recommendations TEXT DEFAULT NULL

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

            'ismod': user[7],

            'recommendations': user[8] if len(user) > 8 else None # Access recommendations column

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

            'ismod': user[7],

            'recommendations': user[8] if len(user) > 8 else None # Access recommendations column

        }

    return None
 
def update_user_recommendations(userid, recommendations):

    """Update the recommendations column for a user."""

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute('''

    UPDATE user

    SET recommendations = ?

    WHERE userid = ?

    ''', (recommendations, userid))

    conn.commit()

    conn.close()
 
def get_user_recommendations(userid):

    """Retrieve recommendations for a user."""

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute('SELECT recommendations FROM user WHERE userid = ?', (userid,))

    result = cursor.fetchone()

    conn.close()
 
    if result:

        return result[0]  # Return recommendations as a string

    return None
 
# Add schema verification (optional)

def verify_user_table_schema():

    """Verify and adjust the user table schema if needed."""

    conn = create_connection()

    cursor = conn.cursor()
 
    # Check if the `recommendations` column exists

    cursor.execute("PRAGMA table_info(user)")

    columns = cursor.fetchall()

    column_names = [column[1] for column in columns]
 
    if "recommendations" not in column_names:

        # Add `recommendations` column if it doesn't exist

        cursor.execute("ALTER TABLE user ADD COLUMN recommendations TEXT DEFAULT NULL")

        conn.commit()

        print("Added 'recommendations' column to 'user' table.")
 
    conn.close()
 
if __name__ == "__main__":

    # Ensure the tables are created and schema is correct

    create_tables()

    verify_user_table_schema()

    print("Tables created and schema verified successfully!")

 