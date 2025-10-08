import tkinter as tk
from ui.dashboard import Dashboard
from ui.add_event import AddEventFrame
from ui.view_events import ViewEventsFrame
from ui.reports import ReportsFrame
from ui.settings import SettingsFrame

from db.database_manager import DatabaseManager
from ml.ml_model import PriorityModel

# Navigate between different screens for the user
class SchedulerApp(tk.Tk):
    def __init__(self, username, role):
        super().__init__()

        self.title("Linear Regression Priority Scheduler")
        # self.geometry("600x400")
        self.geometry("950x650")

        self.username = username
        self.role = role

        # Create the shared DatabaseManager instance here
        self.db_manager = DatabaseManager(
            host="localhost",
            user="app_user",
            password="your_strong_password",
            database="event_storage_db"
        )
        # set up connection to DB at begin of program run
        self.db_manager.connect_db()

        # Link the Machine learning to the application
        self.ml_manager = PriorityModel()

        # Container for all frames
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Initialize all screens
        for F in (Dashboard, AddEventFrame, ViewEventsFrame, ReportsFrame, SettingsFrame):#, RunPredictionFrame, ReportsFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show Dashboard first
        self.show_frame(Dashboard)

    def show_frame(self, frame_class):
        """Bring a frame to the front."""
        frame = self.frames[frame_class]
        frame.tkraise()

    def on_close(self):
        """Handles closing the application and the database connection."""
        print("Closing the program")
        if self.db_manager:
            self.db_manager.close_db()
        self.destroy()

if __name__ == "__main__":
    app = SchedulerApp(username="demo_user", role="Normal User")
    # Ensure the connection is closed when the window is closed by force or on x out
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()