class FeedbackTracker:
    def __init__(self):
        # track feedback in-memory for now
        self.preferences = {}

    def record(self, event_name, accepted: bool):
        """
        Record user feedback on an event suggestion.
        """
        raise NotImplementedError("Feedback logic not implemented yet.")

    def score(self, event_name):
        """
        Return a preference score for the given event.
        """
        raise NotImplementedError("Scoring logic not implemented yet.")
