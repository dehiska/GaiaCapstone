import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('Gaiadb.sqlite3')

# Create a cursor
cursor = conn.cursor()

# Create a table (if it doesn't exist)
#cursor.execute('''
#CREATE TABLE IF NOT EXISTS users (
#    id INTEGER PRIMARY KEY,
#    name TEXT,
#    age INTEGER,
#    email TEXT
#)
#''')

# Insert some data
cursor.execute('''
INSERT INTO user (username, email, phone, password, fullName, password)
VALUES ('dsoul', 'denis@example.com', "2032032033", "Denis Soulima", "123123")
''')

#cursor.execute('''
#INSERT INTO users (name, age, email)
#VALUES ('Bob', 25, 'bob@example.com')
#''')

# Commit the changes
conn.commit()

# Query the database
cursor.execute('SELECT * FROM Users')
print(cursor.fetchall())

# Close the connection
conn.close()
