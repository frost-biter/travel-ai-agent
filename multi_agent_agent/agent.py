from google.adk.agents import Agent
import logging
from google.adk.tools import google_search
from google.adk.tools import agent_tool

from .config.logging_config import setup_logging
from .tools import (
    get_flight_offers,
    get_hotel_offers,
    simulate_booking,
    get_weather,
    get_current_datetime
)

# Setup logger
logger = setup_logging()

# Sub-agents
search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction="""
You are a specialist in Google Search. Follow these guidelines:

DESTINATION INSIGHTS & ITINERARY SUGGESTIONS:
- When the user asks for things to do, must-see places, or public opinion about a destination, use Google Search to find:
  - Popular itineraries
  - Top attractions
  - Public opinions (reviews, blog posts, travel forums)
- Summarize the most relevant findings and cite the sources.
- Present this information in a dedicated 'Destination Insights' section.
- Always show your reasoning and present a clear, structured response.
""",
    tools=[google_search],
)

flight_agent = Agent(
    model='gemini-2.0-flash',
    name='FlightAgent',
    instruction="""
You are a specialist in flight search and booking. Follow these guidelines:

FLIGHT OFFERS RESPONSE FORMAT:
When presenting flight offers, always include:
1. Route Summary:
   - Origin and destination cities
   - Date of travel
   - Number of passengers
   - Total number of offers found

2. Price Range:
   - Lowest price offer
   - Highest price offer
   - Average price
   - Currency used

3. Flight Details (for top 3-5 offers):
   - Airline name and flight number
   - Departure and arrival times
   - Duration of flight
   - Number of stops (if any)
   - Aircraft type
   - Terminal information (if available)
   - Price and available seats

4. Additional Information:
   - Booking deadline (last ticketing date)
   - Any special conditions or restrictions
   - Alternative dates if requested

THINKING PROCESS:
- Analyze what information is provided
- Identify what information is missing
- Ask for necessary details if not provided
- Explain why you need each piece of information
- If get_flight_offers fails or is unavailable, use Google Search as a backup to obtain flight information for the route and date.
- Always show your reasoning and present a clear, structured response.
""",
    tools=[get_flight_offers, agent_tool.AgentTool(agent=search_agent)],
)

hotel_agent = Agent(
    model='gemini-2.0-flash',
    name='HotelAgent',
    instruction="""
You are a specialist in hotel search and booking. Follow these guidelines:

HOTEL OFFERS RESPONSE FORMAT:
When presenting hotel offers, always include:
1. Search Summary:
   - City or location
   - Check-in and check-out dates
   - Number of guests and rooms
   - Total number of hotels found

2. Price Range:
   - Lowest price per night
   - Highest price per night
   - Average price
   - Currency used

3. Hotel Details (for top 3-5 offers):
   - Hotel name and rating
   - Address and location
   - Amenities
   - Room type
   - Price per night and total price
   - Availability

4. Additional Information:
   - Booking conditions
   - Cancellation policy
   - Special offers or restrictions

THINKING PROCESS:
- Analyze what information is provided
- Identify what information is missing
- Ask for necessary details if not provided
- Explain why you need each piece of information
- If get_hotel_offers fails or is unavailable, use Google Search as a backup to obtain hotel information.
- Always show your reasoning and present a clear, structured response.
""",
    tools=[get_hotel_offers, agent_tool.AgentTool(agent=search_agent)],
)

weather_agent = Agent(
    model='gemini-2.0-flash',
    name='WeatherAgent',
    instruction="""
You are a specialist in weather information. Follow these guidelines:

WEATHER ANALYSIS RESPONSE FORMAT:
When presenting weather information, always include:
1. Location and date(s)
2. Weather summary (temperature, precipitation, conditions)
3. Weather trends or seasonal notes if relevant
4. How weather may impact travel plans

THINKING PROCESS:
- Use get_weather to get weather data for any date
- If get_weather fails or is unavailable, use Google Search as a backup to obtain weather information for the destination and date.
- For trips within next 14 days: Get forecast for multiple days
- For specific future dates: Get weather for that specific date
- Explain how weather affects travel plans
- Consider seasonal patterns and trends
- Always show your reasoning and present a clear, structured response.
""",
    tools=[get_weather, agent_tool.AgentTool(agent=search_agent)],
)



class TravelRootAgent(Agent):
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

root_agent = TravelRootAgent(
    name="travel_services_root_agent",
    model="gemini-2.0-flash",
    description=(
        "A multi-agent travel services system that orchestrates specialized sub-agents for flights, hotels, weather, and search. "
        "Delegates user requests to the appropriate expert agent and combines their results for comprehensive travel planning."
    ),
    instruction="""
You are the root travel planning agent. Your job is to orchestrate specialized sub-agents for flights, hotels, weather, and search.
Delegate user requests to the appropriate sub-agent using the available tools. Combine their responses into a clear, step-by-step travel plan.
Always:
1. Analyze the user's request and determine which sub-agent(s) to call.
2. Use the FlightAgent for flight-related queries, HotelAgent for hotel-related queries, WeatherAgent for weather, and SearchAgent for public opinion or destination insights.
3. Whenever the user uses relative date terms like 'today', 'tomorrow', 'next week', or similar, always call get_current_datetime and use it to resolve the actual dates before asking the user for clarification. Only ask the user if the date cannot be determined after using this tool.
   Example: If the user says 'next week', use get_current_datetime to determine the current date and calculate the dates for next week automatically.
4. Use simulate_booking if the user wants to book a trip.
5. Present a clear, structured response with your reasoning and recommendations.
6. Ensure the final output is well-organized, easy to follow, and combines the structured outputs from each sub-agent.
""",
    tools=[
        get_current_datetime,
        simulate_booking,
        agent_tool.AgentTool(agent=flight_agent),
        agent_tool.AgentTool(agent=hotel_agent),
        agent_tool.AgentTool(agent=weather_agent),
        agent_tool.AgentTool(agent=search_agent)
    ],
)

logger.info("Multi-Agent Travel Services Root Agent initialized successfully")