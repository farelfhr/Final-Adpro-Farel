"""
Student Management System
=========================
A comprehensive OOP-based application demonstrating:
- Encapsulation (private attributes with getters/setters)
- Separation of Concerns (Model, Controller, View)
- GUI development with Tkinter
- File persistence using JSON

Author: Final Assignment - Advanced Programming
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from typing import List, Optional, Dict, Any


# ============================================================================
# CLASS 1: THE MODEL (Student)
# ============================================================================
class Student:
    """
    Represents a single student entity.
    
    This class demonstrates ENCAPSULATION - a fundamental OOP principle
    where we protect data by making attributes private (using double underscore)
    and providing controlled access through public getter and setter methods.
    
    Encapsulation Benefits:
    - Data protection: Prevents direct modification of attributes
    - Validation: Allows us to add validation logic in setters
    - Maintainability: Changes to internal structure don't affect external code
    """
    
    def __init__(self, name: str, student_id: str, major: str) -> None:
        """
        Initialize a Student object with private attributes.
        
        Args:
            name: Student's full name
            student_id: Unique student ID (NIM)
            major: Student's major/field of study
        """
        # ENCAPSULATION: Using double underscore to make attributes private
        # These cannot be accessed directly from outside the class
        self.__name: str = name
        self.__student_id: str = student_id
        self.__major: str = major
    
    # ========================================================================
    # GETTER METHODS (Public interface to read private attributes)
    # ========================================================================
    
    def get_name(self) -> str:
        """
        Getter method for student name.
        This is the proper way to access private attributes.
        
        Returns:
            The student's name
        """
        return self.__name
    
    def get_student_id(self) -> str:
        """
        Getter method for student ID.
        
        Returns:
            The student's ID (NIM)
        """
        return self.__student_id
    
    def get_major(self) -> str:
        """
        Getter method for student major.
        
        Returns:
            The student's major
        """
        return self.__major
    
    # ========================================================================
    # SETTER METHODS (Public interface to modify private attributes)
    # ========================================================================
    
    def set_name(self, name: str) -> None:
        """
        Setter method for student name.
        Allows controlled modification with potential validation.
        
        Args:
            name: New name for the student
        """
        if name.strip():  # Basic validation: name should not be empty
            self.__name = name.strip()
        else:
            raise ValueError("Name cannot be empty")
    
    def set_student_id(self, student_id: str) -> None:
        """
        Setter method for student ID.
        
        Args:
            student_id: New student ID
        """
        if student_id.strip():
            self.__student_id = student_id.strip()
        else:
            raise ValueError("Student ID cannot be empty")
    
    def set_major(self, major: str) -> None:
        """
        Setter method for student major.
        
        Args:
            major: New major for the student
        """
        if major.strip():
            self.__major = major.strip()
        else:
            raise ValueError("Major cannot be empty")
    
    def to_dict(self) -> Dict[str, str]:
        """
        Convert Student object to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the student
        """
        return {
            "name": self.__name,
            "student_id": self.__student_id,
            "major": self.__major
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> 'Student':
        """
        Create a Student object from a dictionary.
        This is a class method used for deserialization.
        
        Args:
            data: Dictionary containing student information
            
        Returns:
            A new Student instance
        """
        return cls(
            name=data["name"],
            student_id=data["student_id"],
            major=data["major"]
        )
    
    def __str__(self) -> str:
        """String representation of the Student object."""
        return f"Student(ID: {self.__student_id}, Name: {self.__name}, Major: {self.__major})"
    
    def __repr__(self) -> str:
        """Official string representation of the Student object."""
        return self.__str__()


# ============================================================================
# CLASS 2: THE LOGIC/CONTROLLER (StudentManager)
# ============================================================================
class StudentManager:
    """
    Manages the collection of Student objects and handles business logic.
    
    This class demonstrates:
    - COMPOSITION: Contains a list of Student objects
    - SINGLE RESPONSIBILITY: Focuses solely on student management operations
    - DATA PERSISTENCE: Handles saving/loading data to/from JSON file
    """
    
    def __init__(self, data_file: str = "students_data.json") -> None:
        """
        Initialize the StudentManager with an empty list and load existing data.
        
        Args:
            data_file: Path to the JSON file for data persistence
        """
        # COMPOSITION: StudentManager "has-a" relationship with Student objects
        self.__students: List[Student] = []
        self.__data_file: str = data_file
        
        # Load existing data from file if it exists
        self.load_from_file()
    
    def add_student(self, name: str, student_id: str, major: str) -> bool:
        """
        Add a new student to the collection.
        
        This method demonstrates:
        - Input validation
        - Duplicate checking
        - Error handling
        
        Args:
            name: Student's name
            student_id: Student's ID (NIM)
            major: Student's major
            
        Returns:
            True if student was added successfully, False otherwise
        """
        # Validation: Check if all fields are provided
        if not name.strip() or not student_id.strip() or not major.strip():
            return False
        
        # Check for duplicate student ID (NIM should be unique)
        if self._find_student_by_id(student_id.strip()) is not None:
            return False
        
        # Create new Student object and add to list
        try:
            new_student = Student(name.strip(), student_id.strip(), major.strip())
            self.__students.append(new_student)
            # Save to file after adding
            self.save_to_file()
            return True
        except Exception:
            return False
    
    def delete_student(self, student_id: str) -> bool:
        """
        Delete a student from the collection by student ID.
        
        Args:
            student_id: The ID of the student to delete
            
        Returns:
            True if student was deleted, False if not found
        """
        student = self._find_student_by_id(student_id)
        if student is not None:
            self.__students.remove(student)
            # Save to file after deletion
            self.save_to_file()
            return True
        return False
    
    def get_all_students(self) -> List[Student]:
        """
        Get a copy of all students in the collection.
        
        Returns:
            List of all Student objects
        """
        # Return a copy to prevent external modification
        return self.__students.copy()
    
    def _find_student_by_id(self, student_id: str) -> Optional[Student]:
        """
        Private helper method to find a student by ID.
        This demonstrates ENCAPSULATION - internal methods are private.
        
        Args:
            student_id: The ID to search for
            
        Returns:
            Student object if found, None otherwise
        """
        for student in self.__students:
            if student.get_student_id() == student_id:
                return student
        return None
    
    def save_to_file(self) -> None:
        """
        Save all students to a JSON file for persistence.
        This ensures data is not lost when the application closes.
        
        Demonstrates FILE I/O operations and JSON serialization.
        """
        try:
            # Convert all Student objects to dictionaries
            data = [student.to_dict() for student in self.__students]
            
            # Write to JSON file
            with open(self.__data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            # In a production app, you might want to log this error
            print(f"Error saving to file: {e}")
    
    def load_from_file(self) -> None:
        """
        Load students from a JSON file.
        This is called during initialization to restore previous data.
        
        Demonstrates FILE I/O operations and JSON deserialization.
        """
        try:
            if os.path.exists(self.__data_file):
                with open(self.__data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Convert dictionaries back to Student objects
                self.__students = [Student.from_dict(item) for item in data]
        except Exception as e:
            # If file doesn't exist or is corrupted, start with empty list
            print(f"Error loading from file: {e}")
            self.__students = []


# ============================================================================
# CLASS 3: THE GUI (StudentApp)
# ============================================================================
class StudentApp:
    """
    Main GUI application for the Student Management System.
    
    This class demonstrates:
    - INHERITANCE: Could inherit from tk.Tk (here we use composition instead)
    - SEPARATION OF CONCERNS: GUI is separate from business logic
    - EVENT-DRIVEN PROGRAMMING: Responds to user interactions
    """
    
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the GUI application.
        
        Args:
            root: The main Tkinter root window
        """
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # COMPOSITION: StudentApp "has-a" StudentManager
        # This separates GUI concerns from business logic
        self.manager = StudentManager()
        
        # Build the GUI
        self._create_widgets()
        
        # Load and display existing students
        self._refresh_student_list()
    
    def _create_widgets(self) -> None:
        """
        Create and arrange all GUI widgets.
        This method demonstrates GUI layout and widget creation.
        """
        # ====================================================================
        # HEADER SECTION
        # ====================================================================
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame,
            text="Student Management System",
            font=("Arial", 16, "bold")
        )
        title_label.pack()
        
        # ====================================================================
        # INPUT SECTION
        # ====================================================================
        input_frame = ttk.LabelFrame(self.root, text="Student Information", padding="15")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Name Entry
        ttk.Label(input_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = ttk.Entry(input_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)
        
        # Student ID Entry
        ttk.Label(input_frame, text="Student ID (NIM):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.id_entry = ttk.Entry(input_frame, width=40)
        self.id_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)
        
        # Major Entry
        ttk.Label(input_frame, text="Major:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.major_entry = ttk.Entry(input_frame, width=40)
        self.major_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW)
        
        # Configure column weights for responsive layout
        input_frame.columnconfigure(1, weight=1)
        
        # ====================================================================
        # BUTTON SECTION
        # ====================================================================
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X, padx=10)
        
        # Add Student Button
        add_btn = ttk.Button(
            button_frame,
            text="Add Student",
            command=self._add_student,
            width=15
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Delete Selected Button
        delete_btn = ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self._delete_student,
            width=15
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear Fields Button
        clear_btn = ttk.Button(
            button_frame,
            text="Clear Fields",
            command=self._clear_fields,
            width=15
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # ====================================================================
        # TABLE SECTION (Treeview)
        # ====================================================================
        table_frame = ttk.LabelFrame(self.root, text="Student List", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create Treeview with columns
        columns = ("ID", "Name", "Student ID", "Major")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Define column headings and widths
        self.tree.heading("ID", text="#")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Student ID", text="Student ID (NIM)")
        self.tree.heading("Major", text="Major")
        
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Name", width=200, anchor=tk.W)
        self.tree.column("Student ID", width=150, anchor=tk.CENTER)
        self.tree.column("Major", width=250, anchor=tk.W)
        
        # Scrollbar for the table
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _add_student(self) -> None:
        """
        Handle the "Add Student" button click event.
        This method demonstrates EVENT HANDLING and USER INPUT VALIDATION.
        """
        # Get values from entry widgets
        name = self.name_entry.get()
        student_id = self.id_entry.get()
        major = self.major_entry.get()
        
        # Validate input
        if not name or not student_id or not major:
            messagebox.showwarning(
                "Validation Error",
                "Please fill in all fields (Name, Student ID, and Major)."
            )
            return
        
        # Attempt to add student through the manager
        if self.manager.add_student(name, student_id, major):
            messagebox.showinfo("Success", f"Student '{name}' has been added successfully!")
            self._clear_fields()
            self._refresh_student_list()
        else:
            # Check if it's a duplicate
            if self.manager._find_student_by_id(student_id):
                messagebox.showerror(
                    "Error",
                    f"Student ID '{student_id}' already exists. Please use a unique ID."
                )
            else:
                messagebox.showerror("Error", "Failed to add student. Please check your input.")
    
    def _delete_student(self) -> None:
        """
        Handle the "Delete Selected" button click event.
        This method demonstrates EVENT HANDLING and USER CONFIRMATION.
        """
        # Get selected item from treeview
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to delete.")
            return
        
        # Get the student ID from the selected row
        item_values = self.tree.item(selected_item[0], "values")
        student_id = item_values[2]  # Student ID is in the 3rd column (index 2)
        student_name = item_values[1]  # Name is in the 2nd column (index 1)
        
        # Confirm deletion
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete student '{student_name}' (ID: {student_id})?"
        )
        
        if confirm:
            if self.manager.delete_student(student_id):
                messagebox.showinfo("Success", f"Student '{student_name}' has been deleted.")
                self._refresh_student_list()
            else:
                messagebox.showerror("Error", "Failed to delete student.")
    
    def _clear_fields(self) -> None:
        """
        Clear all input fields.
        This provides a clean slate for entering new data.
        """
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.major_entry.delete(0, tk.END)
        # Focus on name entry for better UX
        self.name_entry.focus()
    
    def _refresh_student_list(self) -> None:
        """
        Refresh the Treeview table with current student data.
        This method demonstrates DATA BINDING between model and view.
        """
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all students from manager
        students = self.manager.get_all_students()
        
        # Populate treeview
        for index, student in enumerate(students, start=1):
            # Using getter methods to access private attributes (Encapsulation in action!)
            self.tree.insert(
                "",
                tk.END,
                values=(
                    index,
                    student.get_name(),
                    student.get_student_id(),
                    student.get_major()
                )
            )


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
def main() -> None:
    """
    Main function to start the application.
    This follows the standard Python application entry point pattern.
    """
    # Create the root window
    root = tk.Tk()
    
    # Create and run the application
    app = StudentApp(root)
    
    # Start the Tkinter event loop
    root.mainloop()


# Run the application if this file is executed directly
if __name__ == "__main__":
    main()

