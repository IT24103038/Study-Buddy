"""
Utility Functions
Helper functions used across the application
"""

from pypdf import PdfReader
from PyQt6.QtWidgets import QFileDialog

def validate_text_input(text):
    """
    Validate text input is not empty
    
    Args:
        text: Input text to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not text or text.strip() == "":
        return False
    return True

def truncate_text(text, max_length=100):
    """
    Truncate text to a maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def format_response(response):
    """
    Format AI response for display
    
    Args:
        response: Raw response text
        
    Returns:
        Formatted response
    """
    # Remove extra whitespace
    response = response.strip()
    return response

def extract_text_from_pdf(file_path):
    """
    Extract text content from a PDF file
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text as a string, or error message if extraction fails
    """
    try:
        # Open and read the PDF
        reader = PdfReader(file_path)
        
        # Extract text from all pages
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # Check if any text was extracted
        if not text or text.strip() == "":
            return "No text could be extracted from this PDF. The file may be image-based or empty."
        
        return text.strip()
    
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"

def open_pdf_dialog(parent_widget):
    """
    Open a file dialog to select a PDF and extract its text
    Shared function for all views that need PDF upload functionality
    
    Args:
        parent_widget: The parent widget (for dialog positioning)
        
    Returns:
        Extracted text from the PDF, or None if no file was selected
    """
    # Open file dialog
    file_path, _ = QFileDialog.getOpenFileName(
        parent_widget,
        "Select PDF File",
        "",
        "PDF Files (*.pdf)"
    )
    
    # Check if file was selected
    if not file_path:
        return None
    
    # Extract and return text from PDF
    return extract_text_from_pdf(file_path)
