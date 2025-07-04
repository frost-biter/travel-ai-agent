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