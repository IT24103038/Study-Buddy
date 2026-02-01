"""
Question Generator
Creates practice questions from lesson text using AI
"""

from ai.ai_client import AIClient

class QuestionGenerator:
    def __init__(self):
        """
        Initialize the question generator
        """
        self.ai_client = AIClient()
    
    def generate(self, text):
        """
        Generate practice questions from the given text
        
        Args:
            text: Input text to generate questions from
            
        Returns:
            Generated questions text
        """
        # Check if text is empty
        if not text or text.strip() == "":
            return "No text provided"
        
        # Build prompt
        prompt = self.build_prompt(text)
        
        # Get AI response
        questions = self.ai_client.send_prompt(prompt)
        
        return questions
    
    def build_prompt(self, text):
        """
        Build the AI prompt for question generation
        
        Args:
            text: Text to generate questions from
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""Generate 5 practice questions based on the following lesson text.
        Make them suitable for university students.
        Make sure to only use information from the lesson text.
        Include a mix of question types (multiple choice, short answer, etc.).

        Lesson text:
        {text}

        Questions:"""
        
        return prompt
