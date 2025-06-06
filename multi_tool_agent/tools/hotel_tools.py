from typing import Dict, List, Any, Optional
import logging
from ..services.hotel_service import HotelService, RadiusUnit, HotelSource, HotelAmenities

logger = logging.getLogger('travel_agent')

def get_hotel_offers(
    city_code: str,
    radius: int = 50,
    radius_unit: str = "KM",
    chain_codes: Optional[List[str]] = None,
    amenities: Optional[List[str]] = None,
    ratings: Optional[List[str]] = None,
    hotel_source: str = "ALL"
) -> Dict[str, Any]:
    """
    Search for hotels in a specific city.
    
    Args:
        city_code: IATA city or airport code (e.g., 'PAR' for Paris)
        radius: Maximum distance from city center (default: 50)
        radius_unit: Unit for radius - 'KM' or 'MILE' (default: KM)
        chain_codes: Optional list of 2-letter hotel chain codes
        amenities: Optional list of amenities (e.g., SWIMMING_POOL, SPA, WIFI)
        ratings: Optional list of hotel star ratings (1-5)
        hotel_source: Source of hotel data - 'BEDBANK', 'DIRECTCHAIN', or 'ALL' (default: ALL)
        
    Returns:
        Dictionary containing hotels or error message
    """
    logger.info(f"Tool: get_hotel_offers called for {city_code}")
    
    try:
        hotel_service = HotelService()
        
        # Convert string parameters to enums
        try:
            radius_unit_enum = RadiusUnit[radius_unit.upper()]
            hotel_source_enum = HotelSource[hotel_source.upper()]
        except KeyError as e:
            logger.error(f"Invalid enum value: {str(e)}")
            return {"error": f"Invalid value: {str(e)}"}
        
        # Search for hotels
        hotels = hotel_service.search_hotels(
            city_code=city_code,
            radius=radius,
            radius_unit=radius_unit_enum,
            chain_codes=chain_codes,
            amenities=amenities,
            ratings=ratings,
            hotel_source=hotel_source_enum
        )
        
        logger.info(f"Successfully retrieved {len(hotels)} hotels")
        return {"hotels": hotels}
        
    except Exception as e:
        error_msg = f"Failed to get hotels: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg} 