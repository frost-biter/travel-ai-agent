from typing import Dict, Any
from ..services import HotelService

def get_hotel_offers(city_code: str, check_in: str, check_out: str, adults: int = 1) -> Dict[str, Any]:
    """
    Search for hotel offers in a city.
    
    Args:
        city_code: City IATA code (e.g., 'LON')
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format
        adults: Number of adult guests (default: 1)
        
    Returns:
        Dictionary containing hotel offers or error message
    """
    try:
        hotel_service = HotelService()
        offers = hotel_service.search_hotels(city_code, check_in, check_out, adults)
        return {"hotel_offers": offers}
    except Exception as e:
        return {"error": str(e)} 