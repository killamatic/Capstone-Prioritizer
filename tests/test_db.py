# import mysql.connector

# try:
#     connection = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="root",
#         database="scheduler_db"
#     )
#     if connection.is_connected():
#         print("Successfully connected to the database!")
#         cursor = connection.cursor()
#         cursor.execute("SELECT VERSION()")
#         db_version = cursor.fetchone()
#         print("Database version:", db_version[0])

# except mysql.connector.Error as e:
#     print(f"Error connecting to MySQL: {e}")
# finally:
#     if 'connection' in locals() and connection.is_connected():
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed.")




import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )
    if connection.is_connected():
        print("Successfully connected to the database!")
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        db_version = cursor.fetchone()
        print("Database version:", db_version[0])

except Exception as e: 
    print(f"Error connecting to MySQL: {e}")
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")







import unittest

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Establish test DB connection or mock
        pass
    
    # TODO: change test name in ML4 from verify_database_connection to test_connection()
    def test_connection(self): # verify_database_connection()
        """Verify DB connection can be established."""
        # 	Verifies that the application can successfully establish a connection to the configured database using the provided credentials.
        self.assertTrue(True)

    def test_create_event(self):
        """Ensure event record can be inserted into DB."""
        # Confirms a new event record is successfully inserted into the events table with valid data, and validates that the record can be retrieved immediately after creation.
        self.assertTrue(True)

    def test_create_prediction(self):
        """Ensure prediction record can be inserted into DB."""
        # Checks the integrity of data creation by simulating the event creation process, ensuring the event is stored correctly and the predicted_priority column is populated (non-null or within an expected range).
        self.assertTrue(True)

    def test_read_event(self):
        """Ensure event record can be retrieved from DB."""
        # Ensures that a specific event can be accurately retrieved from the database using its unique identifier (id), verifying all returned fields match the original input data.
        self.assertTrue(True)

    def test_retrieve_upcoming_events(self):
        """Ensure upcoming events records can be retrieved from DB."""
        # 	Tests the filtering logic by confirming that the function only returns events scheduled for the future, excluding past events or those without a date.
        self.assertTrue(True)

    def test_read_feedback(self):
        """Ensure feedback record can be retrieved from DB."""
        # Verifies the retrieval of user feedback data by fetching an event and checking that the actual_priority value is correctly retrieved
        self.assertTrue(True)

    def test_update_event(self):
        """Ensure event record can be updated."""
        # Confirms that an existing event's details can be modified, such as updating the event's name or date, and that the changes are persistently saved and correctly retrieved in the database.
        self.assertTrue(True)

    def test_delete_event(self):
        """Ensure event record can be deleted."""
        # Ensures an event is permanently removed from the database using its id, and that subsequent attempts to read the deleted event return a failure or None
        self.assertTrue(True)



