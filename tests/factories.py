from datetime import datetime, timedelta

def event_time_data():
    return {

    }

def make_event(name, determined_priority=None, priority=0, importance=0, start=None, duration=0, tags=""):
    return {
        "name": name,
        "determined_priority": determined_priority,
        "priority": priority,
        "importance": importance,
        "start": start or datetime.now(), 
        # "start": start or datetime(2025, 1, 1, 9, 0), #easier to debug if has stationary time rather than .now()
        "duration": timedelta(minutes=duration),
        "tags": tags,


        # event_Id
        # event_name
        # description

        # start_date
        # due_date
        # end_date


        # importance
        # # ENUM: CRITICAL, HIGH, MEDIUM, LOW, 
        # priority_level

        # #combines priority level and due date (priority_weight * priority_level) + (time_until_due * time_until_due_weight )
        # urgency_score

        # category
        # tags
        # status
        # location
        # attendees




        # is_recurring
        # recursion
        # created_time
        # updates_list


    }

def make_similar_events():
    return {
        "similar_events": [make_event("1Prio", priority=1, start=0, duration=1),make_event("0prio", priority=0, start=10, duration=10)]
    }
