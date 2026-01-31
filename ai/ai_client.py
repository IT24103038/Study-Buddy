"""
AI Client
Handles communication with AI API
"""

class AIClient:
    def __init__(self):
        """
        Initialize AI client
        Note: API key should be configured before use
        """
        self.api_key = None
        self.api_url = None
    
    def set_api_key(self, api_key):
        """
        Set the API key for AI service
        
        Args:
            api_key: API key string
        """
        self.api_key = api_key
    
    def send_prompt(self, prompt):
        """
        Send a prompt to the AI service
        
        Args:
            prompt: Text prompt to send
            
        Returns:
            AI response text
        """
        # Check if API key is set
        if not self.api_key:
            return "Error: AI API key not configured. Please set up your API key first."
        
        # TODO: Implement actual API call
        # This is a placeholder that should be replaced with actual API integration
        return "AI integration coming soon. Please configure your AI service."
    
    def is_configured(self):
        """
        Check if AI client is properly configured
        
        Returns:
            True if configured, False otherwise
        """
        return self.api_key is not None
