from typing import Dict, Any, Optional, List
import logging
from ..services import FlightService

logger = logging.getLogger('travel_agent')

def get_flight_offers(origin: str, destination: str, date: str, adults: int = 1) -> Dict[str, Any]:
    """
    Search for flight offers between two cities for a specific date.
    
    Args:
        origin: Origin airport IATA code (e.g., 'JFK')
        destination: Destination airport IATA code (e.g., 'LHR')
        date: Departure date in YYYY-MM-DD format
        adults: Number of adult passengers (default: 1)
        
    Returns:
        Dictionary containing flight offers or error message
    """
    logger.info(f"Tool: get_flight_offers called for {origin} to {destination} on {date}")
    try:
        flight_service = FlightService()
        offers = flight_service.search_flights(origin, destination, date, adults)
        logger.info(f"Successfully retrieved {len(offers)} flight offers")
        return {"flight_offers": offers}
    except Exception as e:
        error_msg = f"Failed to get flight offers: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg} 