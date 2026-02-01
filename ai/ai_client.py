"""
AI Client
Handles communication with Google Gemini AI API
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

class AIClient:
    def __init__(self):
        """
        Initialize AI client with Google Gemini
        Loads API key from .env file
        """
        # Load environment variables
        load_dotenv()
        
        # Get API key from environment
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        # Configure Gemini if API key exists
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Initialize Gemini model
            self.model = genai.GenerativeModel('gemini-3-flash-preview')
        else:
            self.model = None
    
    def set_api_key(self, api_key):
        """
        Set the API key for AI service
        
        Args:
            api_key: API key string
        """
        self.api_key = api_key
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    def send_prompt(self, prompt):
        """
        Send a prompt to the AI service
        
        Args:
            prompt: Text prompt to send
            
        Returns:
            AI response text
        """
        # Check if API key is set
        if not self.api_key or not self.model:
            return "Error: AI API key not configured. Please add your API key to the .env file."
        
        try:
            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            # Handle API errors gracefully
            error_message = str(e)
            if "API_KEY_INVALID" in error_message:
                return "Error: Invalid API key. Please check your Gemini API key in the .env file."
            elif "quota" in error_message.lower():
                return "Error: API quota exceeded. Please check your Gemini API usage limits."
            else:
                return f"Error connecting to AI service: {error_message}"
    
    def is_configured(self):
        """
        Check if AI client is properly configured
        
        Returns:
            True if configured, False otherwise
        """
        return self.api_key is not None and self.model is not None
