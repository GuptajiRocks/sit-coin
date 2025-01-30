import os
from psycopg2 import pool, sql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from .env
connection_string = os.getenv('DATABASE_URL')

# Initialize connection pool
connection_pool = pool.SimpleConnectionPool(1, 10, connection_string)

# Check if the pool was created successfully
if connection_pool:
    print("Connection pool created successfully")

# Get a connection from the pool
conn = connection_pool.getconn()
cur = conn.cursor()

# Define table creation queries
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    balance FLOAT NOT NULL DEFAULT 1000.0,
    qr_code TEXT UNIQUE NOT NULL
);
"""

create_transactions_table = """
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    receiver_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    amount FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Execute table creation
cur.execute(create_users_table)
cur.execute(create_transactions_table)

# Commit changes
conn.commit()

print("Tables created successfully!")

# Release connection back to the pool
cur.close()
connection_pool.putconn(conn)
