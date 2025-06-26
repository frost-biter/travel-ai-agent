from typing import Dict, List, Any, Optional, Union
import logging
from enum import Enum
from .amadeus_client import AmadeusClient

logger = logging.getLogger('travel_agent')

class RadiusUnit(str, Enum):
    """Enum for radius unit options."""
    KM = "KM"
    MILE = "MILE"

class HotelSource(str, Enum):
    """Enum for hotel source options."""
    BEDBANK = "BEDBANK"
    DIRECTCHAIN = "DIRECTCHAIN"
    ALL = "ALL"

class HotelAmenities(str, Enum):
    """Enum for available hotel amenities."""
    SWIMMING_POOL = "SWIMMING_POOL"
    SPA = "SPA"
    FITNESS_CENTER = "FITNESS_CENTER"
    AIR_CONDITIONING = "AIR_CONDITIONING"
    RESTAURANT = "RESTAURANT"
    PARKING = "PARKING"
    PETS_ALLOWED = "PETS_ALLOWED"
    AIRPORT_SHUTTLE = "AIRPORT_SHUTTLE"
    BUSINESS_CENTER = "BUSINESS_CENTER"
    DISABLED_FACILITIES = "DISABLED_FACILITIES"
    WIFI = "WIFI"
    MEETING_ROOMS = "MEETING_ROOMS"
    NO_KID_ALLOWED = "NO_KID_ALLOWED"
    TENNIS = "TENNIS"
    GOLF = "GOLF"
    KITCHEN = "KITCHEN"
    ANIMAL_WATCHING = "ANIMAL_WATCHING"
    BABY_SITTING = "BABY-SITTING"
    BEACH = "BEACH"
    CASINO = "CASINO"
    JACUZZI = "JACUZZI"
    SAUNA = "SAUNA"
    SOLARIUM = "SOLARIUM"
    MASSAGE = "MASSAGE"
    VALET_PARKING = "VALET_PARKING"
    BAR_LOUNGE = "BAR or LOUNGE"
    KIDS_WELCOME = "KIDS_WELCOME"
    NO_PORN_FILMS = "NO_PORN_FILMS"
    MINIBAR = "MINIBAR"
    TELEVISION = "TELEVISION"
    WIFI_IN_ROOM = "WI-FI_IN_ROOM"
    ROOM_SERVICE = "ROOM_SERVICE"
    GUARDED_PARKING = "GUARDED_PARKG"
    SPECIAL_MENU = "SERV_SPEC_MENU"

