from typing import Dict, Any, List, Optional
from datetime import datetime
from .weatherapi_client import WeatherAPIClient

class WeatherService(WeatherAPIClient):
    """Service for weather-related operations."""
    
    def get_forecast(self, location: str, days: int = 7, aqi: str = "no") -> Dict[str, Any]:
        """
        Get weather forecast for a location.
        
        Args:
            location: City name, lat/lon, or zip code
            days: Number of forecast days (1-14)
            aqi: Include air quality data ("yes"/"no")
            
        Returns:
            Dictionary containing weather forecast data
        """
        params = {
            "q": location,
            "days": min(max(1, days), 14),  # Ensure days is between 1 and 14
            "aqi": aqi
        }
        
        response = self._make_request("GET", "/forecast.json", params)
        return self._parse_forecast(response)
    
    def get_future_weather(self, location: str, future_date: str) -> Dict[str, Any]:
        """
        Get future weather prediction for a location.
        
        Args:
            location: City name, lat/lon, or zip code
            future_date: Future date in YYYY-MM-DD format
            
        Returns:
            Dictionary containing future weather prediction
        """
        params = {
            "q": location,
            "dt": future_date
        }
        
        response = self._make_request("GET", "/future.json", params)
        return self._parse_future_weather(response)
    
    def get_current_weather(self, location: str) -> Dict[str, Any]:
        """
        Get current weather conditions for a location.
        Note: This is currently not used for travel recommendations,
        but could be used for live updates in the future.
        
        Args:
            location: City name, lat/lon, or zip code
            
        Returns:
            Dictionary containing current weather conditions
        """
        params = {"q": location}
        response = self._make_request("GET", "/current.json", params)
        return self._parse_current_weather(response)
    
    def _parse_forecast(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and organize forecast response."""
        location = response.get("location", {})
        forecast_days = response.get("forecast", {}).get("forecastday", [])
        
        return {
            "location": {
                "name": location.get("name"),
                "region": location.get("region"),
                "country": location.get("country"),
                "lat": location.get("lat"),
                "lon": location.get("lon"),
                "tz_id": location.get("tz_id"),
                "localtime": location.get("localtime")
            },
            "forecast": [
                {
                    "date": day.get("date"),
                    "day": {
                        "maxtemp_c": day.get("day", {}).get("maxtemp_c"),
                        "mintemp_c": day.get("day", {}).get("mintemp_c"),
                        "totalsnow_cm": day.get("day", {}).get("totalsnow_cm", 0.0),
                        "daily_chance_of_rain": day.get("day", {}).get("daily_chance_of_rain"),
                        "daily_chance_of_snow": day.get("day", {}).get("daily_chance_of_snow"),
                        "condition": day.get("day", {}).get("condition", {}).get("text"),
                        "uv": day.get("day", {}).get("uv")
                    },
                    "astro": {
                        "sunrise": day.get("astro", {}).get("sunrise"),
                        "sunset": day.get("astro", {}).get("sunset"),
                        "moon_phase": day.get("astro", {}).get("moon_phase")
                    }
                }
                for day in forecast_days
            ]
        }
    
    def _parse_future_weather(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and organize future weather response."""
        location = response.get("location", {})
        forecast_day = response.get("forecast", {}).get("forecastday", [{}])[0]
        
        return {
            "location": {
                "name": location.get("name"),
                "region": location.get("region"),
                "country": location.get("country"),
                "lat": location.get("lat"),
                "lon": location.get("lon"),
                "tz_id": location.get("tz_id"),
                "localtime": location.get("localtime")
            },
            "forecast": {
                "date": forecast_day.get("date"),
                "day": {
                    "maxtemp_c": forecast_day.get("day", {}).get("maxtemp_c"),
                    "mintemp_c": forecast_day.get("day", {}).get("mintemp_c"),
                    "condition": forecast_day.get("day", {}).get("condition", {}).get("text"),
                    "uv": forecast_day.get("day", {}).get("uv")
                },
                "astro": {
                    "sunrise": forecast_day.get("astro", {}).get("sunrise"),
                    "sunset": forecast_day.get("astro", {}).get("sunset"),
                    "moon_phase": forecast_day.get("astro", {}).get("moon_phase")
                }
            }
        }
    
    def _parse_current_weather(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and organize current weather response."""
        location = response.get("location", {})
        current = response.get("current", {})
        
        return {
            "location": {
                "name": location.get("name"),
                "region": location.get("region"),
                "country": location.get("country"),
                "lat": location.get("lat"),
                "lon": location.get("lon"),
                "tz_id": location.get("tz_id"),
                "localtime": location.get("localtime")
            },
            "current": {
                "temp_c": current.get("temp_c"),
                "is_day": current.get("is_day"),
                "condition": current.get("condition", {}).get("text"),
                "humidity": current.get("humidity"),
                "cloud": current.get("cloud"),
                "feelslike_c": current.get("feelslike_c"),
                "uv": current.get("uv")
            }
        } 