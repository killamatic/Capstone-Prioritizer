from datetime import datetime


class DefaultRules:
    def __init__(self, work_start=9, work_end=17):
        self.work_start = work_start
        self.work_end = work_end

    """
    Sorting by compound sort.
    events: ['event_id', 'event_name', 'event_date', 'event_duration', 'predicted_priority', 
        'actual_priority', 'participant_count', 'created_at', 'created_by']
    
    """
    def sort(self, events, descending=True):
        # sort based on importance
        # sorted_importance = self.sort_importance(events, descending)
        # # descending priority sort
        # sorted_imp_prio = self.sort_prio(sorted_importance, descending)
        actual_priority_index = 5
        participant_count_index = 6
        sorted_events = sorted(
            events, 
            # key=lambda x: (-x['actual_priority'], -x['participant_count'], x['start'])
            key=lambda x: (-x[actual_priority_index], -x[participant_count_index])
        )

        # return sorted_imp_prio
        return sorted_events
        # raise NotImplementedError("Sort logic not implemented yet.")


    """
    Only show events during work hours
    """
    def filter(self, events):
        return list(filter(
        lambda e: self.work_start <= e["start"].hour < self.work_end,
        events
        ))
        # raise NotImplementedError("Filter logic not implemented yet.")
    