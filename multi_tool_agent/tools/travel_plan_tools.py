from typing import Dict, Any
from ..services import TravelPlanService

def evaluate_travel_plan(
    origin: str,
    destination: str,
    start_date: str,
    end_date: str,
    max_budget: float,
    adults: int = 1
) -> Dict[str, Any]:
    """
    Collect comprehensive travel data for AI evaluation.
    
    This tool gathers all relevant information about flights, hotels, and weather
    for the specified travel plan. The AI agent will use this data to provide
    personalized recommendations based on the specific context and user preferences.
    
    Args:
        origin: Origin airport IATA code (e.g., 'JFK')
        destination: Destination airport IATA code (e.g., 'LHR')
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        max_budget: Maximum budget for the trip in USD
        adults: Number of adult travelers (default: 1)
        
    Returns:
        Dictionary containing comprehensive travel data for AI evaluation:
        - Trip details (dates, duration, budget)
        - Weather forecast data
        - Available flights with prices and details
        - Available hotels with amenities and rates
    """
    try:
        travel_plan_service = TravelPlanService()
        travel_data = travel_plan_service.collect_travel_data(
            origin,
            destination,
            start_date,
            end_date,
            max_budget,
            adults
        )
        return travel_data
    except Exception as e:
        return {"error": str(e)} 