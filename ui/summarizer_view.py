"""
Lesson Summarizer View
Interface for summarizing lessons
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from ai.summarizer import Summarizer
from utils.helpers import open_pdf_dialog
from data.database import Database
from ui.save_lesson_dialog import SaveLessonDialog

class SummarizerView(QWidget):
    def __init__(self):
        """
        Initialize the summarizer view
        """
        super().__init__()
        
        self.summarizer = Summarizer()
        self.db = Database()
        
        # Setup UI
        self.setup_ui()
        
        # Load lessons for selector
        self.load_lessons_selector()
    
    def setup_ui(self):
        """
        Create the summarizer interface
        """
        # Create vertical layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("Lesson Summarizer")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; padding: 20px;")
        layout.addWidget(title)
        
        # Lesson selector row
        selector_layout = QHBoxLayout()
        
        selector_label = QLabel("Load Saved Lesson:")
        selector_layout.addWidget(selector_label)
        
        self.lesson_selector = QComboBox()
        self.lesson_selector.addItem("-- Select a lesson --")
        self.lesson_selector.currentIndexChanged.connect(self.load_selected_lesson)
        selector_layout.addWidget(self.lesson_selector)
        
        layout.addLayout(selector_layout)
        
        # Input label
        input_label = QLabel("Paste your lesson text below:")
        input_label.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(input_label)
        
        # Text input area
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter your lesson text here...")
        self.text_input.setMinimumHeight(200)
        layout.addWidget(self.text_input)
        
        # Button row (Upload PDF + Save Lesson + Summarize)
        button_layout = QHBoxLayout()
        
        # Upload PDF button
        upload_button = QPushButton("Upload PDF")
        upload_button.clicked.connect(self.upload_pdf)
        upload_button.setMinimumHeight(40)
        button_layout.addWidget(upload_button)
        
        # Save Lesson button
        save_button = QPushButton("Save Lesson")
        save_button.clicked.connect(self.save_lesson)
        save_button.setMinimumHeight(40)
        button_layout.addWidget(save_button)
        
        # Summarize button
        summarize_button = QPushButton("Summarize")
        summarize_button.clicked.connect(self.summarize_text)
        summarize_button.setMinimumHeight(40)
        button_layout.addWidget(summarize_button)
        
        layout.addLayout(button_layout)
        
        # Output label
        output_label = QLabel("Summary:")
        output_label.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(output_label)
        
        # Summary output area
        self.summary_output = QTextEdit()
        self.summary_output.setReadOnly(True)
        self.summary_output.setMinimumHeight(200)
        layout.addWidget(self.summary_output)
    
    def load_lessons_selector(self):
        """
        Load all lessons into the selector dropdown
        """
        # Clear current items
        self.lesson_selector.clear()
        self.lesson_selector.addItem("-- Select a lesson --", None)
        
        # Get all lessons from database
        lessons = self.db.get_all_lessons()
        
        # Add lessons to selector
        for lesson in lessons:
            display_text = f"{lesson['title']} - {lesson['module']} ({lesson['academic_year']})"
            self.lesson_selector.addItem(display_text, lesson['id'])
    
    def load_selected_lesson(self):
        """
        Load the selected lesson into the text input
        """
        # Get selected lesson ID
        lesson_id = self.lesson_selector.currentData()
        
        if not lesson_id:
            return
        
        # Get lesson from database
        lesson = self.db.get_lesson_by_id(lesson_id)
        
        if lesson:
            # Load lesson content into text input
            self.text_input.setPlainText(lesson['content'])
    
    def save_lesson(self):
        """
        Save the current text as a new lesson
        """
        # Get current text
        text = self.text_input.toPlainText()
        
        if not text or text.strip() == "":
            QMessageBox.warning(self, "No Content", "Please enter some text before saving.")
            return
        
        # Open save dialog
        dialog = SaveLessonDialog(self)
        
        if dialog.exec():
            # Get lesson data from dialog
            lesson_data = dialog.get_lesson_data()
            
            if lesson_data:
                # Save to database
                self.db.save_lesson(
                    title=lesson_data['title'],
                    content=text,
                    academic_year=lesson_data['academic_year'],
                    semester=lesson_data['semester'],
                    module=lesson_data['module']
                )
                
                # Reload lessons selector
                self.load_lessons_selector()
                
                # Show success message
                QMessageBox.information(self, "Success", "Lesson saved successfully!")
    
    def summarize_text(self):
        """
        Get text from input and generate summary
        """
        # Get input text
        text = self.text_input.toPlainText()
        
        # Check if text is empty
        if not text or text.strip() == "":
            self.summary_output.setPlainText("Please enter some text to summarize.")
            return
        
        # Show loading message
        self.summary_output.setPlainText("Generating summary...")
        
        # Generate summary
        summary = self.summarizer.summarize(text)
        
        # Display summary
        self.summary_output.setPlainText(summary)
    
    def upload_pdf(self):
        """
        Open file dialog to select and upload a PDF file
        Extract text and insert into input area
        """
        # Use shared PDF dialog function
        extracted_text = open_pdf_dialog(self)
        
        # Check if file was selected and text extracted
        if not extracted_text:
            return
        
        # Get existing text in input area
        existing_text = self.text_input.toPlainText()
        
        # Combine existing text with extracted text
        if existing_text and existing_text.strip():
            combined_text = existing_text + "\n\n" + extracted_text
        else:
            combined_text = extracted_text
        
        # Insert combined text into input area
        self.text_input.setPlainText(combined_text)
