import sqlite3
from pathlib import Path

class PreferenceStore:
    def __init__(self, db_path="preferences.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        """
        Create the preferences table if it doesn't exist.
        """
        raise NotImplementedError("DB init not implemented yet.")

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
