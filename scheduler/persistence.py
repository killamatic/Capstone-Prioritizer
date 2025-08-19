import sqlite3
from pathlib import Path

class PreferenceStore:
    def __init__(self, db_path="preferences.db"):
        self.db_path = Path(db_path)
        self.conn = None
        self.cursor = None
        self._init_db()


    def _init_db(self):
        """
        Create the users and events table if it doesn't exist.
        """
        raise NotImplementedError("DB init not implemented yet.")
    
    def connect_db(self):
        """
        Attempt a connection to the database
        """
        #Connect to a database file named 'scheduler.db'
        # conn = sqlite3.connect('scheduler.db')
        raise NotImplementedError("connect_db not implemented yet.")

    def save(self, preferences: dict):
        """
        Save preferences to SQLite.
        """
        raise NotImplementedError("Save logic not implemented yet.")

    def load(self) -> dict:
        """
        Load preferences from SQLite.
        """
        raise NotImplementedError("Load logic not implemented yet.")