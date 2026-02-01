"""
Save Lesson Dialog
Dialog for saving a lesson with categorization
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt

class SaveLessonDialog(QDialog):
    def __init__(self, parent=None):
        """
        Initialize the save lesson dialog
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.setWindowTitle("Save Lesson")
        self.setMinimumWidth(400)
        
        # Store result
        self.lesson_data = None
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """
        Create the dialog interface
        """
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title field
        title_label = QLabel("Lesson Title:")
        layout.addWidget(title_label)
        
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("e.g., Introduction to Databases")
        layout.addWidget(self.title_input)
        
        # Academic Year field
        year_label = QLabel("Academic Year:")
        layout.addWidget(year_label)
        
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("e.g., 2025/2026")
        layout.addWidget(self.year_input)
        
        # Semester field
        semester_label = QLabel("Semester:")
        layout.addWidget(semester_label)
        
        self.semester_input = QLineEdit()
        self.semester_input.setPlaceholderText("e.g., Semester 1")
        layout.addWidget(self.semester_input)
        
        # Module field
        module_label = QLabel("Module/Subject:")
        layout.addWidget(module_label)
        
        self.module_input = QLineEdit()
        self.module_input.setPlaceholderText("e.g., Database Systems")
        layout.addWidget(self.module_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_lesson)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def save_lesson(self):
        """
        Validate and save lesson data
        """
        # Get input values
        title = self.title_input.text().strip()
        year = self.year_input.text().strip()
        semester = self.semester_input.text().strip()
        module = self.module_input.text().strip()
        
        # Validate inputs
        if not title:
            QMessageBox.warning(self, "Missing Information", "Please enter a lesson title.")
            return
        
        if not year:
            QMessageBox.warning(self, "Missing Information", "Please enter an academic year.")
            return
        
        if not semester:
            QMessageBox.warning(self, "Missing Information", "Please enter a semester.")
            return
        
        if not module:
            QMessageBox.warning(self, "Missing Information", "Please enter a module/subject.")
            return
        
        # Store data
        self.lesson_data = {
            'title': title,
            'academic_year': year,
            'semester': semester,
            'module': module
        }
        
        # Close dialog with success
        self.accept()
    
    def get_lesson_data(self):
        """
        Get the entered lesson data
        
        Returns:
            Dictionary with lesson information or None if cancelled
        """
        return self.lesson_data
