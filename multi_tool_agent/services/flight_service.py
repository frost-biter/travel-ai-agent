from typing import Dict, List, Any, Optional, Union
import logging
from datetime import datetime, timedelta
from .amadeus_client import AmadeusClient

logger = logging.getLogger('travel_agent')

class FlightService(AmadeusClient):
    """Service for flight-related operations."""
    
    def search_flights(self, origin: str, destination: str, date: str, adults: int = 1) -> List[Dict[str, Any]]:
        """
        Search for flight offers for a specific date.
        
        Args:
            origin: Origin airport IATA code
            destination: Destination airport IATA code
            date: Departure date in YYYY-MM-DD format
            adults: Number of adult passengers
            
        Returns:
            List of simplified flight offers
        """
        logger.info(f"Searching flights from {origin} to {destination} on {date}")
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": date,
            "adults": adults
        }
        
        try:
            response = self._make_request("GET", "/v2/shopping/flight-offers", params)
            offers = self._parse_flight_offers(response)
            logger.info(f"Found {len(offers)} flight offers")
            return offers
        except Exception as e:
            logger.error(f"Failed to search flights: {str(e)}", exc_info=True)
            raise
    
    def search_cheapest_flights(
        self,
        origin: str,
        destination: str,
        departure_date: Optional[str] = None,
        one_way: bool = False,
        duration: Optional[str] = None,
        non_stop: bool = False,
        max_price: Optional[int] = None,
        view_by: str = "DATE"
    ) -> List[Dict[str, Any]]:
        """
        Search for cheapest flight dates between cities.
        
        Args:
            origin: IATA code of origin city (e.g., 'MAD' for Madrid)
            destination: IATA code of destination city (e.g., 'MUC' for Munich)
            departure_date: Optional date or range in YYYY-MM-DD format.
                          For range, use comma (e.g., '2024-03-01,2024-03-31')
            one_way: If True, search one-way flights only. Default False (round-trip)
            duration: For round trips, exact duration or range in days (e.g., '2,8')
            non_stop: If True, search non-stop flights only. Default False
            max_price: Maximum price limit (positive integer)
            view_by: How to view results: 'DATE', 'DURATION', or 'WEEK'
                    DATE: Best price per departure date
                    DURATION: Best price per duration (round-trip)
                    WEEK: Best price per week
            
        Returns:
            List of cheapest flight dates with prices
            
        Raises:
            ValueError: If parameters are invalid or incompatible
        """
        logger.info(f"Searching cheapest flights from {origin} to {destination}")
        
        # Validate parameters
        if one_way and duration:
            logger.error("Duration parameter cannot be used with one-way flights")
            raise ValueError("Duration parameter cannot be used with one-way flights")
            
        if view_by not in ["DATE", "DURATION", "WEEK"]:
            logger.error(f"Invalid view_by parameter: {view_by}")
            raise ValueError("view_by must be one of: DATE, DURATION, WEEK")
            
        # Build parameters
        params = {
            "origin": origin.upper(),
            "destination": destination.upper(),
            "oneWay": str(one_way).lower(),
            "nonStop": str(non_stop).lower(),
            "viewBy": view_by
        }
        
        # Add optional parameters
        if departure_date:
            params["departureDate"] = departure_date
            
        if duration and not one_way:
            params["duration"] = duration
            
        if max_price:
            if not isinstance(max_price, int) or max_price <= 0:
                logger.error(f"Invalid max_price: {max_price}")
                raise ValueError("max_price must be a positive integer")
            params["maxPrice"] = max_price
            
        try:
            logger.debug(f"Searching with parameters: {params}")
            response = self._make_request(
                "GET",
                "/v1/shopping/flight-dates",
                params=params
            )
            return self._parse_cheapest_dates(response)
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to search cheapest flights: {error_msg}", exc_info=True)
            
            # Handle specific API errors
            if "425" in error_msg:
                raise ValueError("Invalid date format. Use YYYY-MM-DD format")
            elif "477" in error_msg:
                raise ValueError("Invalid parameter format")
            elif "2668" in error_msg:
                raise ValueError("Invalid parameter combination")
            elif "4926" in error_msg:
                raise ValueError("Invalid data received from server")
            elif "32171" in error_msg:
                raise ValueError("Missing required parameters")
            else:
                raise
    
    def _parse_cheapest_dates(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse and simplify cheapest dates response."""
        dates = []
        data = response.get("data", [])
        logger.debug(f"Parsing {len(data)} flight dates")
        
        for date_data in data:
            if date_data.get("type") != "flight-date":
                continue
                
            flight_date = {
                "type": date_data.get("type"),
                "origin": date_data.get("origin"),
                "destination": date_data.get("destination"),
                "departure_date": date_data.get("departureDate"),
                "return_date": date_data.get("returnDate"),
                "price": {
                    "total": date_data.get("price", {}).get("total"),
                    "currency": date_data.get("price", {}).get("currency", "EUR")
                }
            }
            
            # Add links if available
            links = date_data.get("links", {})
            if links:
                flight_date["links"] = links
                
            dates.append(flight_date)
            logger.debug(
                f"Parsed flight date: {flight_date['departure_date']} "
                f"(Return: {flight_date['return_date']}) "
                f"Price: {flight_date['price']['total']} {flight_date['price']['currency']}"
            )
        
        # Sort by price
        dates.sort(key=lambda x: float(x["price"]["total"]))
        return dates
    
    def _parse_flight_offers(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse and simplify flight offers response."""
        offers = []
        carriers = response.get("dictionaries", {}).get("carriers", {})
        aircrafts = response.get("dictionaries", {}).get("aircraft", {})
        currencies = response.get("dictionaries", {}).get("currencies", {})

        for offer in response.get("data", []):
            simplified_offer = {
                "id": offer.get("id"),
                "price": {
                    "total": offer.get("price", {}).get("total"),
                    "currency": offer.get("price", {}).get("currency")
                },
                "seats_available": offer.get("numberOfBookableSeats"),
                "last_ticketing_date": offer.get("lastTicketingDate")
            }
            
            # Process segments
            segments = []
            for itinerary in offer.get("itineraries", []):
                for segment in itinerary.get("segments", []):
                    carrier_code = segment.get("carrierCode")
                    aircraft_code = segment.get("aircraft", {}).get("code")
                    
                    segments.append({
                        "departure": {
                            "airport": segment.get("departure", {}).get("iataCode"),
                            "terminal": segment.get("departure", {}).get("terminal"),
                            "time": segment.get("departure", {}).get("at")
                        },
                        "arrival": {
                            "airport": segment.get("arrival", {}).get("iataCode"),
                            "terminal": segment.get("arrival", {}).get("terminal"),
                            "time": segment.get("arrival", {}).get("at")
                        },
                        "carrier": {
                            "code": carrier_code,
                            "name": carriers.get(carrier_code)
                        },
                        "flight_number": segment.get("number"),
                        "aircraft": {
                            "code": aircraft_code,
                            "name": aircrafts.get(aircraft_code)
                        },
                        "duration": segment.get("duration"),
                        "stops": segment.get("numberOfStops", 0)
                    })
            
            simplified_offer["segments"] = segments
            offers.append(simplified_offer)
        
        return offers 