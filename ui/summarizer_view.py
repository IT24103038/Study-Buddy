"""
Lesson Summarizer View
Interface for summarizing lessons
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt6.QtCore import Qt
from ai.summarizer import Summarizer

class SummarizerView(QWidget):
    def __init__(self):
        """
        Initialize the summarizer view
        """
        super().__init__()
        
        self.summarizer = Summarizer()
        
        # Setup UI
        self.setup_ui()
    
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
        
        # Input label
        input_label = QLabel("Paste your lesson text below:")
        input_label.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(input_label)
        
        # Text input area
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter your lesson text here...")
        self.text_input.setMinimumHeight(200)
        layout.addWidget(self.text_input)
        
        # Summarize button
        summarize_button = QPushButton("Summarize")
        summarize_button.clicked.connect(self.summarize_text)
        summarize_button.setMinimumHeight(40)
        layout.addWidget(summarize_button)
        
        # Output label
        output_label = QLabel("Summary:")
        output_label.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(output_label)
        
        # Summary output area
        self.summary_output = QTextEdit()
        self.summary_output.setReadOnly(True)
        self.summary_output.setMinimumHeight(200)
        layout.addWidget(self.summary_output)
    
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
