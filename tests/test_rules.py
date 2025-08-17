from tests.factories import make_event, make_similar_events
from scheduler.rules import DefaultRules
from datetime import datetime

def test_sorts_events_by_priority():
    rules = DefaultRules()
    events = [
        make_event("Low", priority=1),
        make_event("Medium", priority=2),
        make_event("Medium", priority=2),
        make_event("High", priority=3),
    ]
    sorted_events = rules.sort(events)
    assert sorted_events[0]["name"] == "High"
    assert sorted_events[1]["name"] == "Medium"
    assert sorted_events[2]["name"] == "Medium"
    assert sorted_events[3]["name"] == "Low"

def test_sorts_events_by_importance():
    rules = DefaultRules()
    events = [
        make_event("Low", importance=1),
        make_event("Medium", importance=2),
        make_event("High", importance=3),
        make_event("Medium", importance=2),
    ]
    sorted_events = rules.sort(events)
    assert sorted_events[0]["name"] == "High"
    assert sorted_events[1]["name"] == "Medium"
    assert sorted_events[2]["name"] == "Medium"
    assert sorted_events[3]["name"] == "Low"

def test_breaks_priority_ties_by_earliest_start_time():
    rules = DefaultRules()
    events = [
        make_event("B", priority=3, start=datetime(2025,1,1,11,0)),
        make_event("A", priority=3, start=datetime(2025,1,1,9,0)),
    ]
    sorted_events = rules.sort(events)
    assert sorted_events[0]["name"] == "A"

def test_rejects_events_outside_work_hours():
    rules = DefaultRules(work_start=9, work_end=17)
    events = [make_event("Midnight Call", start=datetime(2025,1,1,0,0))]
    filtered_events = rules.filter(events)
    assert len(filtered_events) == 0

# def test_prio_similar_events():
#     rules = DefaultRules()
#     similar = make_similar_events()
#     events = [
#         similar.get(0),
#         similar.get(1),
#     ]
#     sorted_events = rules.priofilter(events)
#     assert sorted_events[0]["name"] == "1Prio"