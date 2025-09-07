# import tkinter as tk
# from tkinter import ttk, messagebox

# class AddEventWindow(tk.Toplevel):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.title("Add Event")
#         self.geometry("400x300")

#         # Example form fields
#         tk.Label(self, text="Event Name:").pack(pady=5)
#         self.event_name = tk.Entry(self, width=30)
#         self.event_name.pack(pady=5)

#         tk.Label(self, text="Date:").pack(pady=5)
#         self.event_date = tk.Entry(self, width=30)  # Replace with tkcalendar later
#         self.event_date.pack(pady=5)

#         ttk.Button(self, text="Save Event", command=self.save_event).pack(pady=15)

#     def save_event(self):
#         messagebox.showinfo("Saved", f"Event '{self.event_name.get()}' saved!")
#         self.destroy()


import tkinter as tk
from tkinter import ttk


class AddEventFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Add Event", font=("Helvetica", 14, "bold")).pack(pady=10)

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
        print(f"Event saved: {self.event_name.get()} at {self.event_date.get()}")