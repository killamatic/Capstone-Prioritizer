class DefaultRules:
    def __init__(self, work_start=9, work_end=17):
        self.work_start = work_start
        self.work_end = work_end

    def sort(self, events, feedback=None):
        raise NotImplementedError("Sort logic not implemented yet.")

    def filter(self, events):
        raise NotImplementedError("Filter logic not implemented yet.")