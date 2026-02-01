"""
Main Application Window
Handles the primary UI and navigation
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from ui.sidebar import Sidebar
from ui.summarizer_view import SummarizerView
from ui.question_view import QuestionView
from ui.lessons_view import LessonsView

class App:
    def __init__(self):
        """
        Initialize the main application window
        """
        # Create QApplication instance
        self.app = QApplication(sys.argv)
        
        # Create main window
        self.window = QMainWindow()
        self.window.setWindowTitle("Study Buddy")
        self.window.setGeometry(100, 100, 1000, 600)
        
        # Setup UI components
        self.setup_ui()
        
        # Apply stylesheet from external QSS if present, otherwise use built-in theme
        self._apply_external_stylesheet()
    
    def setup_ui(self):
        """
        Setup the main UI layout
        """
        # Create central widget
        central_widget = QWidget()
        self.window.setCentralWidget(central_widget)
        
        # Create horizontal layout
        layout = QHBoxLayout()
        central_widget.setLayout(layout)
        
        # Create sidebar
        self.sidebar = Sidebar(self.switch_view)
        layout.addWidget(self.sidebar)
        
        # Create main content container
        self.content_container = QWidget()
        self.content_layout = QHBoxLayout()
        self.content_container.setLayout(self.content_layout)
        layout.addWidget(self.content_container)
        
        # Set stretch factors (sidebar:content = 1:4)
        layout.setStretch(0, 1)
        layout.setStretch(1, 4)
        
        # Initialize with summarizer view
        self.current_view = None
        self.switch_view("summarizer")
    
    def switch_view(self, view_name):
        """
        Switch between different views
        
        Args:
            view_name: Name of the view to display
        """
        # Clear current view
        if self.current_view:
            self.content_layout.removeWidget(self.current_view)
            self.current_view.deleteLater()
            self.current_view = None
        
        # Load new view
        if view_name == "summarizer":
            self.current_view = SummarizerView()
        elif view_name == "questions":
            self.current_view = QuestionView()
        elif view_name == "lessons":
            self.current_view = LessonsView()
        else:
            # Default view - coming soon
            self.current_view = QWidget()
            layout = QHBoxLayout()
            label = QLabel(f"{view_name.title()} - Coming Soon!")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 20px;")
            layout.addWidget(label)
            self.current_view.setLayout(layout)
        
        self.content_layout.addWidget(self.current_view)
    
    # Note: embedded stylesheet removed. All styling should come from external QSS files.

    def _apply_external_stylesheet(self):
        """
        Load an external QSS stylesheet from `ui/style.qss` and apply it to the QApplication.
        If the file is not present or cannot be read, do nothing and let Qt use its default styling.
        """
        try:
            qss_path = Path(__file__).resolve().parent / "style.qss"
            if qss_path.exists():
                qss = qss_path.read_text(encoding="utf-8")
                self.app.setStyleSheet(qss)
        except Exception:
            # Ignore errors and leave default Qt styling in place
            pass
    
    def run(self):
        """
        Start the application main loop
        """
        self.window.show()
        sys.exit(self.app.exec())
