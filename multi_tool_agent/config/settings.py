import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Configuration settings for the travel agent."""
    
    def __init__(self):
        self.amadeus_api_key = os.getenv("AMADEUS_API_KEY")
        self.amadeus_secret_key = os.getenv("AMADEUS_SECRET_KEY")
        self.amadeus_base_url = "https://test.api.amadeus.com"
        
        # Validate required settings
        self._validate_settings()
    
    def _validate_settings(self):
        """Validate that all required settings are present."""
        if not self.amadeus_api_key:
            raise ValueError("AMADEUS_API_KEY environment variable is required")
        if not self.amadeus_secret_key:
            raise ValueError("AMADEUS_SECRET_KEY environment variable is required")

_settings = None

def get_settings():
    """Get the singleton settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings 