import tkinter as tk
from ui.dashboard import Dashboard
from ui.add_event import AddEventFrame
# TODO: implement more screens
# from ui.view_events import ViewEventsFrame
# from ui.run_prediction import RunPredictionFrame
# from ui.reports import ReportsFrame

# Navigate between different screens for the user
class SchedulerApp(tk.Tk):
    def __init__(self, username, role):
        super().__init__()

        self.title("Linear Regression Priority Scheduler")
        self.geometry("600x400")

        self.username = username
        self.role = role

        # Container for all frames
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        # Initialize all screens
        # for F in (Dashboard, AddEventFrame, ViewEventsFrame, RunPredictionFrame, ReportsFrame): # How it should look in the future once implemented multiple pages
        for F in (Dashboard, AddEventFrame):#, ViewEventsFrame, RunPredictionFrame, ReportsFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show Dashboard first
        self.show_frame(Dashboard)

    def show_frame(self, frame_class):
        """Bring a frame to the front."""
        frame = self.frames[frame_class]
        frame.tkraise()

if __name__ == "__main__":
    app = SchedulerApp(username="demo_user", role="Normal User")
    app.mainloop()