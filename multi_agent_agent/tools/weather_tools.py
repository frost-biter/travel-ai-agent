from typing import Dict, Any, Optional
from ..services import WeatherService

def get_weather(location: str, date: Optional[str] = None, days: int = 7) -> Dict[str, Any]:
    """
    Get detailed weather data for a location.
    
    This tool provides comprehensive weather data that the AI agent will use
    to evaluate travel plans. The AI will consider factors like temperature trends,
    precipitation chances, and daylight hours to make context-aware recommendations.
    
    Args:
        location: City name, lat/lon, or zip code (e.g., 'London', '51.5,-0.1', '90210')
        date: Optional specific date in YYYY-MM-DD format. If provided, returns weather for that date.
              If not provided, returns forecast for next 'days' days.
        days: Number of forecast days (1-14) when date is not provided
        
    Returns:
        Dictionary containing weather information including:
        - Location details (name, region, country, coordinates)
        - Current conditions (temperature, weather, humidity, etc.)
        - Daily forecasts (temperature, precipitation chances, conditions)
        - Astronomical data (sunrise, sunset, moon phase)
    """
    try:
        weather_service = WeatherService()
        return weather_service.get_weather(location, date, days)
    except Exception as e:
        return {"error": str(e)} 