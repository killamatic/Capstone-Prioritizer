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

        # retrieve all events that have been predicted on
        # sort into accepted and rejected lists?
        # One hot encode feature of if the user will agree or disagree with the system?
        # datetime transition from date to days until event
        # store portion of each list for testing
        # fit model


        raise NotImplementedError("Training not implemented yet.")

    def score(self, event_name):
        """
        Predict a preference score for an event.
        """
        
        # make the dataframe
        # run prediction method
        # return rounded priority > int

        raise NotImplementedError("Scoring not implemented yet.")
