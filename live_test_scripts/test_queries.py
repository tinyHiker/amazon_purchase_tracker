import sqlite3

# Connect to a database (or create if it doesn't exist)
conn = sqlite3.connect('live_test_scripts/test_database.db')  # This will create a file named 'my_database.db'

# Create a cursor object
cursor = conn.cursor()

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


# Create the 'Users' table
user_data = [
    ('Alice', None),
    ('Bob', None),
    ('Charlie', None)
]

cursor.executemany("INSERT INTO users (name, master) VALUES (?, ?)", user_data)


product_data = [
    ('Product A', 9.99, 1, 5),  # Assuming user with ID 1 (Alice) is linked to this product
    ('Product B', 15.50, 2, 8), # Assuming user with ID 2 (Bob) is linked to this product
    ('Product C', 12.30, 3, 7)  # Assuming user with ID 3 (Charlie) is linked to this product
]

cursor.executemany("INSERT INTO products (name, price, user_id, rating) VALUES (?, ?, ?, ?)", product_data)


query = "SELECT * FROM products"
cursor.execute(query)

# Fetch all rows from the query result
products = cursor.fetchall()

print(products)
print(type(products[1][2]))
# Commit the changes
conn.commit()

# Close the connection
conn.close()