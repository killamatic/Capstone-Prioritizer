import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import pandas as pd
import json

class ReportsFrame(ttk.Frame):
    """
    Displaying various project reports using a central, read-only scrolled text area.
    """
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller

        # Store the shared DatabaseManager instance
        self.db_manager = controller.db_manager
        # make sure teh connection is still valid while initializing the frame
        self.db_manager.connect_db()

        self.reports = ["add_event", "view_events", "settings"]
        self.current_report = self.reports[0] # Start with the first report

        # Configure grid for the ReportsFrame
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1) # Text area gets most space
        self.grid_rowconfigure(1, weight=0) # Buttons row is fixed height

        self._setup_report_display()
        self._setup_control_buttons()
        
        # Load the initial report content
        self.show_report(self.current_report)

    def _setup_report_display(self):
        """Sets up the central ScrolledText widget for report viewing."""
        
        # Using scrolledtext provides a built-in scrollbar
        self.report_text = scrolledtext.ScrolledText(
            self, 
            wrap=tk.WORD, 
            state='disabled', # Start as read-only
            font=("Helvetica", 14), 
            padx=10, 
            pady=10,
            bg="#f4f4f4",
            fg="#333333"
        )
        self.report_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

    def _setup_control_buttons(self):
        """Creates the row of buttons at the bottom for report selection."""
        
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Center the buttons in the frame
        button_frame.columnconfigure(0, weight=1)
        
        # Container to hold the actual buttons
        button_container = ttk.Frame(button_frame)
        button_container.grid(row=0, column=0)
        
        for i, report_name in enumerate(self.reports):
            button = ttk.Button(
                button_container, 
                text=report_name,
                command=lambda name=report_name: self.show_report(name)
            )
            button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_container, text="< Back to Dashboard",
                   command=lambda: self.controller.show_frame(self.controller.frames.keys().__iter__().__next__())).pack(pady=5)

    def _generate_report_content(self, report_type):
        listed_reports_dictionary = self.db_manager.get_reports_by_type(report_type)
        print("gotten all reports of type: ")
        print(report_type)

        # varchar(255) is max length of largest attribute
        max_key_length = 150

        # store the string to produce in the screen
        report_lines = [
        f"--- {report_type} ---",
        "" # Blank line
        ]

        # Check if the list is empty
        if not listed_reports_dictionary:
            report_lines.append("No data available for this section.")
            return "\n".join(report_lines)

        # Go over each list element and retrieve data to form report
        # Iterate through each dictionary in the list
        for i, row_dict in enumerate(listed_reports_dictionary):
            
            # Add a row separator for distinct entries, if there are multiple keys
            if len(row_dict) > 2 and i > 0:
                report_lines.append("-" * (max_key_length)) 
                
            # Iterate through the key-value pairs within the dictionary
            for key, value in row_dict.items():
                
                # Format the output line: use f-string alignment
                # The < operator left-aligns the key, using the calculated max_key_length
                formatted_line = f"{key.replace('_', ' ').title():<{max_key_length}}: {value}"
                report_lines.append(formatted_line)
            
            report_lines.append("") # Add a newline after each item block

        # Join all the lines into a single string
        return "\n".join(report_lines)

    def show_report(self, report_name):
        """Updates the text area with the content of the selected report."""
        
        content = self._generate_report_content(report_name)
        
        # Temporarily enable the text widget for editing
        self.report_text.config(state='normal')
        
        # Clear previous content
        self.report_text.delete(1.0, tk.END)
        
        # Insert new content
        self.report_text.insert(tk.END, content)
        
        # Set the widget back to read-only
        self.report_text.config(state='disabled')
        
        self.current_report = report_name
        print(f"Displaying Report: {report_name}")
