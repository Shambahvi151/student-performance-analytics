
from Database import create_connection

connection = create_connection()

print("Database connected successfully!")

connection.close()