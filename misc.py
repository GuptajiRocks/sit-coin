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
# if connection_pool:
#     print("Connection pool created successfully")

# # Get a connection from the pool
# conn = connection_pool.getconn()
# cur = conn.cursor()


# # Commit changes
# conn.commit()

# print("Tables created successfully!")

# # Release connection back to the pool
# cur.close()
# connection_pool.putconn(conn)
