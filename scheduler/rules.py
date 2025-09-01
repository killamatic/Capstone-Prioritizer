from datetime import datetime


class DefaultRules:
    def __init__(self, work_start=9, work_end=17):
        self.work_start = work_start
        self.work_end = work_end

        """
        Sorting by use of compound sort.
        """
    def sort(self, events, feedback=None, descending=True):
        # sort based on importance
        # sorted_importance = self.sort_importance(events, descending)
        # # descending priority sort
        # sorted_imp_prio = self.sort_prio(sorted_importance, descending)

        sorted_events = sorted(
            events, 
            key=lambda x: (-x['priority'], -x['importance'], x['start'])
        )

        # return sorted_imp_prio
        return sorted_events
        # raise NotImplementedError("Sort logic not implemented yet.")



    def filter(self, events):
        return list(filter(
        lambda e: self.work_start <= e["start"].hour < self.work_end,
        events
        ))
        # raise NotImplementedError("Filter logic not implemented yet.")
    