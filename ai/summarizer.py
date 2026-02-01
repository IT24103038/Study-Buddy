"""
Text Summarizer
Generates summaries from lesson text using AI
"""

from ai.ai_client import AIClient

class Summarizer:
    def __init__(self):
        """
        Initialize the summarizer
        """
        self.ai_client = AIClient()
    
    def summarize(self, text):
        """
        Generate a summary of the given text
        
        Args:
            text: Input text to summarize
            
        Returns:
            Summary text
        """
        # Check if text is empty
        if not text or text.strip() == "":
            return "No text provided"
        
        # Build prompt
        prompt = self.build_prompt(text)
        
        # Get AI response
        summary = self.ai_client.send_prompt(prompt)
        
        return summary
    
    def build_prompt(self, text):
        """
        Build the AI prompt for summarization
        
        Args:
            text: Text to summarize
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Summarize the following lesson for a student in simple language.
        Use bullet points.

        Lesson text:
        {text}

        Summary:"""
        
        return prompt
