from typing import Dict, Any
from .base_client import BaseAPIClient

class AmadeusClient(BaseAPIClient):
    """Base client for Amadeus API interactions."""
    
    def __init__(self):
        super().__init__()
        self._access_token = None
    
    @property
    def base_url(self) -> str:
        return self.settings.amadeus_base_url
    
    def _get_access_token(self) -> str:
        """Get or refresh the Amadeus API access token."""
        if self._access_token:
            return self._access_token
            
        data = {
            "grant_type": "client_credentials",
            "client_id": self.settings.amadeus_api_key,
            "client_secret": self.settings.amadeus_secret_key
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = super()._make_request(
                method="POST",
                endpoint="/v1/security/oauth2/token",
                headers=headers,
                data=data
            )
            self._access_token = response["access_token"]
            return self._access_token
        except Exception as e:
            raise Exception(f"Failed to get Amadeus access token: {str(e)}")
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Dict[str, Any] = None,
        data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Make an authenticated request to the Amadeus API."""
        headers = {"Authorization": f"Bearer {self._get_access_token()}"}
        return super()._make_request(method, endpoint, params=params, headers=headers, data=data) 