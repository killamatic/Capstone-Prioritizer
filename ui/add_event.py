import tkinter as tk
from tkinter import ttk, messagebox
# from ui.dashboard import Dashboard
from datetime import datetime
import pandas as pd

    # event_id INT AUTO_INCREMENT PRIMARY KEY,
# event_name VARCHAR(255) NOT NULL,
# event_date DATE NOT NULL,
# event_duration INT NOT NULL,
    # predicted_priority INT,
    # actual_priority INT,
    # participant_count INT,
    # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    # created_by INT,
    # FOREIGN KEY (created_by) REFERENCES users(user_id)

class AddEventFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Store the shared DatabaseManager instance
        self.db_manager = controller.db_manager
        # make sure teh connection is still valid while initializing the frame
        self.db_manager.connect_db()

        tk.Label(self, text="Add Event Screen", font=("Helvetica", 14, "bold")).pack(pady=10)

        tk.Label(self, text="Event Name:").pack(pady=5)
        self.event_name = tk.Entry(self, width=30)
        self.event_name.pack(pady=5)

        tk.Label(self, text="Date:").pack(pady=5)
        self.event_date = tk.Entry(self, width=30)
        self.event_date.pack(pady=5)

        tk.Label(self, text="Duration:").pack(pady=5)
        self.event_duration = tk.Entry(self, width=30)
        self.event_duration.pack(pady=5)

        tk.Label(self, text="Priority:").pack(pady=5)
        self.actual_priority = tk.Entry(self, width=30)
        self.actual_priority.pack(pady=5)
        
        # tk.Label(self, text="Duration:").pack(pady=5)
        # self.event_duration = tk.Entry(self, width=30)
        # self.event_duration.pack(pady=5)
        
        # tk.Label(self, text="Duration:").pack(pady=5)
        # self.event_duration = tk.Entry(self, width=30)
        # self.event_duration.pack(pady=5)
        
               

        ttk.Button(self, text="Save", command=self.save_event).pack(pady=10)

        ttk.Button(self, text="Import", command=self.import_events).pack(pady=10)

        ttk.Button(self, text="< Back to Dashboard",
                   command=lambda: controller.show_frame(controller.frames.keys().__iter__().__next__())).pack(pady=5)

    def save_event(self):
        name = self.event_name.get()
        date = self.event_date.get()
        duration = self.event_duration.get()
        actual_priority = self.actual_priority.get()

        # TODO: Remove SQL injection ability here
        # TODO: format dates here
        if len(date) == 0 or len(name) == 0 or len(duration) == 0:
            print("Need to add data to the required  NOT NULL fields: name, date & duration")
            return 
        
        # Get the date data from user entered string 
        formatted_date = datetime.strptime(date, '%m/%d/%y').strftime('%Y-%m-%d')
        # add event to the database
        self.db_manager.add_event(name, formatted_date, duration, actual_priority)
        print("after added event")
        # TODO: check that event was added correctly to db
        unique_event_id = self.db_manager.get_event_id_by_event_name(name)
        # TODO: run prediction logic on event and save prediction to Db
        if unique_event_id is not None:
            print(f"Event saved: {name} at {formatted_date} represented as: {date}")
            tk.messagebox.showinfo("Saved Event!", "Event now viewable from view events screen")
        else:
            print("error happened, the unique id associated is None")
    
    def import_events(self):
        # exit ui ../ enter data folder /data/ filename
        # output_filepath = "../data/synthetic_training_data.csv"
        output_filepath = "./data/synthetic_training_data_updated.csv"
        DATA_FILE = output_filepath # "synthetic_training_data.csv"
        try:
            df = pd.read_csv(DATA_FILE)
            print(f"Data loaded successfully from {DATA_FILE}. Shape: {df.shape}")
        except FileNotFoundError:
            print(f"Error: {DATA_FILE} not found. Run data_generator.py first.")
            return
            
        # 1. Select the columns you actually need for add_event
        # Adjust this list based on the exact features your model and scheduler use
        columns_to_process = [
            'event_name',
            'event_date',
            'event_duration', 
            # 'predicted_priority', 
            'generated_priority', 
            'participants_count' 
        ]
        
        # Filter the DataFrame to only the columns you need
        data_subset = df[columns_to_process]
        
        # get current timestamp for any predictions

        # Use itertuples to iterate quickly
        for row in data_subset.itertuples(index=False, name='Event'):
            
            # 'row' is a named tuple (Event(duration=60, participants=15, ...))
            # Access elements by name for clarity
            event_name = row.event_name
            date = row.event_date
            duration = row.event_duration
            # predicted_priority = row.predicted_priority
            # Need to modify the generator to change column label to be generated priority
            actual_priority = row.generated_priority
            participants = row.participants_count
            
            # formatted_date = datetime.strptime(date, '%m/%d/%y').strftime('%Y-%m-%d')

            # Calling the existing function with the extracted attributes
            # self.add_event(event_name, date, duration, predicted_priority, actual_priority, participants)
            self.db_manager.add_event(event_name, date, duration, actual_priority)
            
            # addition of possible predictions if added to the faking +ML, but no predictions until ML is trained, import data pre ML training
            # prediction_timestamp, predicted_priority, feedback, event_id
            # self.db_manager.add_prediction()

        print(f"Successfully added {len(df)} events to the scheduler.")