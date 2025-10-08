import tkinter as tk
from tkinter import ttk
from scheduler.rules import DefaultRules


    # event_id INT AUTO_INCREMENT PRIMARY KEY,
    # event_name VARCHAR(255) NOT NULL,
    # event_date DATETIME NOT NULL,
    # expected_priority INT,
    # resources_required VARCHAR(255),
    # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    # created_by INT,
    # FOREIGN KEY (created_by) REFERENCES users(user_id)
class ViewEventsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Store the shared DatabaseManager instance
        self.db_manager = controller.db_manager
        # make sure the connection is still valid while initializing the frame
        self.db_manager.connect_db()

        self.rules = DefaultRules()

        tk.Label(self, text="Your Events", font=("Helvetica", 14, "bold")).pack(pady=10)

        # Table for displaying events
        self.tree = ttk.Treeview(
            self,
            columns=("Name", "Date", "Duration", "Priority", "Predicted Priority", "Participants"),
            show="headings",
            height=10
        )
        self.tree.heading("Name", text="Event Name")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Duration", text="Duration")
        self.tree.heading("Priority", text="Priority")
        # "Predicted Priority", "Participants"
        self.tree.heading("Predicted Priority", text="Predicted Priority")
        self.tree.heading("Participants", text="Participants")

        self.tree.column("Name", width=200, anchor="w")
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Duration", width=100, anchor="center")
        self.tree.column("Priority", width=80, anchor="center")
        # "Predicted Priority", "Participants"
        self.tree.column("Predicted Priority", width=80, anchor="center")
        self.tree.column("Participants", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True, pady=10)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Refresh",
                   command=self.load_db_events).grid(row=0, column=0, padx=5)
        
        ttk.Button(button_frame, text="Remove Selected Row",
                   command=self.delete_event).grid(row=0, column=1, padx=5)

        ttk.Button(button_frame, text="Confirm Selected",
                   command=self.confirm_event).grid(row=0, column=2, padx=5)

        ttk.Button(button_frame, text="Deny Selected",
                   command=self.deny_event).grid(row=0, column=3, padx=5)
        


        ttk.Button(self, text="< Back to Dashboard",
                   command=lambda: controller.show_frame(controller.frames.keys().__iter__().__next__())).pack(pady=5)

        self.load_db_events()

#     0event_id INT AUTO_INCREMENT PRIMARY KEY, 
#     1event_name VARCHAR(255) NOT NULL,
#     2event_date DATE NOT NULL,
#     3event_duration INT NOT NULL,
#     4predicted_priority INT,
#     5actual_priority INT,
#     6participant_count INT,
#     7created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     8created_by INT,

    """
    Load events into the Treeview from the Db.
    """
    def load_db_events(self):
        # Clear current rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # get all events
        event_list = self.db_manager.get_all_events()

        # TODO: test default rules to sort events
        sorted_event_list = self.rules.sort(event_list)

        # insert each event into the tree
        # for event in event_list:
        for event in sorted_event_list:
            # event_id, event_name, event_date, event_duration, predicted_priority, actual_priority, participant_count, created_at, created_by
            # 0            1          2            3                  4                    5                6               7           8
            # tree values: "Name" 1, "Date" 2, "Duration" 3, "Priority" 5, "Predicted Priority" 4, "Participants" 6
            self.tree.insert("", "end", iid=event[0], values = (event[1], event[2], event[3], event[5], event[4], event[6]))

    def delete_event(self):
        # find the selected event_id
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("no selection", "select a row to delete")
            return

        print(f"the selected item is: {selected_item[0]}")
        event_id = selected_item[0]

        # call the db logic
        if self.db_manager.delete_event_by_id(event_id):
            print(f"successfully removed event with id: {event_id}")
            content = {
                "Deleted event id": event_id
            }
            self.report_create("deleted event", "view_events", content)
            # reload the table to remove content from tree
            self.load_db_events()
        else:
            print(f"failed removal opperation of id: {event_id}")


    def confirm_event(self):
        """Handler for confirming an event."""
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("No selection", "Select a row to confirm")
            return

        event_id = selected_item[0]

        # now that we have the event id, search for a prediction object in the predictions table
        successful_confirmation = self.db_manager.confirm_prediction(event_id)

        # grab information on the row from the cached data
        item_data = self.tree.item(event_id)
        event_name = item_data['values'][0]
        print(f"Confirming event {event_name}")

        if successful_confirmation:
            content = {
                "Confirmed": event_name
            }
            self.report_create("prediction confirmation", "view_events", content)
            tk.messagebox.showinfo("Confirmed", f"Event {event_name} confirmed")

    def deny_event(self):
        """Handler for denying an event."""
        selected_item = self.tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("No selection", "Select a row to deny")
            return

        event_id = selected_item[0]
        successful_denial = self.db_manager.deny_prediction(event_id)
        # grab information on the row from the cached data
        item_data = self.tree.item(event_id)
        event_name = item_data['values'][0]
        print(f"Denying event {event_name}")

        if successful_denial:
            tk.messagebox.showinfo("Denied", f"Event {event_name} denied")
            content = {
                "Denied": event_name
            }
            self.report_create("prediction denial", "view_events", content)
    
    
    # component:    report_title    string 255 char
    # action:       report_type     string 50 char
    # content:      report_content  dict > json
    def report_create(self, component, action, content):
        # add the report to the database
        report_id = self.controller.db_manager.create_report(component, action, content) 
        report_object = self.controller.db_manager.get_report(report_id)
        print("View_Events: Report create finished")
        print(report_object["report_title"])
        print(report_object["report_content"])