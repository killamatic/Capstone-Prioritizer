import tempfile
from scheduler.persistence import PreferenceStore

def test_saves_and_loads_preferences():
    with tempfile.NamedTemporaryFile() as tmp:
        store = PreferenceStore(db_path=tmp.name)
        store.save({"Yoga": 0.8})
        loaded = store.load()
        assert loaded["Yoga"] == 0.8
