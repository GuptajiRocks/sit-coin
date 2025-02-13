# # import qrcode
# # import base64
# # qrdata = "https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox"
# # qr = qrcode.make(qrdata)

# import psycopg2
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env
# load_dotenv()

# # Fetch variables
# USER = os.getenv("user")
# PASSWORD = os.getenv("password")
# HOST = os.getenv("host")
# PORT = os.getenv("port")
# DBNAME = os.getenv("dbname")

# # Connect to the database
# try:
#     connection = psycopg2.connect(
#         user=USER,
#         password=PASSWORD,
#         host=HOST,
#         port=PORT,
#         dbname=DBNAME
#     )
#     print("Connection successful!")
    
#     # Create a cursor to execute SQL queries
#     cursor = connection.cursor()
    
#     # Example query
#     cursor.execute("SELECT NOW();")
#     result = cursor.fetchone()
#     print("Current Time:", result)

#     # Close the cursor and connection
#     cursor.close()
#     connection.close()
#     print("Connection closed.")

# except Exception as e:
#     print(f"Failed to connect: {e}")



# # import os
# # from psycopg2 import pool, sql
# # from dotenv import load_dotenv

# # # Load environment variables
# # load_dotenv()

# # # Get database URL from .env
# # connection_string = os.getenv('DATABASE_URL')

# # # Initialize connection pool
# # connection_pool = pool.SimpleConnectionPool(1, 10, connection_string)

# # # Check if the pool was created successfully
# # # if connection_pool:
# # #     print("Connection pool created successfully")

# # # # Get a connection from the pool
# # # conn = connection_pool.getconn()
# # # cur = conn.cursor()


# # # # Commit changes
# # # conn.commit()

# # # print("Tables created successfully!")

# # # # Release connection back to the pool
# # # cur.close()
# # # connection_pool.putconn(conn)
