import tempfile
from scheduler.database_manager import DatabaseManager

def test_saves_and_loads_preferences():
    with tempfile.NamedTemporaryFile() as tmp:
        store = DatabaseManager(db_path=tmp.name)
        store.save({"Yoga": 0.8})
        loaded = store.load()
        assert loaded["Yoga"] == 0.8
