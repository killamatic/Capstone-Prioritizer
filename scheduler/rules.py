class DefaultRules:
    def __init__(self, work_start=9, work_end=17):
        self.work_start = work_start
        self.work_end = work_end


    # Highest prio to front
    def sort_prio(self, events, feedback=None, descending=True):
        # descending priority sort
        return sorted(events, key=lambda event: event["priority"], reverse=descending)
        # raise NotImplementedError("Sort logic not implemented yet.")

    # Highest importance to front
    def sort_importance(self, events, feedback=None, descending=True):
        # descending priority sort
        # return sorted(events, key=lambda event: event["importance"], reverse=descending)
        raise NotImplementedError("Sort logic not implemented yet.")

    def sort(self, events, feedback=None, descending=True):
        # sort based on importance
        sorted_importance = self.sort_importance(events, descending)
        # descending priority sort
        return self.sort_prio(events, descending)
        # raise NotImplementedError("Sort logic not implemented yet.")

    def filter(self, events, filter):
        raise NotImplementedError("Filter logic not implemented yet.")
    