from typing import Dict, Any
from ..services import WeatherService

def get_weather_forecast(location: str, days: int = 7) -> Dict[str, Any]:
    """
    Get detailed weather forecast data for a location.
    
    This tool provides comprehensive weather data that the AI agent will use
    to evaluate travel plans. The AI will consider factors like temperature trends,
    precipitation chances, and daylight hours to make context-aware recommendations.
    
    Args:
        location: City name, lat/lon, or zip code (e.g., 'London', '51.5,-0.1', '90210')
        days: Number of forecast days (1-14)
        
    Returns:
        Dictionary containing weather forecast information including:
        - Location details (name, region, country, coordinates)
        - Current conditions (temperature, weather, humidity, etc.)
        - Daily forecasts (temperature, precipitation chances, conditions)
        - Astronomical data (sunrise, sunset, moon phase)
    """
    try:
        weather_service = WeatherService()
        return weather_service.get_forecast(location, days)
    except Exception as e:
        return {"error": str(e)}

def get_future_weather(location: str, future_date: str) -> Dict[str, Any]:
    """
    Get detailed weather prediction for a specific future date.
    
    This tool is useful for checking weather conditions on specific dates
    beyond the standard forecast period. The AI will use this data to
    evaluate travel plans for future dates.
    
    Args:
        location: City name, lat/lon, or zip code
        future_date: Future date in YYYY-MM-DD format
        
    Returns:
        Dictionary containing weather prediction including:
        - Location details
        - Temperature range (max/min)
        - Weather conditions
        - Astronomical data
    """
    try:
        weather_service = WeatherService()
        return weather_service.get_future_weather(location, future_date)
    except Exception as e:
        return {"error": str(e)}

def get_weather_analysis(location: str, days: int = 7) -> Dict[str, Any]:
    """
    Get comprehensive weather data for AI analysis.
    
    This tool collects detailed weather information that the AI agent will use
    to evaluate travel plans. The AI will consider factors like temperature trends,
    precipitation chances, and daylight hours to make context-aware recommendations.
    
    Args:
        location: City name, lat/lon, or zip code
        days: Number of days to analyze (1-14)
        
    Returns:
        Raw weather API response containing:
        - Location information
        - Current conditions
        - Daily forecasts with weather details
        - Astronomical data
    """
    try:
        weather_service = WeatherService()
        return weather_service.get_weather_data(location, days)
    except Exception as e:
        return {"error": str(e)}

def get_travel_weather_recommendation(location: str, days: int = 7) -> Dict[str, Any]:
    """
    Get travel recommendations based on weather forecast.
    
    Args:
        location: City name, lat/lon, or zip code
        days: Number of days to analyze (1-14)
        
    Returns:
        Dictionary containing travel recommendations with best and worst days
    """
    try:
        weather_service = WeatherService()
        recommendations = weather_service.get_travel_recommendation(location, days)
        
        # Create a user-friendly response
        response = {
            "location": recommendations["location"],
            "summary": _create_recommendation_summary(recommendations)
        }
        
        if recommendations["best_days"]:
            response["best_days"] = recommendations["best_days"]
        
        if recommendations["poor_days"]:
            response["poor_days"] = recommendations["poor_days"]
            
        return response
    except Exception as e:
        return {"error": str(e)}

def _create_recommendation_summary(recommendations: Dict[str, Any]) -> str:
    """Create a user-friendly summary of weather recommendations."""
    location = recommendations["location"]
    best_days = recommendations["best_days"]
    poor_days = recommendations["poor_days"]
    
    summary_parts = [f"Here's a quick look at the weather in {location}:"]
    
    if best_days:
        best_day = best_days[0]
        summary_parts.append(
            f"\n🌟 Best day for travel: {best_day['date']} "
            f"({best_day['summary']['condition']}, "
            f"{best_day['summary']['max_temp']}°C, "
            f"{best_day['summary']['chance_of_rain']}% chance of rain)"
        )
        
        if len(best_days) > 1:
            other_good_dates = [day["date"] for day in best_days[1:]]
            summary_parts.append(f"\n✨ Other good days: {', '.join(other_good_dates)}")
    
    if poor_days:
        poor_dates = [day["date"] for day in poor_days]
        summary_parts.append(
            f"\n⚠️ Days to avoid or plan indoor activities: {', '.join(poor_dates)} "
            "(due to unfavorable weather conditions)"
        )
    
    return "".join(summary_parts) 