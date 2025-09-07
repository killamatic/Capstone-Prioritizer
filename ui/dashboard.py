import tkinter as tk
from tkinter import ttk, messagebox
from ui.add_event import AddEventWindow 


class Dashboard(tk.Tk):
    def __init__(self, username, role):
        super().__init__()

        self.title("Linear Regression Priority Scheduler - Dashboard")
        self.geometry("600x400")
        self.configure(bg="#f0f0f0")

        self.username = username
        self.role = role

        # Title Label
        title_label = tk.Label(
            self, text=f"Welcome, {self.username} ({self.role})",
            font=("Helvetica", 16, "bold"), bg="#f0f0f0"
        )
        title_label.pack(pady=20)

        # Button Frame
        button_frame = tk.Frame(self, bg="#f0f0f0")
        button_frame.pack(pady=30)

        # Navigation Buttons
        ttk.Button(button_frame, text="Add Event", width=30, command=self.open_add_event).pack(pady=10)
        ttk.Button(button_frame, text="View Events", width=30, command=self.open_view_events).pack(pady=10)
        ttk.Button(button_frame, text="Run Prediction", width=30, command=self.open_run_prediction).pack(pady=10)
        ttk.Button(button_frame, text="Reports", width=30, command=self.open_reports).pack(pady=10)
        ttk.Button(button_frame, text="Exit", width=30, command=self.quit_app).pack(pady=10)

    # Placeholder navigation methods
    def open_add_event(self):
        AddEventWindow(self)
        # messagebox.showinfo("Navigation", "This will open the Add Event screen. To be implemented")

    def open_view_events(self):
        messagebox.showinfo("Navigation", "This will open the View Events screen. To be implemented")

    def open_run_prediction(self):
        messagebox.showinfo("Navigation", "This will run the prediction engine. To be implemented")

    def open_reports(self):
        messagebox.showinfo("Navigation", "This will open the Reports screen. To be implemented")

    def quit_app(self):
        self.destroy()


if __name__ == "__main__":
    # Example: Launch dashboard for a normal user
    # TODO: modify this to read the users login information
    app = Dashboard(username="test_user", role="Normal User")
    app.mainloop()