import tkinter as tk
from tkinter import ttk
# TODO: set up interaction between the database and user input screens 
# from database_manager import DatabaseManager


class ViewEventsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Your Events", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Table for displaying events
        self.tree = ttk.Treeview(
            self,
            columns=("Name", "Date", "Priority"),
            show="headings",
            height=10
        )
        self.tree.heading("Name", text="Event Name")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Priority", text="Priority")

        self.tree.column("Name", width=200, anchor="w")
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Priority", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True, pady=10)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Refresh",
                   command=self.load_events).grid(row=0, column=0, padx=5)
        ttk.Button(self, text="< Back to Dashboard",
                   command=lambda: controller.show_frame(controller.frames.keys().__iter__().__next__())).pack(pady=5)


        # Load sample data for now
        self.load_events()

    def load_events(self):
        """Load events into the Treeview (replace with DB call later)."""
        # Clear current rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # TODO: Mock data (replace this with a DB query in the future)
        mock_events = [
            ("Team Meeting", "2025-09-09", "High"),
            ("Doctor Appointment", "2025-09-10", "Medium"),
            ("Gym", "2025-09-11", "Low"),
        ]

        for event in mock_events:
            self.tree.insert("", "end", values=event)