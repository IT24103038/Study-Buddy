"""
Question Generator View
Interface for generating practice questions
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import Qt
from ai.question_generator import QuestionGenerator

class QuestionView(QWidget):
    def __init__(self):
        """
        Initialize the question generator view
        """
        super().__init__()
        
        self.question_generator = QuestionGenerator()
        
        # Setup UI
        self.setup_ui()
    
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
        
        # Input label
        input_label = QLabel("Paste your lesson text below:")
        input_label.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(input_label)
        
        # Text input area
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter your lesson text here...")
        self.text_input.setMinimumHeight(200)
        layout.addWidget(self.text_input)
        
        # Generate button
        generate_button = QPushButton("Generate Questions")
        generate_button.clicked.connect(self.generate_questions)
        generate_button.setMinimumHeight(40)
        layout.addWidget(generate_button)
        
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
