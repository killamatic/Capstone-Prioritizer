import tkinter as tk
from tkinter import ttk, messagebox
# from ui.dashboard import Dashboard
from datetime import datetime


    # event_id INT AUTO_INCREMENT PRIMARY KEY,
    # event_name VARCHAR(255) NOT NULL,
    # event_date DATETIME NOT NULL,
    # expected_priority INT,
    # resources_required VARCHAR(255),
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

        ttk.Button(self, text="Save", command=self.save_event).pack(pady=10)
        ttk.Button(self, text="< Back to Dashboard",
                   command=lambda: controller.show_frame(controller.frames.keys().__iter__().__next__())).pack(pady=5)

    def save_event(self):
        name = self.event_name.get()
        date = self.event_date.get()
        # TODO: Remove SQL injection ability here
        # TODO: format dates here
        if len(date) == 0 or len(name) == 0:
            print("Need to add data to the required  NOT NULL fields: date & name")
            return 
        formatted_date = datetime.strptime(date, '%m/%d/%y').strftime('%Y-%m-%d')
        # TODO: save event to DB
        self.db_manager.add_event(name, formatted_date)
        # TODO: check that event was added correctly to db
        unique_event_id = self.db_manager.get_event_id_by_event_name(name)
        # TODO: run prediction logic on event and save prediction to Db
        if unique_event_id is not None:
            print(f"Event saved: {name} at {formatted_date} represented as: {date}")
            tk.messagebox.showinfo("Saved Event!", "Event now viewable from view events screen")
        else:
            print("error happened, the unique id associated is None")