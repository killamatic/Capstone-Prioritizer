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











import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import joblib

class PriorityModel:
    def __init__(self, model_path="priority_model.pkl"):
        self.model = None
        self.model_path = model_path

    def train(self, data: pd.DataFrame):
        """
        Train the linear regression model.
        Expects data with columns: ['event_duration', 'participants_count', 'resources_required', 'priority_score']
        """
        X = data[['event_duration', 'participants_count', 'resources_required']]
        y = data['priority_score']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)
        r2 = r2_score(y_test, y_pred)

        print(f"Model trained with R² = {r2:.3f}")

        # Save model
        joblib.dump(self.model, self.model_path)

    def load(self):
        """Load saved model from disk."""
        self.model = joblib.load(self.model_path)

    def predict_priority(self, event_features: dict) -> float:
        """
        Predict priority for a single event.
        event_features: {'event_duration': 60, 'participants_count': 10, 'resources_required': 2}
        """
        if not self.model:
            self.load()

        features = [[
            event_features['event_duration'],
            event_features['participants_count'],
            event_features['resources_required']
        ]]

        prediction = self.model.predict(features)[0]
        return prediction