class HotelService(AmadeusClient):
    """Service for hotel-related operations."""
    
    def search_hotels(
        self,
        city_code: str,
        radius: int = 50,
        radius_unit: RadiusUnit = RadiusUnit.KM,
        chain_codes: Optional[List[str]] = None,
        amenities: Optional[List[Union[str, HotelAmenities]]] = None,
        ratings: Optional[List[str]] = None,
        hotel_source: HotelSource = HotelSource.ALL
    ) -> List[Dict[str, Any]]:
        """
        Search for hotels in a city.
        
        Args:
            city_code: IATA city or airport code (e.g., 'PAR' for Paris)
            radius: Maximum distance from city center (default: 5)
            radius_unit: Unit for radius - KM or MILE (default: KM)
            chain_codes: Optional list of 2-letter hotel chain codes
            amenities: Optional list of amenities from HotelAmenities enum
            ratings: Optional list of hotel star ratings (1-5)
            hotel_source: Source of hotel data (default: ALL)
            
        Returns:
            List of hotels matching the criteria
            
        Raises:
            ValueError: If parameters are invalid
        """
        logger.info(f"Searching hotels in {city_code} within {radius} {radius_unit}")
        
        # Validate parameters
        if not city_code or len(city_code) != 3:
            logger.error(f"Invalid city code: {city_code}")
            raise ValueError("City code must be a 3-letter IATA code")
            
        if radius <= 0:
            logger.error(f"Invalid radius: {radius}")
            raise ValueError("Radius must be positive")
            
        if chain_codes:
            for code in chain_codes:
                if not (isinstance(code, str) and len(code) == 2 and code.isalpha()):
                    logger.error(f"Invalid chain code: {code}")
                    raise ValueError("Chain codes must be 2-letter alphabetic strings")
                    
        if ratings:
            valid_ratings = {"1", "2", "3", "4", "5"}
            invalid_ratings = [r for r in ratings if r not in valid_ratings]
            if invalid_ratings:
                logger.error(f"Invalid ratings: {invalid_ratings}")
                raise ValueError("Ratings must be between 1 and 5")
                
        # Build parameters
        params = {
            "cityCode": city_code.upper(),
            "radius": radius,
            "radiusUnit": radius_unit.value,
            "hotelSource": hotel_source.value
        }
        
        # Add optional parameters
        if chain_codes:
            params["chainCodes"] = chain_codes
            logger.debug(f"Added chain codes filter: {chain_codes}")
            
        if amenities:
            # Convert string amenities to enum values if needed
            validated_amenities = []
            for amenity in amenities:
                if isinstance(amenity, str):
                    try:
                        validated_amenities.append(HotelAmenities[amenity].value)
                    except KeyError:
                        logger.warning(f"Invalid amenity ignored: {amenity}")
                else:
                    validated_amenities.append(amenity.value)
            params["amenities"] = validated_amenities
            logger.debug(f"Added amenities filter: {validated_amenities}")
            
        if ratings:
            params["ratings"] = ratings
            logger.debug(f"Added ratings filter: {ratings}")
            
        try:
            logger.debug(f"Searching with parameters: {params}")
            response = self._make_request(
                "GET",
                "/v1/reference-data/locations/hotels/by-city",
                params=params
            )
            return self._parse_hotels(response)
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to search hotels: {error_msg}", exc_info=True)
            
            if "477" in error_msg:
                raise ValueError("Invalid parameter format")
            elif "32171" in error_msg:
                raise ValueError("Missing required parameters")
            else:
                raise
    
    def _parse_hotels(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse and simplify hotels response."""
        hotels = []
        data = response.get("data", [])
        logger.debug(f"Parsing {len(data)} hotels")
        
        for hotel in data:
            hotel_data = {
                "hotelId": hotel.get("hotelId"),
                "name": hotel.get("name"),
                "iataCode": hotel.get("iataCode"),
                "distance": {
                    "value": hotel.get("distance", {}).get("value"),
                    "unit": hotel.get("distance", {}).get("unit")
                },
                "address": {
                    "cityName": hotel.get("address", {}).get("cityName"),
                    "countryCode": hotel.get("address", {}).get("countryCode"),
                    "stateCode": hotel.get("address", {}).get("stateCode"),
                    "postalCode": hotel.get("address", {}).get("postalCode"),
                    "lines": hotel.get("address", {}).get("lines", [])
                },
                "geoCode": {
                    "latitude": hotel.get("geoCode", {}).get("latitude"),
                    "longitude": hotel.get("geoCode", {}).get("longitude")
                },
                "chainCode": hotel.get("chainCode"),
                "amenities": hotel.get("amenities", []),
                "rating": hotel.get("rating")
            }
            hotels.append(hotel_data)
            logger.debug(
                f"Parsed hotel {hotel_data['hotelId']}: "
                f"{hotel_data['name']} ({hotel_data['rating']}★)"
            )
        
        return hotels
    
    def get_hotel_offer_details(self, offer_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific hotel offer.
        
        Args:
            offer_id: The hotel offer ID from search results
            
        Returns:
            Detailed hotel offer information
        """
        logger.info(f"Getting details for hotel offer {offer_id}")
        try:
            response = self._make_request(
                "GET", 
                f"/v3/shopping/hotel-offers/{offer_id}"
            )
            details = self._parse_hotel_offer_details(response)
            logger.info(f"Successfully retrieved details for hotel offer {offer_id}")
            return details
        except Exception as e:
            logger.error(f"Failed to get hotel offer details: {str(e)}", exc_info=True)
            raise
    
    def _parse_hotel_offer_details(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and simplify detailed hotel offer response."""
        if not response.get("data"):
            logger.warning("No data found in hotel offer details response")
            return {}
            
        offer = response["data"]
        hotel = offer.get("hotel", {})
        
        details = {
            "offerId": offer.get("id"),
            "hotelId": hotel.get("hotelId"),
            "name": hotel.get("name"),
            "rating": hotel.get("rating"),
            "description": hotel.get("description", {}).get("text"),
            "address": {
                "cityName": hotel.get("address", {}).get("cityName"),
                "countryCode": hotel.get("address", {}).get("countryCode"),
                "stateCode": hotel.get("address", {}).get("stateCode"),
                "postalCode": hotel.get("address", {}).get("postalCode"),
                "lines": hotel.get("address", {}).get("lines", [])
            },
            "contact": hotel.get("contact"),
            "amenities": hotel.get("amenities", []),
            "price": {
                "total": offer.get("price", {}).get("total"),
                "currency": offer.get("price", {}).get("currency"),
                "variations": offer.get("price", {}).get("variations", {})
            },
            "policies": offer.get("policies", {}),
            "room": {
                "type": offer.get("room", {}).get("type"),
                "description": offer.get("room", {}).get("description")
            },
            "available": True
        }
        logger.debug(f"Parsed details for hotel offer {details['offerId']}")
        return details 