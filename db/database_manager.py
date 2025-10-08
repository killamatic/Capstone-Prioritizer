# CRUD opperations + Connection logic
from pathlib import Path
import mysql.connector
import pandas as pd 
import os
import json

# Database connection parameters
db_config = {
    "host": "localhost",
    "user": "app_user",
    "password": "your_strong_password",
    "database": "event_storage_db"
}

# TODO: modify db_path field, not used anymore
class DatabaseManager:
    def __init__(self, host, user, password, database, db_path="preferences.db"):
        self.db_path = Path(db_path)
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.user_id = None
        self.conn = None
        self.cursor = None


    def _init_db(self):
        """
        Create the users and events table if it doesn't exist.
        """

    def connect_db(self):
        """
        Attempt a connection to the database
        """
        # ensure the connection is not already present
        if self.conn is not None and self.conn.is_connected():
            print("Connection alrady established")
            return

        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Successful connection to database")
            self.add_user(self.user, "user")
            self.get_user_id_by_username(self.user)
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            self.conn = None

    def close_db(self):
        """
        Closes the database connection.
        """
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Connection closed.")
        else:
            print("No active connection to close.")

    
    
    def get_user_id_by_username(self, username):
        """
        Queries the 'users' table for a user by their username.

        Args:
            username (str): The username to look up.

        Returns:
            int: The unique user ID if found, otherwise None.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return None

        cursor = self.conn.cursor()
        query = "SELECT user_id FROM users WHERE username = %s"
        try:
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                print(f"Got the user id: {result[0]}")
                return result[0]
            else:                
                print("Could not get teh user_id")
                return None
        except mysql.connector.Error as err:
            print(f"Error getting user ID: {err}")
            return None
        finally:
            cursor.close()

    def get_event_id_by_event_name(self, event_name):
        """
        Queries the 'events' table for an event by its event_name.

        Args:
            event_name (str): The name to look up.

        Returns:
            int: The unique event ID if found, otherwise None.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return None

        cursor = self.conn.cursor()
        query = "SELECT event_id FROM events WHERE event_name = %s"
        try:
            cursor.execute(query, (event_name,))
            result = cursor.fetchone()
            if result:
                print(f"Got the event id: {result[0]}")
                return result[0]
            else:                
                print("Could not get the event_id")
                return None
        except mysql.connector.Error as err:
            print(f"Error getting event ID: {err}")
            return None
        finally:
            cursor.close()

    # user_id INT AUTO_INCREMENT PRIMARY KEY,
    # username VARCHAR(100) NOT NULL UNIQUE,
    # role ENUM('admin', 'user') DEFAULT 'user',
    # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    def add_user(self, username, role):
        """
        Adds a new user to the 'users' table.
        If there was already a user, just get their ID
        returns the Db user_id that the new user is associated with
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return None

        cursor = self.conn.cursor()
        query = "INSERT INTO users (username, role) VALUES (%s, %s)"
        try:
            cursor.execute(query, (username, role))
            self.conn.commit()
            print(f"User '{username}' added successfully.")
            self.user_id = cursor.lastrowid
            return self.user_id # Return the ID of the new user to store in memory
        except mysql.connector.Error as err:
            print(f"Error adding user: {err}")
            return None
        finally:
            cursor.close()

    # events schema:
    # event_id INT AUTO_INCREMENT PRIMARY KEY,
    # event_name VARCHAR(255) NOT NULL,
    # event_date DATETIME NOT NULL,
    # expected_priority INT,
    # resources_required VARCHAR(255),
    # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    # created_by INT,
    # FOREIGN KEY (created_by) REFERENCES users(user_id)
    def add_event(self, event_name, event_date, event_duration, actual_priority, predicted_priority, participant_count):
        """
        Adds a new event to the 'events' table.
        
        Args:
            event_name (str): the events name
            event_date (datetime): When the event will happen
            expected_priority (int): What the system has predicted for priority
            resources_required (str)
            created_at (datetime)
            created_by INT,
            FOREIGN KEY (created_by) REFERENCES users(user_id)
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return

        cursor = self.conn.cursor()
        query = "INSERT INTO events (event_name, event_date, event_duration, actual_priority, predicted_priority, participant_count) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (event_name, event_date, event_duration, actual_priority, predicted_priority, participant_count)
        try:
            cursor.execute(query, values)
            event_id_produced = cursor.lastrowid
            print("Db: add_event: event_id was retreived as: ")
            print(event_id_produced)
            self.conn.commit()
            print(f"Event '{event_name}' added successfully under '{event_id_produced}'.")
            return event_id_produced
        except mysql.connector.Error as err:
            print(f"Error adding event: {err}")
            return -1
        finally:
            cursor.close()
            


 # predictions schema:
    # prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    # prediction_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    # predicted_priority INT,
    # feedback boolean,
    # event_id INT NOT NULL,
    # FOREIGN KEY (event_id) REFERENCES events(event_id)
    def add_prediction(self, prediction_timestamp, predicted_priority, feedback, event_id):
        """
        Adds a new prediction to the 'predictions' table.
        
        Args:
            prediction_timestamp, 
            predicted_priority, 
            feedback, 
            event_id
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return

        cursor = self.conn.cursor()
        query = "INSERT INTO predictions (prediction_timestamp, predicted_priority, feedback, event_id) VALUES (%s, %s, %s, %s)"
        values = (prediction_timestamp, predicted_priority, feedback, event_id)
        try:
            cursor.execute(query, values)
            self.conn.commit()
            print(f"Prediction '{event_id}' added successfully.")
            print(f"Predicted Priority '{predicted_priority}'")
        except mysql.connector.Error as err:
            print(f"Error adding event: {err}")
        finally:
            cursor.close()

    def confirm_prediction(self, event_id: int) -> bool:
        """
        Mark a prediction as confirmed (feedback = TRUE).
        Returns True if the update was successful.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return None

        cursor = self.conn.cursor()
        try:
            self.connect_db()
            query = "UPDATE predictions SET feedback = TRUE WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error confirming prediction {event_id}: {e}")
            return False

    def deny_prediction(self, event_id: int) -> bool:
        """
        Mark a prediction as denied (feedback = FALSE).
        Returns True if the update was successful.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return None

        cursor = self.conn.cursor()
        try:
            self.connect_db()
            query = "UPDATE predictions SET feedback = FALSE WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error denying prediction {event_id}: {e}")
            return False

    # Predictions table CRUD methods
    def create_prediction(self, predicted_priority: int, event_id: int, feedback=None) -> int:
        """
        Insert a new prediction record.
        Returns the inserted prediction_id.
        """
        try:
            self.connect_db()
            query = """
                INSERT INTO predictions (predicted_priority, feedback, event_id)
                VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, (predicted_priority, feedback, event_id))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error creating prediction: {e}")
            return None

    def get_prediction(self, prediction_id: int):
        """
        Retrieve a single prediction by ID.
        Returns dict or None.
        """
        try:
            self.connect_db()
            query = "SELECT * FROM predictions WHERE prediction_id = %s LIMIT 1"
            self.cursor.execute(query, (prediction_id,))
            row = self.cursor.fetchone()
            # empty the buffer connection
            self.cursor.fetchall()
            if row:
                return {
                    "prediction_id": row[0],
                    "prediction_timestamp": row[1],
                    "predicted_priority": row[2],
                    "feedback": row[3],
                    "event_id": row[4],
                }
            return None
        except Exception as e:
            print(f"Error fetching prediction {prediction_id}: {e}")
            return None

    def get_all_predictions(self):
        """
        Retrieve all predictions.
        """
        try:
            self.connect_db()
            query = "SELECT * FROM predictions"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [
                {
                    "prediction_id": row[0],
                    "prediction_timestamp": row[1],
                    "predicted_priority": row[2],
                    "feedback": row[3],
                    "event_id": row[4],
                }
                for row in rows
            ]
        except Exception as e:
            print(f"Error fetching all predictions: {e}")
            return []

    def get_prediction_feedback(self, event_id: int):
        """
        Retrieve the feedback status of a prediction.
        Returns True, False, or None if not set.
        """
        try:
            self.connect_db()
            query = "SELECT feedback FROM predictions WHERE event_id = %s"
            self.cursor.execute(query, (event_id,))
            result = self.cursor.fetchone()
            if result is not None:
                return result[0]  # could be True, False
            return None
        except Exception as e:
            print(f"Error retrieving feedback for prediction {event_id}: {e}")
            return None

    def update_prediction_feedback(self, prediction_id: int, feedback: bool) -> bool:
        """
        Update feedback for a prediction.
        Returns True if update succeeded.
        """
        try:
            self.connect_db()
            query = "UPDATE predictions SET feedback = %s WHERE prediction_id = %s"
            self.cursor.execute(query, (feedback, prediction_id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating prediction feedback: {e}")
            return False

    def delete_prediction(self, prediction_id: int) -> bool:
        """
        Delete a prediction by ID.
        """
        try:
            self.connect_db()
            query = "DELETE FROM predictions WHERE prediction_id = %s"
            self.cursor.execute(query, (prediction_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting prediction {prediction_id}: {e}")
            return False




    # Reports CRUD methods
    def create_report(self, report_title: str, report_type: str, report_content: dict) -> int:
        """
        Insert a new report. Report content is stored as JSON.
        Returns report_id.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return None

        cursor = self.conn.cursor()

        print("DB:Create report")
        try:
            self.connect_db()
            query = """
                INSERT INTO reports (report_title, report_type, report_content) VALUES (%s, %s, %s)
            """
            report_json = json.dumps(report_content)
            values = (report_title, report_type, report_json)

            print("made json")
            cursor.execute(query, values)
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating report: {e}")
            return None

    def get_report(self, report_id: int) -> dict:
        """
        Retrieve a single report by ID.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return None

        cursor = self.conn.cursor()
        print("DB:Get report")
        try:
            self.connect_db()
            query = "SELECT * FROM reports WHERE report_id = %s LIMIT 1"
            cursor.execute(query, (report_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "report_id": row[0],
                    "report_title": row[1],
                    "report_type": row[2],
                    "report_content": json.loads(row[3]) if row[3] else None,
                    "report_timestamp": row[4]
                }
            return None
        except Exception as e:
            print(f"Error fetching report {report_id}: {e}")
            return None
        
    def get_reports_by_type(self, report_type: str) -> list[dict]:
        """
        Retrieve all reports matching the given report type.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return None

        # Initialize an empty list to hold the structured report objects
        all_reports = [] 
        
        cursor = self.conn.cursor()
        print(f"DB: Getting all reports of type: {report_type}")
        
        try:
            self.connect_db() 
            
            query = "SELECT report_id, report_title, report_type, report_content, report_timestamp FROM reports WHERE report_type = %s"
            cursor.execute(query, (report_type,))
            
            all_rows = cursor.fetchall() 
            print("inside get_reports_by_type: inside try: all rows retrieved: ")
            print(all_rows)
            if all_rows:
                
                for row in all_rows:
                    # Convert each row (tuple) into a structured dictionary
                    report_obj = {
                        "report_id": row[0],
                        "report_title": row[1],
                        "report_type": row[2],
                        # Deserialize the JSON content back into a python dictionary
                        "report_content": json.loads(row[3]) if row[3] else None,
                        "report_timestamp": row[4]
                    }
                    all_reports.append(report_obj)
                print("list fully inserted into")
                # Return the list of all structured reports
                return all_reports 
            # Return an empty list if no rows returned in above if
            return [] 
            
        except Exception as e:
            print(f"Error fetching reports of type {report_type}: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def get_all_reports(self):
        """
        Retrieve all reports.
        """
        try:
            import json
            self.connect_db()
            query = "SELECT * FROM reports"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [
                {
                    "report_id": row[0],
                    "report_title": row[1],
                    "report_type": row[2],
                    "report_content": json.loads(row[3]) if row[3] else None,
                    "report_timestamp": row[4],
                }
                for row in rows
            ]
        except Exception as e:
            print(f"Error fetching all reports: {e}")
            return []

    def update_report(self, report_id: int, report_title=None, report_type=None, report_content=None) -> bool:
        """
        Update a report's fields. Only updates non-None fields.
        """
        try:
            import json
            self.connect_db()
            fields = []
            values = []

            if report_title is not None:
                fields.append("report_title = %s")
                values.append(report_title)
            if report_type is not None:
                fields.append("report_type = %s")
                values.append(report_type)
            if report_content is not None:
                fields.append("report_content = %s")
                values.append(json.dumps(report_content))

            if not fields:
                return False  # nothing to update

            query = f"UPDATE reports SET {', '.join(fields)} WHERE report_id = %s"
            values.append(report_id)
            self.cursor.execute(query, tuple(values))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating report {report_id}: {e}")
            return False

    def delete_report(self, report_id: int) -> bool:
        """
        Delete a report by ID.
        """
        try:
            self.connect_db()
            query = "DELETE FROM reports WHERE report_id = %s"
            self.cursor.execute(query, (report_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting report {report_id}: {e}")
            return False


    def get_user_count(self):
        """Example method to query the database."""
        if not self.conn or not self.conn.is_connected():
            print("Connection Error: Not connected to the database.")
            return 0
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except mysql.connector.Error as err:
            print(f"Database Error: Query failed: {err}")
            return 0


    def get_all_events(self):
        """
        Retrieves all events from the 'events' table.
        
        Returns:
            list: A list of tuples, where each tuple is a row from the table.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return []

        cursor = self.conn.cursor()
        query = "SELECT * FROM events"
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            column_names = [i[0] for i in cursor.description]

            print("The column names are: ")
            print(column_names)
            
            return result
        except mysql.connector.Error as err:
            print(f"Error getting events: {err}")
            return []
        finally:
            cursor.close()

    def get_all_events_as_dataframe(self) -> pd.DataFrame:
        """
        Retrieves all events from the 'predictions' table and returns them as a Pandas DataFrame.
        This is the most efficient method for preparing data for machine learning.
        
        Returns:
            pd.DataFrame: DataFrame containing all event data.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return pd.DataFrame()

        cursor = self.conn.cursor()
        # possible left join to use in future implementation
        # query = """
        #         SELECT
        #             e.*,
        #             p.predicted_priority,
        #             p.feedback
        #         FROM
        #             events e
        #         LEFT JOIN
        #             predictions p ON e.event_id = p.event_id
        #     """
        query = "SELECT * FROM events"

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            # column names from the cursor description
            # The cursor's description attribute holds metadata about the columns.
            # Each item in the description is a tuple, and the column name is the first element (index 0).
            column_names = [i[0] for i in cursor.description]
    
            # Create the DataFrame
            df = pd.DataFrame(result, columns=column_names)

            # Clean Data (Filter out rows without user feedback)
            # Only train the model on data where the user has confirmed or denied the prediction.
            # df_training = df.dropna(subset=['feedback'])

            # return df_training
            return df
        except mysql.connector.Error as err:
            print(f"Error getting events: {err}")
            return pd.DataFrame()
        finally:
            cursor.close()

    def update_event(self, event_id: int, feedback: bool) -> bool:
        """
        Update event attributes.
        Returns True if update succeeded.
        """
        try:
            self.connect_db()
            query = "UPDATE events SET feedback = %s WHERE event_id = %s"
            self.cursor.execute(query, (feedback, event_id))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating event: {e}")
            return False

    def delete_event_by_id(self, event_id):
        """
        Deletes a single event from the database by its unique ID.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return False

        cursor = self.conn.cursor()
        query = "DELETE FROM events WHERE event_id = %s"
        try:
            cursor.execute(query, (event_id,))
            self.conn.commit()
            print(f"Event with ID {event_id} deleted successfully.")
            return True
        except mysql.connector.Error as err:
            print(f"Error deleting event: {err}")
            return False
        finally:
            cursor.close()