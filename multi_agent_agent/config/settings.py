import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Configuration settings for the travel agent."""
    
    def __init__(self):
        # Amadeus settings
        self.amadeus_api_key = os.getenv("AMADEUS_API_KEY")
        self.amadeus_secret_key = os.getenv("AMADEUS_SECRET_KEY")
        self.amadeus_base_url = "https://test.api.amadeus.com"
        
        # Weather API settings
        self.weather_api_key = os.getenv("WEATHER_API_KEY")
        self.weather_api_base_url = "http://api.weatherapi.com/v1"
        
        # Validate required settings
        self._validate_settings()
    
    def _validate_settings(self):
        """Validate that all required settings are present."""
        required_settings = {
            "AMADEUS_API_KEY": self.amadeus_api_key,
            "AMADEUS_SECRET_KEY": self.amadeus_secret_key,
            "WEATHER_API_KEY": self.weather_api_key
        }
        
        missing_settings = [key for key, value in required_settings.items() if not value]
        if missing_settings:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_settings)}")

_settings = None

def get_settings():
    """Get the singleton settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings 