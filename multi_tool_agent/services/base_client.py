import requests
from typing import Dict, Any
from abc import ABC, abstractmethod
from ..config import get_settings

class BaseAPIClient(ABC):
    """Base class for all API clients."""
    
    def __init__(self):
        self.settings = get_settings()
    
    @property
    @abstractmethod
    def base_url(self) -> str:
        """Get the base URL for the API."""
        pass
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Dict[str, Any] = None,
        headers: Dict[str, str] = None,
        data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            headers: Request headers
            data: Request body data
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params or {},
                headers=headers or {},
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}") 