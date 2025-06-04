from typing import Dict, Any
from ..services import FlightService

def get_flight_offers(origin: str, destination: str, date: str, adults: int = 1) -> Dict[str, Any]:
    """
    Search for flight offers between two cities.
    
    Args:
        origin: Origin airport IATA code (e.g., 'JFK')
        destination: Destination airport IATA code (e.g., 'LHR')
        date: Departure date in YYYY-MM-DD format
        adults: Number of adult passengers (default: 1)
        
    Returns:
        Dictionary containing flight offers or error message
    """
    try:
        flight_service = FlightService()
        offers = flight_service.search_flights(origin, destination, date, adults)
        return {"flight_offers": offers}
    except Exception as e:
        return {"error": str(e)} 