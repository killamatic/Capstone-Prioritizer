class FeedbackTracker:
    def __init__(self):
        # track feedback in-memory for until there is a corresponding DB entry, This means that feedback is not persistant yet, and is flushed at every application run
        self.preferences = {}

    def record(self, event_name, accepted: bool):
        """
        Record user feedback on an event suggestion.
        """
        # Store a pointer to the event in the form of an event_name, indicating if the system correctly predicted the event priority with the accepted boolean
        self.preferences[event_name] = accepted
        # raise NotImplementedError("Feedback logic not implemented yet.")

    def score(self, event_name):
        """
        Return a preference score for the given event.
        """
        # obtain the event from the Db based on event_name
        # Obtain the related prediction from the Db
        raise NotImplementedError("Scoring logic not implemented yet.")
