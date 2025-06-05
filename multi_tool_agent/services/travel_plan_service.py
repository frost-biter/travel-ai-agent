from typing import Dict, Any, List
from datetime import datetime, timedelta
from .weather_service import WeatherService
from .flight_service import FlightService
from .hotel_service import HotelService

class TravelPlanService:
    """Service for collecting travel plan data for AI evaluation."""
    
    def __init__(self):
        self.weather_service = WeatherService()
        self.flight_service = FlightService()
        self.hotel_service = HotelService()
        
    def collect_travel_data(
        self,
        origin: str,
        destination: str,
        start_date: str,
        end_date: str,
        max_budget: float,
        adults: int = 1
    ) -> Dict[str, Any]:
        """
        Collect all relevant data for AI to evaluate travel plans.
        
        Args:
            origin: Origin airport IATA code
            destination: Destination airport IATA code
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            max_budget: Maximum budget for the trip
            adults: Number of adult travelers
            
        Returns:
            Dictionary containing all travel-related data for AI evaluation
        """
        # Get weather data
        weather_data = self.weather_service.get_travel_recommendation(destination)
        
        # Get flight options
        flight_offers = self.flight_service.search_flights(origin, destination, start_date, adults)
        
        # Get hotel options
        hotel_offers = self.hotel_service.search_hotels(destination, start_date, end_date, adults)
        
        # Calculate trip duration
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        duration = (end - start).days
        
        # Organize flight data
        flight_data = []
        for flight in flight_offers:
            flight_data.append({
                "carrier": flight.get("carrier"),
                "departure_time": flight.get("departure", {}).get("time"),
                "arrival_time": flight.get("arrival", {}).get("time"),
                "price": flight.get("price", {}).get("total"),
                "currency": flight.get("price", {}).get("currency", "USD"),
                "seats_available": flight.get("seats_available"),
                "cabin_class": flight.get("cabin_class")
            })
        
        # Organize hotel data
        hotel_data = []
        for hotel in hotel_offers:
            hotel_offers_list = []
            for offer in hotel.get("offers", []):
                hotel_offers_list.append({
                    "room_type": offer.get("room", {}).get("type"),
                    "price_per_night": offer.get("price", {}).get("total"),
                    "currency": offer.get("price", {}).get("currency", "USD"),
                    "board_type": offer.get("board_type"),
                    "cancellation_policy": offer.get("policies", {}).get("cancellation")
                })
            
            hotel_data.append({
                "name": hotel.get("name"),
                "rating": hotel.get("rating"),
                "location": {
                    "address": hotel.get("address", {}).get("lines", []),
                    "city": hotel.get("address", {}).get("cityName"),
                    "distance_to_center": hotel.get("distance_to_center")
                },
                "amenities": hotel.get("amenities", []),
                "offers": hotel_offers_list
            })
        
        # Organize weather data
        weather_details = []
        for day in weather_data.get("forecast", []):
            weather_details.append({
                "date": day.get("date"),
                "condition": day.get("condition"),
                "max_temp": day.get("max_temp"),
                "min_temp": day.get("min_temp"),
                "chance_of_rain": day.get("chance_of_rain"),
                "uv_index": day.get("uv"),
                "sunrise": day.get("sunrise"),
                "sunset": day.get("sunset")
            })
        
        # Return comprehensive data for AI evaluation
        return {
            "trip_details": {
                "origin": origin,
                "destination": destination,
                "start_date": start_date,
                "end_date": end_date,
                "duration_days": duration,
                "travelers": adults,
                "max_budget": max_budget
            },
            "weather_data": {
                "location": weather_data.get("location"),
                "daily_forecast": weather_details
            },
            "transportation": {
                "flights": flight_data
            },
            "accommodation": {
                "hotels": hotel_data
            }
        } 