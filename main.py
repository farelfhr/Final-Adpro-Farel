"""
Student Management System
=========================
A comprehensive OOP-based application demonstrating:
- Encapsulation (private attributes with getters/setters)
- Inheritance and Polymorphism (Person -> Student, get_details)
- Separation of Concerns (Model, Manager, App)
- GUI development with Tkinter (styles, Treeview, Toplevel)
- File persistence using JSON

Author: Muhammad Farel Alfathir - Final Assignment (Advanced Programming)
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Dict


# ============================================================================
# CUSTOM EXCEPTION FOR VALIDATION
# ============================================================================
class ValidationError(Exception):
    """
    Custom exception type used for validation errors.

    Using a custom exception (instead of generic ValueError) makes the
    intent of the error clearer and demonstrates how to create domain-
    specific exceptions in OOP.
    """


# ============================================================================
# BASE MODEL CLASS: Person (used for INHERITANCE & POLYMORPHISM)
# ============================================================================
class Person:
    """
    Base class representing a generic person.

    This class introduces:
    - INHERITANCE: Other classes (like Student) will inherit from Person.
    - ENCAPSULATION: Private attributes with getters and setters.
    - POLYMORPHISM: The get_details method can be overridden by subclasses.
    """

    def __init__(self, name: str, person_id: str) -> None:
        """
        Initialize a Person with private attributes.

        Args:
            name: Person's full name.
            person_id: Unique identifier (e.g. ID, NIM).
        """
        self.__name: str = name
        self.__id: str = person_id

    # ---------------------------------------------------------------------
    # Getter methods
    # ---------------------------------------------------------------------
    def get_name(self) -> str:
        """Return the person's name."""
        return self.__name

    def get_id(self) -> str:
        """Return the person's identifier."""
        return self.__id

    # ---------------------------------------------------------------------
    # Setter methods with validation and custom exceptions
    # ---------------------------------------------------------------------
    def set_name(self, name: str) -> None:
        """
        Set the person's name, with simple validation.

        Raises:
            ValidationError: If the provided name is empty.
        """
        if not name.strip():
            raise ValidationError("Name cannot be empty.")
        self.__name = name.strip()

    def set_id(self, person_id: str) -> None:
        """
        Set the person's identifier, with simple validation.

        Raises:
            ValidationError: If the provided ID is empty.
        """
        if not person_id.strip():
            raise ValidationError("ID cannot be empty.")
        self.__id = person_id.strip()

    # ---------------------------------------------------------------------
    # POLYMORPHIC METHOD
    # ---------------------------------------------------------------------
    def get_details(self) -> str:
        """
        Return a human-readable description of the person.

        This method is designed for POLYMORPHISM: subclasses such as
        Student will override this method to provide more specific details.
        """
        return f"Person(ID: {self.__id}, Name: {self.__name})"


