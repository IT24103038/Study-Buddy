"""
Sidebar Navigation
Handles navigation between different features
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

class Sidebar(QWidget):
    def __init__(self, switch_view_callback):
        """
        Initialize the sidebar
        
        Args:
            switch_view_callback: Function to call when switching views
        """
        super().__init__()
        
        self.switch_view = switch_view_callback
        
        # Setup sidebar components
        self.setup_sidebar()
    
    def setup_sidebar(self):
        """
        Create sidebar buttons and layout
        """
        # Create vertical layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # App title
        title = QLabel("Study Buddy")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 20px;")
        layout.addWidget(title)
        
        # Navigation buttons
        self.create_nav_button(layout, "Lessons", "lessons")
        self.create_nav_button(layout, "Summarizer", "summarizer")
        self.create_nav_button(layout, "Questions", "questions")
        self.create_nav_button(layout, "Schedule", "schedule")
        self.create_nav_button(layout, "Notes", "notes")
        self.create_nav_button(layout, "Flashcards", "flashcards")
        self.create_nav_button(layout, "Progress", "progress")
        
        # Add stretch to push buttons to top
        layout.addStretch()
        
        # Set fixed width for sidebar
        self.setFixedWidth(200)
    
    def create_nav_button(self, layout, text, view_name):
        """
        Create a navigation button
        
        Args:
            layout: Layout to add button to
            text: Button label
            view_name: Name of view to switch to
        """
        button = QPushButton(text)
        button.clicked.connect(lambda: self.switch_view(view_name))
        button.setMinimumHeight(40)
        layout.addWidget(button)
