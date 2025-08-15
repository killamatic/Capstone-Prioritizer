from datetime import datetime, timedelta

def make_event(name, priority=1, start=None, duration=60):
    return {
        "name": name,
        "priority": priority,
        "start": start or datetime(2025, 1, 1, 9, 0),
        "duration": timedelta(minutes=duration)
    }