"""
Utility Functions
Helper functions used across the application
"""

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
