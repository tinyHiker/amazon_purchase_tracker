import sqlite3

# Connect to a database (or create if it doesn't exist)
conn = sqlite3.connect('database.db')  # This will create a file named 'my_database.db'

# Create a cursor object
cursor = conn.cursor()

# Create the 'Users' table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        master INTEGER REFERENCES users(id) CHECK (master != id)
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        bought INTEGER NOT NULL DEFAULT 0 CHECK (bought IN (0, 1)),
        user_id INTEGER,
        rating INTEGER CHECK (rating >= 1 AND rating <= 10),
        FOREIGN KEY (user_id) REFERENCES Users(id)
    )
    ''')


# Commit the changes
conn.commit()

# Close the connection
conn.close()