"""
Question Generator View
Interface for generating practice questions
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
                              QPushButton, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from ai.question_generator import QuestionGenerator
from utils.helpers import open_pdf_dialog
from data.database import Database
from ui.save_lesson_dialog import SaveLessonDialog

class QuestionView(QWidget):
    def __init__(self):
        """
        Initialize the question generator view
        """
        super().__init__()
        
        self.question_generator = QuestionGenerator()
        self.db = Database()
        
        # Setup UI
        self.setup_ui()
        
        # Load lessons for selector
        self.load_lessons_selector()
    
    def setup_ui(self):
        """
        Create the question generator interface
        """
        # Create vertical layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("Question Generator")
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
        
        # Button row (Upload PDF + Save Lesson + Generate Questions)
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
        
        # Generate button
        generate_button = QPushButton("Generate Questions")
        generate_button.clicked.connect(self.generate_questions)
        generate_button.setMinimumHeight(40)
        button_layout.addWidget(generate_button)
        
        layout.addLayout(button_layout)
        
        # Output label
        output_label = QLabel("Generated Questions:")
        output_label.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(output_label)
        
        # Questions output area
        self.questions_output = QTextEdit()
        self.questions_output.setReadOnly(True)
        self.questions_output.setMinimumHeight(200)
        layout.addWidget(self.questions_output)
    
    def generate_questions(self):
        """
        Get text from input and generate questions
        """
        # Get input text
        text = self.text_input.toPlainText()
        
        # Check if text is empty
        if not text or text.strip() == "":
            self.questions_output.setPlainText("Please enter some text to generate questions from.")
            return
        
        # Show loading message
        self.questions_output.setPlainText("Generating questions...")
        
        # Generate questions
        questions = self.question_generator.generate(text)
        
        # Display questions
        self.questions_output.setPlainText(questions)
    
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
    
    def load_lessons_selector(self):
        """
        Populate the lesson selector dropdown with saved lessons
        """
        # Clear existing items (except placeholder)
        self.lesson_selector.clear()
        self.lesson_selector.addItem("-- Select a lesson --")
        
        # Get all lessons from database
        lessons = self.db.get_all_lessons()
        
        # Add lessons to dropdown
        for lesson in lessons:
            # Format display: "Title (Year - Semester - Module)"
            display_text = f"{lesson['title']} ({lesson['academic_year']} - {lesson['semester']} - {lesson['module']})"
            self.lesson_selector.addItem(display_text, lesson['id'])
    
    def load_selected_lesson(self):
        """
        Load the selected lesson content into the text input area
        """
        # Get selected lesson ID
        lesson_id = self.lesson_selector.currentData()
        
        # If no valid lesson selected (e.g., placeholder), do nothing
        if not lesson_id:
            return
        
        # Get lesson from database
        lesson = self.db.get_lesson_by_id(lesson_id)
        
        if lesson:
            # Load content into text input
            self.text_input.setPlainText(lesson['content'])
    
    def save_lesson(self):
        """
        Open dialog to save the current lesson to the database
        """
        # Get current text
        text = self.text_input.toPlainText()
        
        # Validate text exists
        if not text or not text.strip():
            QMessageBox.warning(self, "No Content", "Please enter some lesson text before saving.")
            return
        
        # Open save dialog
        dialog = SaveLessonDialog(self)
        
        if dialog.exec():
            # Get lesson data from dialog
            lesson_data = dialog.get_lesson_data()
            
            # Add content to lesson data
            lesson_data['content'] = text
            
            # Save to database
            lesson_id = self.db.save_lesson(
                lesson_data['title'],
                lesson_data['content'],
                lesson_data['academic_year'],
                lesson_data['semester'],
                lesson_data['module']
            )
            
            if lesson_id:
                QMessageBox.information(self, "Success", "Lesson saved successfully!")
                
                # Refresh lesson selector
                self.load_lessons_selector()
            else:
                QMessageBox.critical(self, "Error", "Failed to save lesson.")
