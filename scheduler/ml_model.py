class PreferenceModel:
    def __init__(self, seed=None):
        self.seed = seed
        # in future: load from persistence
        self.model = None

    def train(self, feedback_data):
        """
        Train model incrementally on feedback.
        feedback_data: list of (event_name, accepted)
        """
        raise NotImplementedError("Training not implemented yet.")

    def score(self, event_name):
        """
        Predict a preference score for an event.
        """
        raise NotImplementedError("Scoring not implemented yet.")
