import requests
import os
import pprint


def get_flight_offers(origin: str, destination: str, date: str) -> dict:
    """
    Fetch flight offers from Amadeus API.
    """
    access_token = get_amadeus_token()
    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": 1
    }

    response = requests.get(url, headers=headers, params=params)
    if response.ok:
        data = response.json()
        simplified_offers = parse_amadeus_flight_offers(data)
        pprint.pprint(simplified_offers[0])
        return {"flight_offers": simplified_offers} 
    else:
        return {"error": response.text}

def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("AMADEUS_API_KEY"),
        "client_secret": os.getenv("AMADEUS_SECRET_KEY")
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def parse_amadeus_flight_offers(response_json):
    """
    Parses Amadeus flight offers response JSON and extracts simplified flight offer info.

    Args:
        response_json (dict): JSON response from Amadeus flight offers API.

    Returns:
        list of dict: List of simplified flight offer data.
    """
    offers = []
    carriers = response_json.get("dictionaries", {}).get("carriers", {})
    aircrafts = response_json.get("dictionaries", {}).get("aircraft", {})
    currencies = response_json.get("dictionaries", {}).get("currencies", {})

    for offer in response_json.get("data", []):
        offer_id = offer.get("id")
        price_info = offer.get("price", {})
        currency_code = price_info.get("currency")
        currency_name = currencies.get(currency_code, currency_code)
        total_price = price_info.get("total")

        available_seats = offer.get("numberOfBookableSeats")
        last_ticketing_date = offer.get("lastTicketingDate")
        validating_airlines = offer.get("validatingAirlineCodes", [])
        validating_airline = validating_airlines[0] if validating_airlines else None
        validating_airline_name = carriers.get(validating_airline, validating_airline)

        # Process first itinerary only (usually there's only one)
        itinerary = offer.get("itineraries", [{}])[0]
        itinerary_duration = itinerary.get("duration")
        segments = []
        for segment in itinerary.get("segments", []):
            seg_departure = segment.get("departure", {})
            seg_arrival = segment.get("arrival", {})
            seg_aircraft_code = segment.get("aircraft", {}).get("code")
            segments.append({
                "from": seg_departure.get("iataCode"),
                "to": seg_arrival.get("iataCode"),
                "departure": seg_departure.get("at"),
                "arrival": seg_arrival.get("at"),
                "departure_terminal": seg_departure.get("terminal"),
                "arrival_terminal": seg_arrival.get("terminal"),
                "carrier_code": segment.get("carrierCode"),
                "carrier_name": carriers.get(segment.get("carrierCode"), segment.get("carrierCode")),
                "flight_number": segment.get("number"),
                "aircraft_code": seg_aircraft_code,
                "aircraft_name": aircrafts.get(seg_aircraft_code, seg_aircraft_code),
                "duration": segment.get("duration"),
                "number_of_stops": segment.get("numberOfStops")
            })

        # Traveler pricing (for first traveler pricing only)
        traveler_pricing = offer.get("travelerPricings", [{}])[0]
        fare_option = traveler_pricing.get("fareOption")
        traveler_type = traveler_pricing.get("travelerType")
        traveler_price_info = traveler_pricing.get("price", {})
        traveler_price_total = traveler_price_info.get("total")
        traveler_currency = traveler_price_info.get("currency")
        fare_details = traveler_pricing.get("fareDetailsBySegment", [{}])[0]
        cabin = fare_details.get("cabin")
        booking_class = fare_details.get("class")
        checked_bags = fare_details.get("includedCheckedBags", {})
        checked_bags_weight = checked_bags.get("weight")
        checked_bags_unit = checked_bags.get("weightUnit")

        simplified_offer = {
            "id": offer_id,
            "price": {
                "total": total_price,
                "currency_code": currency_code,
                "currency_name": currency_name
            },
            "available_seats": available_seats,
            "last_ticketing_date": last_ticketing_date,
            "validating_airline": {
                "code": validating_airline,
                "name": validating_airline_name
            },
            "itinerary": {
                "duration": itinerary_duration,
                "segments": segments
            },
            "traveler_pricing": {
                "traveler_type": traveler_type,
                "fare_option": fare_option,
                "price_total": traveler_price_total,
                "price_currency": traveler_currency,
                "cabin": cabin,
                "booking_class": booking_class,
                "checked_bags_weight": checked_bags_weight,
                "checked_bags_unit": checked_bags_unit
            }
        }
        offers.append(simplified_offer)

    return offers
