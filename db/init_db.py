# Create Schema and tables


import mysql.connector
from mysql.connector import errorcode
from db.schema import TABLES

def init_database():
    try:
        # Connect as root or scheduler_user depending on setup
        conn = mysql.connector.connect(
            user="root",
            password="root",
            host="localhost",
            database="scheduler_db"
        )
        cursor = conn.cursor()

        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS scheduler_db")
        cursor.execute("USE scheduler_db")

        # TODO: make users + permissions
        # 2. Create dedicated app user
        # cursor.execute("CREATE USER IF NOT EXISTS 'scheduler_user'@'localhost' IDENTIFIED BY 'StrongPassword123!'")

        # 3. Grant privileges to user
        # cursor.execute("GRANT ALL PRIVILEGES ON scheduler_db.* TO 'scheduler_user'@'localhost'")
        # cursor.execute("FLUSH PRIVILEGES")

        # Create tables
        for table_sql in TABLES:
            cursor.execute(table_sql)

        conn.commit()
        print("Database, user and tables created successfully!")

    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# Make sure the database is pre-made OR initialised when main is run
if __name__ == "__main__":
    init_database()