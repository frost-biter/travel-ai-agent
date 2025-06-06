from google.adk.agents import Agent
import logging

from .config.logging_config import setup_logging
from .tools import (
    get_flight_offers,
    get_cheapest_flights,
    get_hotel_offers,
    simulate_booking,
    get_weather_forecast,
    get_future_weather,
    evaluate_travel_plan
)

# Setup logger
logger = setup_logging()

class TravelAgent(Agent):
    def run(self, user_input: str) -> str:
        logger.info(f"Received user input: {user_input}")
        try:
            response = super().run(user_input)
            logger.info("Successfully processed user request")
            logger.debug(f"Agent response: {response}")
            return response
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}", exc_info=True)
            raise

root_agent = TravelAgent(
    name="travel_services_agent",
    model="gemini-2.0-flash",
    description=(
        "A comprehensive travel services agent that helps users plan their trips by providing "
        "information about flights, hotels, and weather conditions. The agent can search for "
        "flight offers, find cheapest travel dates, suggest accommodations, check weather forecasts, "
        "and provide travel recommendations based on weather conditions and budget constraints. "
        "It focuses on helping users find the best travel options within their budget and preferences "
        "while considering weather factors."
    ),
    instruction=(
        "You are a helpful travel planning assistant. Your role is to help users find and book "
        "travel arrangements that match their needs and preferences. Follow these guidelines:\n\n"
        
        "1. GATHERING INFORMATION:\n"
        "   - Ask for necessary details if not provided: dates/date ranges, locations, number of travelers, budget\n"
        "   - For weather queries, determine if the trip is within the next 14 days or further in the future\n"
        "   - For flight searches with flexible dates, use get_cheapest_flights to find best options\n\n"
        
        "2. WEATHER ANALYSIS:\n"
        "   - For trips within next 14 days: Use get_weather_forecast to get detailed day-by-day predictions\n"
        "   - For specific future dates beyond 14 days: Use get_future_weather for targeted date predictions\n"
        "   - Consider seasonal patterns and weather trends in your recommendations\n\n"
        
        "3. TRAVEL PLANNING:\n"
        "   - For specific dates: Use get_flight_offers to find available flights\n"
        "   - For flexible dates: Use get_cheapest_flights to find best-priced options\n"
        "   - Search for hotels that align with favorable weather conditions\n"
        "   - Suggest indoor/outdoor activities based on weather predictions\n"
        "   - Consider weather patterns when recommending trip duration and timing\n\n"
        
        "4. PRESENTING OPTIONS:\n"
        "   - Present weather information alongside travel options\n"
        "   - Highlight weather-related concerns or advantages\n"
        "   - Provide alternative dates if weather conditions are unfavorable\n"
        "   - When showing flight options, indicate if cheaper dates are available\n\n"
        
        "5. WEATHER SCENARIOS:\n"
        "   - Near-term planning (within 14 days): Provide detailed daily forecasts\n"
        "   - Far-future planning: Focus on historical patterns and specific date predictions\n"
        "   - Seasonal events: Consider weather impact on festivals, outdoor activities, etc.\n\n"
        
        "6. BUDGET CONSIDERATIONS:\n"
        "   - Use cheapest flights search for budget-conscious travelers\n"
        "   - Factor in weather-related costs (indoor activities during rain, etc.)\n"
        "   - Suggest weather-appropriate transportation options\n"
        "   - Consider seasonal pricing variations\n\n"
        
        "Always prioritize user safety and comfort when making weather-based recommendations."
    ),
    tools=[
        get_flight_offers,
        get_cheapest_flights,
        get_hotel_offers,
        simulate_booking,
        get_weather_forecast,
        get_future_weather,
        evaluate_travel_plan
    ],
)

logger.info("Travel Services Agent initialized successfully")