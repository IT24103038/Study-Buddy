"""
Lessons Library View
Interface for managing saved lessons
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QListWidget, QListWidgetItem,
                              QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from data.database import Database

class LessonsView(QWidget):
    def __init__(self):
        """
        Initialize the lessons library view
        """
        super().__init__()
        
        self.db = Database()
        
        # Setup UI
        self.setup_ui()
        
        # Load lessons
        self.load_lessons()
    
    def setup_ui(self):
        """
        Create the lessons library interface
        """
        # Create vertical layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("Lessons Library")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px;")
        layout.addWidget(title)
        
        # Filter section
        filter_layout = QHBoxLayout()
        
        filter_label = QLabel("Filter by:")
        filter_layout.addWidget(filter_label)
        
        # Academic Year filter
        self.year_filter = QComboBox()
        self.year_filter.addItem("All Years")
        self.year_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.year_filter)
        
        # Semester filter
        self.semester_filter = QComboBox()
        self.semester_filter.addItem("All Semesters")
        self.semester_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.semester_filter)
        
        # Module filter
        self.module_filter = QComboBox()
        self.module_filter.addItem("All Modules")
        self.module_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.module_filter)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Lessons list
        self.lessons_list = QListWidget()
        self.lessons_list.setMinimumHeight(400)
        layout.addWidget(self.lessons_list)
        
        # Button row
        button_layout = QHBoxLayout()
        
        # Delete button
        delete_button = QPushButton("Delete Selected Lesson")
        delete_button.clicked.connect(self.delete_lesson)
        delete_button.setMinimumHeight(40)
        button_layout.addWidget(delete_button)
        
        # Refresh button
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.load_lessons)
        refresh_button.setMinimumHeight(40)
        button_layout.addWidget(refresh_button)
        
        layout.addLayout(button_layout)
    
    def load_lessons(self):
        """
        Load all lessons from database and populate list
        """
        # Clear current list
        self.lessons_list.clear()
        
        # Load filter options
        self.load_filter_options()
        
        # Get all lessons
        lessons = self.db.get_all_lessons()
        
        # Populate list
        for lesson in lessons:
            item_text = f"{lesson['title']} - {lesson['module']} ({lesson['academic_year']}, {lesson['semester']})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, lesson['id'])
            self.lessons_list.addItem(item)
    
    def load_filter_options(self):
        """
        Load unique years, semesters, and modules for filters
        """
        # Save current selections
        current_year = self.year_filter.currentText()
        current_semester = self.semester_filter.currentText()
        current_module = self.module_filter.currentText()
        
        # Clear filters
        self.year_filter.clear()
        self.semester_filter.clear()
        self.module_filter.clear()
        
        # Add "All" options
        self.year_filter.addItem("All Years")
        self.semester_filter.addItem("All Semesters")
        self.module_filter.addItem("All Modules")
        
        # Load unique values from database
        years = self.db.get_unique_years()
        semesters = self.db.get_unique_semesters()
        modules = self.db.get_unique_modules()
        
        # Populate filters
        self.year_filter.addItems(years)
        self.semester_filter.addItems(semesters)
        self.module_filter.addItems(modules)
        
        # Restore selections if they still exist
        year_index = self.year_filter.findText(current_year)
        if year_index >= 0:
            self.year_filter.setCurrentIndex(year_index)
        
        semester_index = self.semester_filter.findText(current_semester)
        if semester_index >= 0:
            self.semester_filter.setCurrentIndex(semester_index)
        
        module_index = self.module_filter.findText(current_module)
        if module_index >= 0:
            self.module_filter.setCurrentIndex(module_index)
    
    def apply_filters(self):
        """
        Apply selected filters to lessons list
        """
        # Get filter values
        year = self.year_filter.currentText()
        semester = self.semester_filter.currentText()
        module = self.module_filter.currentText()
        
        # Convert "All" to None
        year = None if year == "All Years" else year
        semester = None if semester == "All Semesters" else semester
        module = None if module == "All Modules" else module
        
        # Get filtered lessons
        lessons = self.db.get_lessons_by_filters(year, semester, module)
        
        # Clear and populate list
        self.lessons_list.clear()
        for lesson in lessons:
            item_text = f"{lesson['title']} - {lesson['module']} ({lesson['academic_year']}, {lesson['semester']})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, lesson['id'])
            self.lessons_list.addItem(item)
    
    def delete_lesson(self):
        """
        Delete the selected lesson
        """
        # Get selected item
        current_item = self.lessons_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a lesson to delete.")
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this lesson?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Get lesson ID and delete
            lesson_id = current_item.data(Qt.ItemDataRole.UserRole)
            self.db.delete_lesson(lesson_id)
            
            # Reload lessons
            self.load_lessons()
            
            QMessageBox.information(self, "Success", "Lesson deleted successfully!")
