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

def get_cheapest_flights(
    origin: str,
    destination: str,
    departure_date: Optional[str] = None,
    one_way: bool = False,
    duration: Optional[str] = None,
    non_stop: bool = False,
    max_price: Optional[int] = None,
    view_by: str = "DATE"
) -> Dict[str, Any]:
    """
    Search for cheapest flight dates between two cities.
    
    Args:
        origin: IATA code of origin city (e.g., 'MAD' for Madrid)
        destination: IATA code of destination city (e.g., 'MUC' for Munich)
        departure_date: Optional date or range in YYYY-MM-DD format.
                      For range, use comma (e.g., '2024-03-01,2024-03-31')
        one_way: If True, search one-way flights only (default: False)
        duration: For round trips, exact duration or range in days (e.g., '2,8')
        non_stop: If True, search non-stop flights only (default: False)
        max_price: Maximum price limit (positive integer)
        view_by: How to view results: 'DATE', 'DURATION', or 'WEEK'
                DATE: Best price per departure date
                DURATION: Best price per duration (round-trip)
                WEEK: Best price per week
        
    Returns:
        Dictionary containing cheapest flight dates or error message
    """
    logger.info(
        f"Tool: get_cheapest_flights called for {origin} to {destination}"
        f"{' (one-way)' if one_way else ' (round-trip)'}"
    )
    
    try:
        flight_service = FlightService()
        dates = flight_service.search_cheapest_flights(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            one_way=one_way,
            duration=duration,
            non_stop=non_stop,
            max_price=max_price,
            view_by=view_by
        )
        logger.info(f"Successfully retrieved {len(dates)} flight dates")
        return {"cheapest_dates": dates}
    except ValueError as e:
        error_msg = str(e)
        logger.error(f"Invalid parameters: {error_msg}")
        return {"error": error_msg}
    except Exception as e:
        error_msg = f"Failed to get cheapest flights: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"error": error_msg} 