import sqlite3

# Connect to a database (or create if it doesn't exist)
conn = sqlite3.connect('database.db')  # This will create a file named 'my_database.db'

# Create a cursor object
cursor = conn.cursor()

# Select all records from the 'users' table
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()  # Fetch all rows of the query result

print("Users:")
for user in users:
    print(user)  # Each 'user' is a tuple representing a row from the 'users' table

# Select all records from the 'products' table
cursor.execute("SELECT * FROM products")
products = cursor.fetchall()  # Fetch all rows of the query result

print("\nProducts:")
for product in products:
    print(product)  # Each 'product' is a tuple representing a row from the 'products' table


# Commit the changes
conn.commit()

# Close the connection
conn.close()