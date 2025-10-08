import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import pandas as pd
import json

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

        # add the ML manager for prediction ability after save event action || import
        self.ml_manager = controller.ml_manager

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
        
        tk.Label(self, text="Participants:").pack(pady=5)
        self.participant_count = tk.Entry(self, width=30)
        self.participant_count.pack(pady=5)
        
               

        ttk.Button(self, text="Save", command=self.save_event).pack(pady=10)

        ttk.Button(self, text="Import", command=self.import_events).pack(pady=10)

        ttk.Button(self, text="< Back to Dashboard",
                   command=lambda: controller.show_frame(controller.frames.keys().__iter__().__next__())).pack(pady=5)

    def save_event(self):
        name = self.event_name.get()
        date = self.event_date.get()
        duration = int(self.event_duration.get())
        actual_priority = int(self.actual_priority.get())
        participant_count = int(self.participant_count.get())

        # if len(date) == 0 or len(name) == 0 or len(duration) == 0:
        #     print("Need to add data to the required  NOT NULL fields: name, date & duration")
        #     return 
        
        
        # Get the date data from user entered string 
        formatted_string_date = datetime.strptime(date, '%m/%d/%y').strftime('%Y-%m-%d')
        # formatted_date = datetime.strptime(formatted_string_date, '%Y-%m-%d')
        formatted_date = datetime.strptime(formatted_string_date, '%Y-%m-%d')

        # calculate the time until event
        remaining_time = self.calculate_time_until_event(formatted_date)
        print("remaining time from today is: ")
        print(remaining_time)
        
        # create event_features dictionary
        event_features = {'event_duration': duration, 'participant_count': participant_count, 'days_until_event': remaining_time}
        predicted_priority = self.ml_manager.predict_priority(event_features)
        
        prediction_content = {
            "Event name": name,
            "correct priority": actual_priority,
            "predicted priority": predicted_priority,
            "remaining days until event": remaining_time
        }
        self.report_create("predicted priority", "add_event", prediction_content) 

        print("predicted priority:")
        print(int(predicted_priority))


        # add event to the database
        event_db_id = self.db_manager.add_event(name, formatted_string_date, duration, actual_priority, predicted_priority, participant_count)
        
        print("after added event, the id produced was: ")
        print(event_db_id)
        
        if event_db_id is not None and event_db_id > -1:
            print(f"Event saved: {name} at {formatted_string_date} represented as: {date}")
            tk.messagebox.showinfo("Saved Event!", "Event now viewable from view events screen")
            print("add_event:save_event: generating and checking report for addition of event")
            content = {
                "Event name": name,
                "correct priority": actual_priority,
                "predicted priority": predicted_priority
            }
            self.report_create("saved event", "add_event", content)
        else:
            print("error happened, the unique id associated is None")
    
    def calculate_time_until_event(self, future_datetime) -> int:
        print("calculating time until event")
        today = date.today()
        time_until_event = future_datetime.date() - today
        days_remaining = time_until_event.days
        return days_remaining

    def import_events(self):
        # exit ui ../ enter data folder /data/ filename
        # output_filepath = "../data/synthetic_training_data.csv"
        output_filepath = "./data/synthetic_training_data_updated.csv"
        DATA_FILE = output_filepath # "synthetic_training_data.csv"
        try:
            df = pd.read_csv(DATA_FILE)
            print("importing data the df looks as such:")
            print(df.head())
            print(f"Data loaded successfully from {DATA_FILE}. Shape: {df.shape}")
        except FileNotFoundError:
            print(f"Error: {DATA_FILE} not found. Run data_generator.py first.")
            return
            
        # Select the columns for add_event
        columns_to_process = [
            'event_name',
            'event_date',
            'event_duration', 
            'actual_priority', 
            'participant_count' 
        ]
        
        # Filter the DataFrame to only used values
        data_subset = df[columns_to_process]

        # Use itertuples to iterate quickly
        for row in data_subset.itertuples(index=False, name='Event'):
            
            # 'row' is a named tuple (Event(duration=60, participants=15, ...))
            # Access elements by name for clarity
            event_name = row.event_name
            date = row.event_date
            duration = row.event_duration
            predicted_priority = row.actual_priority
            # Need to modify the generator to change column label to be generated priority
            actual_priority = row.actual_priority
            participants = row.participant_count
            
            # Calling the existing function with the extracted attributes
            self.db_manager.add_event(event_name, date, duration, actual_priority, predicted_priority, participants)
        data_length_string = str(len(df))+" events imported"
        content = {
            "Imported Data": data_length_string
        }
        self.report_create( "Imported Events", "add_event", content)
        print(f"Successfully added {len(df)} events to the scheduler.")
    
    # takes arguments of :
    # component:    report_title    string 255 char
    # action:       report_type     string 50 char
    # content:      report_content  dict > json
    def report_create(self, title, type, content):
        # add the report to the database
        report_id = self.controller.db_manager.create_report(title, type, content) 
        report_object = self.controller.db_manager.get_report(report_id)
        print("Add_Event: Report create finished")
        print(report_object["report_title"])        
        print(report_object["report_content"])