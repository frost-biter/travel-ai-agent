from typing import Dict, List, Any
from .amadeus_client import AmadeusClient

class HotelService(AmadeusClient):
    """Service for hotel-related operations."""
    
    def search_hotels(self, city_code: str, check_in: str, check_out: str, adults: int = 1) -> List[Dict[str, Any]]:
        """
        Search for hotel offers in a city.
        
        Args:
            city_code: City IATA code
            check_in: Check-in date in YYYY-MM-DD format
            check_out: Check-out date in YYYY-MM-DD format
            adults: Number of adult guests
            
        Returns:
            List of simplified hotel offers
        """
        # params = {
        #     "cityCode": city_code,
        #     "checkInDate": check_in,
        #     "checkOutDate": check_out,
        #     "adults": adults,
        #     "radius": 50,
        #     "radiusUnit": "KM"

        # }
        params = {
            "cityCode": city_code,  # Required: IATA city or airport code
            "radius": 50,        # Optional: Distance in radiusUnit (default 5)
            "radiusUnit": "KM", # Optional: 'KM' or 'MILE' (default 'KM')
            # "chainCodes": ["MC", "HY"],  # Optional: List of hotel chain codes (2-letter codes)
            "amenities": ["WIFI", "PARKING", "RESTAURANT"],  # Optional: List of desired amenities
            "ratings": ["3", "4", "5"],  # Optional: List of star ratings
            "hotelSource": "ALL"         # Optional: BEDBANK, DIRECTCHAIN, or ALL (default 'ALL')
        }
        
        response = self._make_request("GET", "/v1/reference-data/locations/hotels/by-city", params)
        return response
        # return self._parse_hotel_offers(response)
    
    # def get_hotel_offer(self, offer_id: str) -> Dict[str, Any]:
    #     """
    #     Get detailed information about a specific hotel offer.
        
    #     Args:
    #         offer_id: The hotel offer ID
            
    #     Returns:
    #         Detailed hotel offer information
    #     """
    #     response = self._make_request("GET", f"/v2/shopping/hotel-offers/{offer_id}")
    #     return self._parse_hotel_offer_details(response)
    
    # def _parse_hotel_offers(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
    #     """Parse and simplify hotel offers response."""
    #     offers = []
        
    #     for offer in response.get("data", []):
    #         hotel = offer.get("hotel", {})
            
    #         simplified_offer = {
    #             "id": offer.get("id"),
    #             "hotel": {
    #                 "name": hotel.get("name"),
    #                 "rating": hotel.get("rating"),
    #                 "address": {
    #                     "lines": hotel.get("address", {}).get("lines", []),
    #                     "city": hotel.get("address", {}).get("cityName"),
    #                     "country": hotel.get("address", {}).get("countryCode")
    #                 },
    #                 "amenities": hotel.get("amenities", []),
    #                 "contact": {
    #                     "phone": hotel.get("contact", {}).get("phone"),
    #                     "email": hotel.get("contact", {}).get("email")
    #                 }
    #             },
    #             "available": offer.get("available", False),
    #             "offers": []
    #         }
            
    #         # Process room offers
    #         for room_offer in offer.get("offers", []):
    #             simplified_offer["offers"].append({
    #                 "id": room_offer.get("id"),
    #                 "room": {
    #                     "type": room_offer.get("room", {}).get("type"),
    #                     "description": room_offer.get("room", {}).get("description")
    #                 },
    #                 "guests": {
    #                     "adults": room_offer.get("guests", {}).get("adults")
    #                 },
    #                 "price": {
    #                     "total": room_offer.get("price", {}).get("total"),
    #                     "currency": room_offer.get("price", {}).get("currency")
    #                 },
    #                 "policies": room_offer.get("policies", {})
    #             })
            
    #         offers.append(simplified_offer)
        
    #     return offers
    
    # def _parse_hotel_offer_details(self, response: Dict[str, Any]) -> Dict[str, Any]:
    #     """Parse and simplify detailed hotel offer response."""
    #     if not response.get("data"):
    #         return {}
            
    #     offer = response["data"]
    #     return {
    #         "id": offer.get("id"),
    #         "hotel": {
    #             "name": offer.get("hotel", {}).get("name"),
    #             "rating": offer.get("hotel", {}).get("rating"),
    #             "description": offer.get("hotel", {}).get("description"),
    #             "address": offer.get("hotel", {}).get("address", {}),
    #             "amenities": offer.get("hotel", {}).get("amenities", []),
    #             "media": offer.get("hotel", {}).get("media", [])
    #         },
    #         "room": {
    #             "type": offer.get("room", {}).get("type"),
    #             "description": offer.get("room", {}).get("description")
    #         },
    #         "price": offer.get("price", {}),
    #         "policies": offer.get("policies", {}),
    #         "payment": offer.get("payment", {})
    #     } 