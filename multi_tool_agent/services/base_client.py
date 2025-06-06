import requests
import logging
from typing import Dict, Any
from abc import ABC, abstractmethod
from ..config import get_settings

logger = logging.getLogger('travel_agent')

class BaseAPIClient(ABC):
    """Base class for all API clients."""
    
    def __init__(self):
        self.settings = get_settings()
        self._service_name = self.__class__.__name__
        logger.debug(f"Initialized {self._service_name}")
    
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
        data: Dict[str, Any] = None,
        is_form_data: bool = False
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            headers: Request headers
            data: Request body data
            is_form_data: Whether to send data as form-encoded (default: False)
            
        Returns:
            API response as dictionary
        """
        url = f"{self.base_url}{endpoint}"
        
        # Log request details
        logger.debug(
            f"{self._service_name} Request - Method: {method}, Endpoint: {endpoint}"
            f"\nParams: {params}"
            f"\nHeaders: {headers}"
            f"\nData: {data}"
            f"\nForm Data: {is_form_data}"
        )
        
        try:
            kwargs = {
                "params": params or {},
                "headers": headers or {}
            }
            
            if data:
                if is_form_data:
                    kwargs["data"] = data
                else:
                    kwargs["json"] = data
            
            response = requests.request(method=method, url=url, **kwargs)
            
            # Log response status
            logger.debug(
                f"{self._service_name} Response - Status: {response.status_code}"
                f"\nURL: {response.url}"
            )
            
            # Log error details if any
            if not response.ok:
                logger.error(
                    f"{self._service_name} Error - Status: {response.status_code}"
                    f"\nResponse: {response.text}"
                )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            error_msg = f"{self._service_name} API request failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise Exception(error_msg) 