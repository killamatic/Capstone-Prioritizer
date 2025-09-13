# CRUD opperations + Connection logic


# import sqlite3
from pathlib import Path
import mysql.connector
# from dotenv import load_dotenv
import os

# Database connection parameters
db_config = {
    "host": "localhost",
    "user": "app_user",
    "password": "your_strong_password",
    "database": "event_storage_db"
}


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
        raise NotImplementedError("DB init not implemented yet.")
    
    # redundant at this point
    # def create_connection(config):
    #     """
    #     Creates and returns a connection to the MySQL database.
    #     Returns None if the connection fails.
    #     """
    #     conn = None
    #     try:
    #         conn = mysql.connector.connect(**config)
    #         print("Connection to MySQL DB successful")
    #     except mysql.connector.Error as e:
    #         print(f"Error connecting to MySQL: {e}")
    #     return conn

    def connect_db(self):
        """
        Attempt a connection to the database
        """
        # load_dotenv()

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

    # Artifact code 
    # def get_connection(self):
    #     return mysql.connector.connect(
    #         host="localhost",
    #         # user="scheduler_user",
    #         user="root",
    #         # password="StrongPassword123!",
    #         password="root",
    #         database="scheduler_db"
    #     )

    # artifact code
    # # TODO: Turn this method into general function that takes all possible atrributes    
    # def insert_event(self, name, date, expected_priority, resources):
    #     cursor = self.conn.cursor()
    #     sql = """
    #     INSERT INTO events (event_name, expected_priority, expected_attendance, resources_required)
    #     VALUES (%s, %s, %s, %s)
    #     """
    #     cursor.execute(sql, (name, date, expected_priority, resources))
    #     self.conn.commit()
    #     cursor.close()
    #     self.conn.close()
    







# Evaluate below this line with discussion 9/12/25


    def add_product(self, name, quantity, price):
        """
        Adds a new product to the 'products' table.
        
        Args:
            name (str): The product name.
            quantity (int): The product quantity.
            price (float): The product price.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return

        cursor = self.conn.cursor()
        query = "INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)"
        values = (name, quantity, price)
        try:
            cursor.execute(query, values)
            self.conn.commit()
            print(f"Product '{name}' added successfully.")
        except mysql.connector.Error as err:
            print(f"Error adding product: {err}")
        finally:
            cursor.close()

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
        # query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
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
    def add_event(self, event_name, event_date):
        """
        Adds a new event to the 'events' table.
        
        Args:
            name (str): The product name.
            quantity (int): The product quantity.
            price (float): The product price.

            event_id INT AUTO_INCREMENT PRIMARY KEY,
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
        query = "INSERT INTO events (event_name, event_date) VALUES (%s, %s)"
        values = (event_name, event_date)
        try:
            cursor.execute(query, values)
            self.conn.commit()
            print(f"Product '{event_name}' added successfully.")
        except mysql.connector.Error as err:
            print(f"Error adding product: {err}")
        finally:
            cursor.close()







    def get_all_products(self):
        """
        Retrieves all products from the 'products' table.
        
        Returns:
            list: A list of tuples, where each tuple is a row from the table.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return []

        cursor = self.conn.cursor()
        query = "SELECT * FROM products"
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error getting products: {err}")
            return []
        finally:
            cursor.close()

    def update_product_quantity(self, product_id, new_quantity):
        """
        Updates the quantity of a product in the 'products' table.
        
        Args:
            product_id (int): The ID of the product to update.
            new_quantity (int): The new quantity.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return

        cursor = self.conn.cursor()
        query = "UPDATE products SET quantity = %s WHERE id = %s"
        values = (new_quantity, product_id)
        try:
            cursor.execute(query, values)
            self.conn.commit()
            print(f"Product with ID {product_id} updated successfully.")
        except mysql.connector.Error as err:
            print(f"Error updating product: {err}")
        finally:
            cursor.close()

    def delete_product(self, product_id):
        """
        Deletes a product from the 'products' table.
        
        Args:
            product_id (int): The ID of the product to delete.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return

        cursor = self.conn.cursor()
        query = "DELETE FROM products WHERE id = %s"
        values = (product_id,)
        try:
            cursor.execute(query, values)
            self.conn.commit()
            print(f"Product with ID {product_id} deleted successfully.")
        except mysql.connector.Error as err:
            print(f"Error deleting product: {err}")
        finally:
            cursor.close()

    def delete_all_products(self):
        """
        Deletes all products from the 'products' table.
        """
        if not self.conn or not self.conn.is_connected():
            print("Not connected to the database.")
            return

        cursor = self.conn.cursor()
        query = "DELETE FROM products"
        try:
            cursor.execute(query)
            self.conn.commit()
            print("All products deleted successfully.")
        except mysql.connector.Error as err:
            print(f"Error deleting all products: {err}")
        finally:
            cursor.close()


    # replaced by close_db with more verbosity
    def close(self):
        """Closes the connection when the application is shut down."""
        if self.conn and self.conn.is_connected():
            self.conn.close()
            print("Database connection closed.")

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
            return result
        except mysql.connector.Error as err:
            print(f"Error getting events: {err}")
            return []
        finally:
            cursor.close()


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





# 
if __name__ == '__main__':
    db_manager = DatabaseManager(
        host="localhost",
        user="app_user",
        password="your_strong_password",
        database="event_storage_db"
    )

    # Connect to the database
    db_manager.connect_db()

    # --- CRUD Operation Demonstrations ---

    # C - Create (Add a new product)
    db_manager.add_product("Laptop", 10, 1200.50)
    db_manager.add_product("Mouse", 50, 25.00)

    # R - Read (Get all products)
    products = db_manager.get_all_products()
    print("\nAll products:")
    for product in products:
        print(product)
        db_manager.delete_product(product[0])

    # U - Update (Change the quantity of the laptop)
    # Note: We assume the Laptop has ID 1 for this example.
    # You might get a different ID depending on what's in your DB.
    # db_manager.update_product_quantity(1, 8)

    # # R - Read again to see the changes
    # products = db_manager.get_all_products()
    # print("\nAll products after update:")
    # for product in products:
    #     print(product)

    # # D - Delete (Delete the mouse)
    # # Note: We assume the Mouse has ID 2 for this example.
    # db_manager.delete_product(2)

    # # R - Read one last time
    # products = db_manager.get_all_products()
    # print("\nAll products after deletion:")
    # for product in products:
    #     print(product)

    # Close the connection when all operations are finished
    db_manager.close_db()