from scheduler.scheduler import DayScheduler
from factories import make_event
from datetime import datetime

def test_no_overlap_in_schedule():
    scheduler = DayScheduler()
    events = [
        make_event("Meeting", start=datetime(2025,1,1,9,0)),
        make_event("Call", start=datetime(2025,1,1,9,30)),
    ]
    schedule = scheduler.allocate(events)
    assert len(schedule) == 2
    # overlap check (expected to fail now)
    for i, e1 in enumerate(schedule):
        for j, e2 in enumerate(schedule):
            if i != j:
                assert not (e1["start"] < e2["start"] + e2["duration"]
                            and e2["start"] < e1["start"] + e1["duration"])
