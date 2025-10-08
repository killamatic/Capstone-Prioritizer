import tkinter as tk
from tkinter import ttk, messagebox

from ui.add_event import AddEventFrame
from ui.view_events import ViewEventsFrame
from ui.reports import ReportsFrame
from ui.settings import SettingsFrame


class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Store the shared DatabaseManager instance
        self.db_manager = controller.db_manager
        self.ml_manager = controller.ml_manager

        tk.Label(self, text=f"Welcome, {controller.username} ({controller.role})",
                 font=("Helvetica", 14, "bold")).pack(pady=15)

        ttk.Button(self, text="Add Event", width=30,
                   command=lambda: controller.show_frame(AddEventFrame)).pack(pady=10)
        ttk.Button(self, text="View Events", width=30,
                   command=lambda: controller.show_frame(ViewEventsFrame)).pack(pady=10)
        ttk.Button(self, text="Reports", width=30,
                   command=lambda: controller.show_frame(ReportsFrame)).pack(pady=10)
        ttk.Button(self, text="Settings", width=30,
                   command=lambda: controller.show_frame(SettingsFrame)).pack(pady=10)
        ttk.Button(self, text="Exit", width=30,
                   command=controller.quit).pack(pady=10)