# ============================================================================
# CLASS 1: THE MODEL (Student)
# ============================================================================
class Student(Person):
    """
    Represents a single student entity.

    This class demonstrates:
    - ENCAPSULATION: Private attribute for major with getter/setter.
    - INHERITANCE: Inherits common attributes (name, ID) from Person.
    - POLYMORPHISM: Overrides get_details from the Person base class.
    """

    def __init__(self, name: str, student_id: str, major: str) -> None:
        """
        Initialize a Student object with private attributes.

        Args:
            name: Student's full name.
            student_id: Unique student ID (NIM).
            major: Student's major/field of study.
        """
        super().__init__(name=name, person_id=student_id)
        self.__major: str = major

    # ========================================================================
    # ADDITIONAL GETTERS/SETTERS
    # ========================================================================
    def get_student_id(self) -> str:
        """
        Convenience wrapper around base class ID getter.

        Returns:
            The student's ID (NIM).
        """
        return self.get_id()

    def get_major(self) -> str:
        """
        Getter method for student major.

        Returns:
            The student's major.
        """
        return self.__major

    def set_major(self, major: str) -> None:
        """
        Setter method for student major using custom validation.

        Args:
            major: New major for the student.

        Raises:
            ValidationError: If major is empty.
        """
        if not major.strip():
            raise ValidationError("Major cannot be empty.")
        self.__major = major.strip()

    # ---------------------------------------------------------------------
    # POLYMORPHIC METHOD OVERRIDE
    # ---------------------------------------------------------------------
    def get_details(self) -> str:
        """
        Overridden version of Person.get_details.

        Demonstrates POLYMORPHISM: the same method name behaves
        differently for a Student instance than for a generic Person.
        """
        return (
            f"Student(ID: {self.get_student_id()}, "
            f"Name: {self.get_name()}, Major: {self.__major})"
        )

    # ---------------------------------------------------------------------
    # SERIALIZATION HELPERS
    # ---------------------------------------------------------------------
    def to_dict(self) -> Dict[str, str]:
        """
        Convert Student object to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the student.
        """
        return {
            "name": self.get_name(),
            "student_id": self.get_student_id(),
            "major": self.__major,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "Student":
        """
        Create a Student object from a dictionary.

        Args:
            data: Dictionary containing student information.

        Returns:
            A new Student instance.
        """
        return cls(
            name=data["name"],
            student_id=data["student_id"],
            major=data["major"],
        )

    def __str__(self) -> str:
        """String representation of the Student object."""
        return self.get_details()

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
    - COMPOSITION: Contains a list of Student objects.
    - SINGLE RESPONSIBILITY: Focuses solely on student management operations.
    - DATA PERSISTENCE: Handles saving/loading data to/from JSON file.
    """

    def __init__(self, data_file: str = "students_data.json") -> None:
        """
        Initialize the StudentManager with an empty list and load existing data.

        Args:
            data_file: Path to the JSON file for data persistence.
        """
        self.__students: List[Student] = []
        self.__data_file: str = data_file

        # Load existing data from file if it exists
        self.load_from_file()

    # ---------------------------------------------------------------------
    # CRUD OPERATIONS
    # ---------------------------------------------------------------------
    def add_student(self, name: str, student_id: str, major: str) -> bool:
        """
        Add a new student to the collection.

        This method demonstrates:
        - Input validation
        - Duplicate checking
        - Error handling

        Args:
            name: Student's name.
            student_id: Student's ID (NIM).
            major: Student's major.

        Returns:
            True if student was added successfully, False otherwise.
        """
        if not name.strip() or not student_id.strip() or not major.strip():
            return False

        # Check for duplicate student ID (NIM should be unique)
        if self._find_student_by_id(student_id.strip()) is not None:
            return False

        try:
            new_student = Student(name.strip(), student_id.strip(), major.strip())
            self.__students.append(new_student)
            self.save_to_file()
            return True
        except ValidationError:
            return False

    def update_student(
        self,
        original_student_id: str,
        new_name: str,
        new_student_id: str,
        new_major: str,
    ) -> bool:
        """
        Update an existing student's data.

        Args:
            original_student_id: The current ID of the student to update.
            new_name: New name for the student.
            new_student_id: New ID (NIM) for the student.
            new_major: New major for the student.

        Returns:
            True if update was successful, False otherwise.
        """
        student = self._find_student_by_id(original_student_id)
        if student is None:
            return False

        new_student_id_stripped = new_student_id.strip()
        # If changing ID, ensure uniqueness
        if (
            new_student_id_stripped != original_student_id
            and self._find_student_by_id(new_student_id_stripped) is not None
        ):
            return False

        try:
            student.set_name(new_name)
            student.set_id(new_student_id_stripped)
            student.set_major(new_major)
            self.save_to_file()
            return True
        except ValidationError:
            return False

    def delete_student(self, student_id: str) -> bool:
        """
        Delete a student from the collection by student ID.

        Args:
            student_id: The ID of the student to delete.

        Returns:
            True if student was deleted, False if not found.
        """
        student = self._find_student_by_id(student_id)
        if student is not None:
            self.__students.remove(student)
            self.save_to_file()
            return True
        return False

    def get_all_students(self) -> List[Student]:
        """
        Get a copy of all students in the collection.

        Returns:
            List of all Student objects.
        """
        return self.__students.copy()

    def search_students(self, query: str) -> List[Student]:
        """
        Search for students by name or ID.

        This method demonstrates basic search/filter logic.

        Args:
            query: Text to search in name or ID (case-insensitive).

        Returns:
            List of matching Student objects.
        """
        query = query.strip().lower()
        if not query:
            return self.get_all_students()

        result: List[Student] = []
        for student in self.__students:
            if (
                query in student.get_name().lower()
                or query in student.get_student_id().lower()
            ):
                result.append(student)
        return result

    def sort_students(self, by: str = "name", ascending: bool = True) -> None:
        """
        Sort the internal student list by a chosen field.

        Args:
            by: Field to sort by, 'name' or 'id'.
            ascending: Sort ascending (True) or descending (False).
        """
        reverse = not ascending

        if by == "id":
            self.__students.sort(
                key=lambda s: s.get_student_id().lower(), reverse=reverse
            )
        else:
            self.__students.sort(
                key=lambda s: s.get_name().lower(), reverse=reverse
            )

        self.save_to_file()

    # ---------------------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------------------
    def _find_student_by_id(self, student_id: str) -> Optional[Student]:
        """
        Private helper method to find a student by ID.

        Args:
            student_id: The ID to search for.

        Returns:
            Student object if found, None otherwise.
        """
        for student in self.__students:
            if student.get_student_id() == student_id:
                return student
        return None

    # ---------------------------------------------------------------------
    # FILE PERSISTENCE
    # ---------------------------------------------------------------------
    def save_to_file(self) -> None:
        """
        Save all students to a JSON file for persistence.
        """
        try:
            data = [student.to_dict() for student in self.__students]
            with open(self.__data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as exc:
            print(f"Error saving to file: {exc}")

    def load_from_file(self) -> None:
        """
        Load students from a JSON file, if it exists.
        """
        try:
            if os.path.exists(self.__data_file):
                with open(self.__data_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.__students = [Student.from_dict(item) for item in data]
        except Exception as exc:
            print(f"Error loading from file: {exc}")
            self.__students = []


# ============================================================================
# CLASS 3: THE GUI (StudentApp)
# ============================================================================
class StudentApp:
    """
    Main GUI application for the Student Management System.

    This class demonstrates:
    - SEPARATION OF CONCERNS: GUI is separate from business logic.
    - COMPOSITION: Uses a StudentManager instance for operations.
    - EVENT-DRIVEN PROGRAMMING: Responds to user interactions.
    - ADVANCED TKINTER: Styles, Treeview, column sorting, Toplevel edit.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the GUI application.

        Args:
            root: The main Tkinter root window.
        """
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("900x650")
        self.root.resizable(True, True)

        # State for search and sorting
        self._current_search_query: str = ""
        self._current_sort_field: str = "name"
        self._current_sort_ascending: bool = True

        # COMPOSITION: StudentApp "has-a" StudentManager
        self.manager = StudentManager()

        # Configure modern styles
        self._configure_styles()

        # Build the GUI
        self._create_widgets()

        # Load and display existing students
        self._refresh_student_list()

    # ------------------------------------------------------------------
    # STYLING
    # ------------------------------------------------------------------
    def _configure_styles(self) -> None:
        """
        Configure ttk styles to give the application a more modern appearance.
        """
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background="#f5f5fa")
        style.configure(
            "Header.TLabel",
            background="#f5f5fa",
            font=("Segoe UI", 18, "bold"),
            foreground="#333333",
        )
        style.configure("TLabel", background="#f5f5fa", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

        style.configure(
            "Custom.Treeview",
            font=("Segoe UI", 10),
            rowheight=24,
            background="#ffffff",
            fieldbackground="#ffffff",
        )
        style.configure(
            "Custom.Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            foreground="#ffffff",
            background="#4a6fa5",
        )
        style.map(
            "Custom.Treeview.Heading",
            background=[("active", "#3b5a84")],
        )
        style.configure(
            "Status.TLabel",
            background="#e2e4f0",
            font=("Segoe UI", 9),
            anchor="w",
        )

    # ------------------------------------------------------------------
    # WIDGETS
    # ------------------------------------------------------------------
    def _create_widgets(self) -> None:
        """
        Create and arrange all GUI widgets.
        """
        # HEADER
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)

        title_label = ttk.Label(
            header_frame,
            text="Student Management System",
            style="Header.TLabel",
        )
        title_label.pack(side=tk.LEFT)

        # INPUT SECTION
        input_frame = ttk.LabelFrame(
            self.root, text="Student Information", padding="15"
        )
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(input_frame, text="Name:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        self.name_entry = ttk.Entry(input_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text="Student ID (NIM):").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        self.id_entry = ttk.Entry(input_frame, width=40)
        self.id_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.EW)

        ttk.Label(input_frame, text="Major:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.major_entry = ttk.Entry(input_frame, width=40)
        self.major_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.EW)

        input_frame.columnconfigure(1, weight=1)

        # BUTTON SECTION
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X, padx=10)

        add_btn = ttk.Button(
            button_frame,
            text="Add Student",
            command=self._add_student,
            width=15,
        )
        add_btn.pack(side=tk.LEFT, padx=5)

        edit_btn = ttk.Button(
            button_frame,
            text="Edit Selected",
            command=self._open_edit_window,
            width=15,
        )
        edit_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self._delete_student,
            width=15,
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        clear_btn = ttk.Button(
            button_frame,
            text="Clear Fields",
            command=self._clear_fields,
            width=15,
        )
        clear_btn.pack(side=tk.LEFT, padx=5)

        # SEARCH SECTION
        search_frame = ttk.Frame(self.root, padding="0 0 10 0")
        search_frame.pack(fill=tk.X, padx=10)

        ttk.Label(search_frame, text="Search (Name / ID):").pack(
            side=tk.LEFT, padx=(0, 5)
        )
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", lambda event: self._perform_search())

        search_btn = ttk.Button(
            search_frame,
            text="Search",
            command=self._perform_search,
            width=12,
        )
        search_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = ttk.Button(
            search_frame,
            text="Reset",
            command=self._reset_search,
            width=12,
        )
        reset_btn.pack(side=tk.LEFT, padx=5)

        # TABLE SECTION
        table_frame = ttk.LabelFrame(self.root, text="Student List", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ("ID", "Name", "Student ID", "Major")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15,
            style="Custom.Treeview",
        )

        self.tree.heading("ID", text="#")
        self.tree.heading(
            "Name", text="Name", command=lambda: self._on_column_click("name")
        )
        self.tree.heading(
            "Student ID",
            text="Student ID (NIM)",
            command=lambda: self._on_column_click("id"),
        )
        self.tree.heading("Major", text="Major")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Name", width=200, anchor=tk.W)
        self.tree.column("Student ID", width=150, anchor=tk.CENTER)
        self.tree.column("Major", width=250, anchor=tk.W)

        scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Row striping
        self.tree.tag_configure("oddrow", background="#f7f8ff")
        self.tree.tag_configure("evenrow", background="#ffffff")

        # STATUS BAR
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            style="Status.TLabel",
        )
        self.status_label.pack(fill=tk.X, padx=10, pady=2)

    # ------------------------------------------------------------------
    # EVENT HANDLERS
    # ------------------------------------------------------------------
    def _add_student(self) -> None:
        """
        Handle the "Add Student" button click event.
        """
        name = self.name_entry.get()
        student_id = self.id_entry.get()
        major = self.major_entry.get()

        if not name or not student_id or not major:
            messagebox.showwarning(
                "Validation Error",
                "Please fill in all fields (Name, Student ID, and Major).",
            )
            return

        if self.manager.add_student(name, student_id, major):
            messagebox.showinfo(
                "Success", f"Student '{name}' has been added successfully!"
            )
            self._clear_fields()
            self._refresh_student_list()
        else:
            if self.manager._find_student_by_id(student_id):
                messagebox.showerror(
                    "Error",
                    f"Student ID '{student_id}' already exists. Please use a unique ID.",
                )
            else:
                messagebox.showerror(
                    "Error", "Failed to add student. Please check your input."
                )

    def _delete_student(self) -> None:
        """
        Handle the "Delete Selected" button click event.
        """
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning(
                "No Selection", "Please select a student to delete."
            )
            return

        item_values = self.tree.item(selected_item[0], "values")
        student_id = item_values[2]
        student_name = item_values[1]

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete student '{student_name}' (ID: {student_id})?",
        )

        if confirm:
            if self.manager.delete_student(student_id):
                messagebox.showinfo(
                    "Success", f"Student '{student_name}' has been deleted."
                )
                self._refresh_student_list()
            else:
                messagebox.showerror("Error", "Failed to delete student.")

    def _clear_fields(self) -> None:
        """
        Clear all input fields and refocus on the name entry.
        """
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)
        self.major_entry.delete(0, tk.END)
        self.name_entry.focus()

    def _perform_search(self) -> None:
        """
        Trigger a search based on the text in the search entry.
        """
        self._current_search_query = self.search_entry.get().strip()
        self._refresh_student_list()

    def _reset_search(self) -> None:
        """
        Clear the search query and show all students again.
        """
        self._current_search_query = ""
        self.search_entry.delete(0, tk.END)
        self._refresh_student_list()

    def _on_column_click(self, field: str) -> None:
        """
        Handle clicks on Treeview column headers to sort data.

        Args:
            field: 'name' or 'id', identifying the sort key.
        """
        if self._current_sort_field == field:
            self._current_sort_ascending = not self._current_sort_ascending
        else:
            self._current_sort_field = field
            self._current_sort_ascending = True

        self.manager.sort_students(
            by=self._current_sort_field, ascending=self._current_sort_ascending
        )
        self._refresh_student_list()

    def _open_edit_window(self) -> None:
        """
        Open a popup window (Toplevel) to edit the selected student's data.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(
                "No Selection", "Please select a student to edit first."
            )
            return

        item_values = self.tree.item(selected_item[0], "values")
        current_id = item_values[2]
        current_name = item_values[1]
        current_major = item_values[3]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Student")
        edit_window.transient(self.root)
        edit_window.grab_set()
        edit_window.resizable(False, False)

        ttk.Label(edit_window, text="Name:").grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=5
        )
        name_entry = ttk.Entry(edit_window, width=40)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        name_entry.insert(0, current_name)

        ttk.Label(edit_window, text="Student ID (NIM):").grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=5
        )
        id_entry = ttk.Entry(edit_window, width=40)
        id_entry.grid(row=1, column=1, padx=10, pady=5)
        id_entry.insert(0, current_id)

        ttk.Label(edit_window, text="Major:").grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=5
        )
        major_entry = ttk.Entry(edit_window, width=40)
        major_entry.grid(row=2, column=1, padx=10, pady=5)
        major_entry.insert(0, current_major)

        def save_changes() -> None:
            new_name = name_entry.get()
            new_id = id_entry.get()
            new_major = major_entry.get()

            if not new_name or not new_id or not new_major:
                messagebox.showwarning(
                    "Validation Error",
                    "Please fill in all fields (Name, Student ID, and Major).",
                    parent=edit_window,
                )
                return

            success = self.manager.update_student(
                original_student_id=current_id,
                new_name=new_name,
                new_student_id=new_id,
                new_major=new_major,
            )

            if success:
                messagebox.showinfo(
                    "Success",
                    f"Student '{new_name}' has been updated successfully.",
                    parent=edit_window,
                )
                edit_window.destroy()
                self._refresh_student_list()
            else:
                messagebox.showerror(
                    "Error",
                    "Failed to update student. The new ID may already exist or the data is invalid.",
                    parent=edit_window,
                )

        button_frame = ttk.Frame(edit_window, padding="10")
        button_frame.grid(row=3, column=0, columnspan=2, sticky=tk.E)

        save_btn = ttk.Button(button_frame, text="Save", command=save_changes, width=12)
        save_btn.pack(side=tk.RIGHT, padx=5)

        cancel_btn = ttk.Button(
            button_frame, text="Cancel", command=edit_window.destroy, width=12
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)

        self._center_window(edit_window, width=450, height=220)

    @staticmethod
    def _center_window(window: tk.Toplevel, width: int, height: int) -> None:
        """
        Utility method to center a Toplevel window on the screen.
        """
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x_coord = int((screen_width / 2) - (width / 2))
        y_coord = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x_coord}+{y_coord}")

    # ------------------------------------------------------------------
    # DATA BINDING / STATUS
    # ------------------------------------------------------------------
    def _refresh_student_list(self) -> None:
        """
        Refresh the Treeview table with current student data.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

        if self._current_search_query:
            students = self.manager.search_students(self._current_search_query)
        else:
            students = self.manager.get_all_students()

        for index, student in enumerate(students, start=1):
            tag = "evenrow" if index % 2 == 0 else "oddrow"
            self.tree.insert(
                "",
                tk.END,
                values=(
                    index,
                    student.get_name(),
                    student.get_student_id(),
                    student.get_major(),
                ),
                tags=(tag,),
            )

        self._update_status_bar(total=len(self.manager.get_all_students()))

    def _update_status_bar(self, total: int) -> None:
        """
        Update the status bar with total students information.
        """
        self.status_var.set(f"Total Students: {total}")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
def main() -> None:
    """
    Main function to start the application.
    """
    root = tk.Tk()
    StudentApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()