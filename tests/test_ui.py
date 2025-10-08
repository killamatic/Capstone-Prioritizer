import unittest
import tkinter as tk
from tkinter import ttk
from unittest.mock import patch, MagicMock

# Application Logic Stub (needed for headless testing)
class AppLogicStub(tk.Tk):
    """
    A self-contained stub class that simulates the required methods and structure 
    of the main application for unit testing purposes.
    """
    def __init__(self):
        # Initialize tkinter root, but immediately minimize or hide it
        super().__init__()
        self.withdraw() # Hides the window for headless testing
        
        # Mocking the essential attributes from the real App class
        self.columns = ("ID", "Duration", "Participants", "Priority")
        self.tree = self._mock_setup_treeview()
        self.load_sample_data()

    def _mock_setup_treeview(self):
        """Creates a real ttk.Treeview instance for state testing."""
        # Using a real Treeview allows testing insertion and retrieval logic accurately
        tree = ttk.Treeview(self, columns=self.columns, show="headings")
        return tree
    
    def load_sample_data(self):
        """Inserts deterministic sample data for selection testing."""
        sample_events = [
            ("A101", 60, 15, 65.2),
            ("B205", 120, 45, 92.8),
        ]
        
        # Insert data, saving the item ID (iid) for easy selection later
        self.item_ids = []
        for event_id, duration, participants, priority in sample_events:
            iid = self.tree.insert("", tk.END, values=(event_id, duration, participants, f"{priority:.1f}"))
            self.item_ids.append(iid)

    def get_selected_attributes(self):
        """
        The actual method from the application we are testing. 
        It retrieves attributes and calls messagebox.showinfo
        """
        selected_items = self.tree.selection()
        
        if not selected_items:
            # This call is patched/mocked in the test below
            tk.messagebox.showinfo("Selection Error", "Please select an event from the list.")
            return

        first_selected_id = selected_items[0]
        item_data = self.tree.item(first_selected_id)
        attributes = item_data['values']
        
        if attributes:
            output = "\n".join([
                f"{self.columns[i]}: {attributes[i]}" 
                for i in range(len(self.columns))
            ])
            # This call is patched/mocked in the test below
            tk.messagebox.showinfo("Selected Event Details", f"Selected Item ID: {first_selected_id}\n\n{output}")
        else:
            tk.messagebox.showerror("Error", "Could not retrieve attributes for the selected item.")


# Unit Test Implementation for UI Logic
class TestUI(unittest.TestCase):
    """Tests the critical user-facing logic of the Regression Scheduler App."""

    def setUp(self):
        """Initializes the mock Tkinter application before each test."""
        # Use the self-contained stub
        self.app = AppLogicStub()

    def tearDown(self):
        """Ensures the Tkinter root object is destroyed after each test."""
        self.app.destroy()

    def test_treeview_data_loading(self):
        """Verifies that the sample data is loaded correctly into the Treeview."""
        # Check the number of rows inserted
        self.assertEqual(len(self.app.tree.get_children()), 2, "Should load 2 sample events.")
        
        # Check the data of the first row
        first_item_id = self.app.item_ids[0]
        data = self.app.tree.item(first_item_id, 'values')
        self.assertEqual(data[0], 'A101', "First event ID should be A101.")
        self.assertEqual(data[3], '65.2', "First event priority should be 65.2.")

    # Patch the messagebox module to prevent GUI pop-ups
    @patch('tkinter.messagebox.showinfo')
    def test_no_selection_error(self, mock_showinfo):
        """Verifies the error message is shown when no item is selected."""
        # Ensure no selection is active
        self.app.tree.selection_remove(self.app.tree.selection())
        
        self.app.get_selected_attributes()
        
        # Assert that messagebox.showinfo was called with the error message
        mock_showinfo.assert_called_once_with(
            "Selection Error", 
            "Please select an event from the list."
        )

    @patch('tkinter.messagebox.showinfo')
    def test_get_selected_attributes(self, mock_showinfo):
        """Simulates selecting a row and verifies the correct data is retrieved and formatted."""
        
        # Simulate the user selecting the second item ('B205')
        second_item_id = self.app.item_ids[1]
        self.app.tree.selection_set(second_item_id)
        
        self.app.get_selected_attributes()
        
        # Define the expected formatted output based on the sample data
        expected_output = (
            f"Selected Item ID: {second_item_id}\n\n"
            "ID: B205\n"
            "Duration: 120\n"
            "Participants: 45\n"
            "Priority: 92.8"
        )
        
        # Assert that messagebox.showinfo was called with the correct details
        mock_showinfo.assert_called_once_with(
            "Selected Event Details", 
            expected_output
        )


if __name__ == '__main__':
    print("Running Tkinter UI Logic Tests (Headless)")
    # This avoids problems with Tkinter's mainloop blocking unittest
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    print("UI Logic Tests Complete")