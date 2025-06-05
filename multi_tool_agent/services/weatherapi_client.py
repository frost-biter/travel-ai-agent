from typing import Dict, Any
from .base_client import BaseAPIClient

class WeatherAPIClient(BaseAPIClient):
    """Base client for Weather API interactions."""
    
    @property
    def base_url(self) -> str:
        return self.settings.weather_api_base_url
    
    def _make_request(self, method: str, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a request to the WeatherAPI."""
        if params is None:
            params = {}
        params["key"] = self.settings.weather_api_key
        
        return super()._make_request(method, endpoint, params=params)