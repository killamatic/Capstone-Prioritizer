import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import pandas as pd
from datetime import datetime, date

class SettingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Store the shared DatabaseManager instance
        self.db_manager = controller.db_manager
        # make sure teh connection is still valid while initializing the frame
        self.db_manager.connect_db()

        # setup ml for model training button
        self.ml_manager = controller.ml_manager

        tk.Label(self, text="Settings Screen", font=("Helvetica", 14, "bold")).pack(pady=10)


        ttk.Button(self, text="Train ML model", command=self.train_model).pack(pady=10)

        ttk.Button(self, text="Load ML model", command=self.load_model).pack(pady=10)

        ttk.Button(self, text="Change visual theme", command=self.accessability_theme).pack(pady=10)

        ttk.Button(self, text="< Back to Dashboard",
                   command=lambda: controller.show_frame(controller.frames.keys().__iter__().__next__())).pack(pady=5)

    # call the ML component to train on the data in the DB currently
    def train_model(self):
        # pull the data from the Db
        dataframe = self.db_manager.get_all_events_as_dataframe()

        # Go through each row of the dataframe and take the date and turn it into days until event
        time_until_dataframe = self.calculate_days_until_event(dataframe)

        # remove the NAN values from the dataframe: event_id, event_date, event_name, created_at, created_by
        columns_to_drop = [
            'event_id',
            'event_date',
            'event_name',
            'created_at',
            'predicted_priority', #remove this once the model has been trained?
            'created_by'
        ]
        dataframe_cleaned = time_until_dataframe.drop(
        columns=columns_to_drop, 
        axis=1, 
        errors='ignore'
        )   

        trained_r2 = self.ml_manager.train_updated(dataframe_cleaned)
        print("model has been trained")

        training_report_content = {
            "Columns trained on": list(dataframe_cleaned.columns),
            "Achieved r2 accuracy of ": trained_r2
        }
        self.report_create("trained model", "settings", training_report_content)

    def calculate_days_until_event(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the 'event_date' column into an integer representing 
        the number of days until the event from the current date.

        Args:
            df: DataFrame containing the 'event_date' column.

        Returns:
            pd.DataFrame: The modified DataFrame with the new integer column.
        """
        
        # Define the current date (as a naive datetime object for comparison)
        TODAY = pd.Timestamp(date(2025, 10, 8)) 

        # Ensure the 'event_date' column is correctly formatted as datetime objects
        df['event_date'] = pd.to_datetime(df['event_date'])
        
        # Calculate the difference (timedelta)
        time_difference = df['event_date'] - TODAY
        
        # Convert the timedelta result to total days (as a number)
        df['days_until_event'] = time_difference.dt.days
        
        return df

    def load_model(self):
        self.ml_manager.load()
        print("model loaded correctly")

    # Boolean flip for coloration change
    def accessability_theme(self):
        print("theme changed for accessability")

    # takes arguments of :
    # component:    report_title    string 255 char
    # action:       report_type     string 50 char
    # content:      report_content  dict > json
    def report_create(self, component, action, content):
        # add the report to the database
        # report_id = self.controller.db_manager.create_report(component, action, report_dict) 
        report_id = self.controller.db_manager.create_report(component, action, content) 
        report_object = self.controller.db_manager.get_report(report_id)
        print("Add_Event: Report create finished")
        print(report_object["report_title"])        
        print(report_object["report_content"])