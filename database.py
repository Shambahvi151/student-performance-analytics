
import mysql.connector


def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anjali@123",
        database="student_db"
    )

    return connection