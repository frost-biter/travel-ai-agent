import requests
from typing import Dict, Any
from ..config import get_settings

class AmadeusClient:
    """Base client for Amadeus API interactions."""
    
    def __init__(self):
        self.settings = get_settings()
        self._access_token = None
    
    def _get_access_token(self) -> str:
        """Get or refresh the Amadeus API access token."""
        if self._access_token:
            return self._access_token
            
        url = f"{self.settings.amadeus_base_url}/v1/security/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.settings.amadeus_api_key,
            "client_secret": self.settings.amadeus_secret_key
        }

        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            self._access_token = response.json()["access_token"]
            return self._access_token
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get Amadeus access token: {str(e)}")
    
    def _make_request(self, method: str, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make an authenticated request to the Amadeus API."""
        url = f"{self.settings.amadeus_base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self._get_access_token()}"}
        
        try:
            response = requests.request(method, url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Amadeus API request failed: {str(e)}") 