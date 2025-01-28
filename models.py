import sqlite3

# Create database and tables
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    phone INTEGER UNIQUE NOT NULL,
    password TEXT NOT NULL,
    balance REAL NOT NULL
)
''')

connection.commit()
connection.close()
