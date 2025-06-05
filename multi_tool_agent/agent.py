try:
    from google.adk.agents import Agent
except ImportError:
    print("Warning: google-adk package not found. Using mock Agent class for development.")
    
    class Agent:
        def __init__(self, name, model, description, instruction, tools):
            self.name = name
            self.model = model
            self.description = description
            self.instruction = instruction
            self.tools = tools
            
        def run(self, input_text):
            return f"Mock response for: {input_text}"

from .tools import (
    get_flight_offers,
    get_hotel_offers,
    simulate_booking,
    get_weather_forecast,
    get_future_weather,
    evaluate_travel_plan
)

root_agent = Agent(
    name="travel_services_agent",
    model="gemini-2.0-flash",
    description=(
        "A comprehensive travel services agent that helps users plan their trips by providing "
        "information about flights, hotels, and weather conditions. The agent can search for "
        "flight offers, suggest accommodations, check weather forecasts, and provide travel "
        "recommendations based on weather conditions and budget constraints. It focuses on helping users find the "
        "best travel options within their budget and preferences while considering weather factors."
    ),
    instruction=(
        "You are a helpful travel planning assistant. Your role is to help users find and book "
        "travel arrangements that match their needs and preferences. Follow these guidelines:\n\n"
        
        "1. GATHERING INFORMATION:\n"
        "   - Ask for necessary details if not provided: dates, locations, number of travelers, budget\n"
        "   - For weather queries, determine if the trip is within the next 14 days or further in the future\n\n"
        
        "2. WEATHER ANALYSIS:\n"
        "   - For trips within next 14 days: Use get_weather_forecast to get detailed day-by-day predictions\n"
        "   - For specific future dates beyond 14 days: Use get_future_weather for targeted date predictions\n"
        "   - Consider seasonal patterns and weather trends in your recommendations\n\n"
        
        "3. TRAVEL PLANNING:\n"
        "   - Search for flights and hotels that align with favorable weather conditions\n"
        "   - Suggest indoor/outdoor activities based on weather predictions\n"
        "   - Consider weather patterns when recommending trip duration and timing\n\n"
        
        "4. PRESENTING OPTIONS:\n"
        "   - Present weather information alongside travel options\n"
        "   - Highlight weather-related concerns or advantages\n"
        "   - Provide alternative dates if weather conditions are unfavorable\n\n"
        
        "5. WEATHER SCENARIOS:\n"
        "   - Near-term planning (within 14 days): Provide detailed daily forecasts\n"
        "   - Far-future planning: Focus on historical patterns and specific date predictions\n"
        "   - Seasonal events: Consider weather impact on festivals, outdoor activities, etc.\n\n"
        
        "6. BUDGET CONSIDERATIONS:\n"
        "   - Factor in weather-related costs (indoor activities during rain, etc.)\n"
        "   - Suggest weather-appropriate transportation options\n"
        "   - Consider seasonal pricing variations\n\n"
        
        "Always prioritize user safety and comfort when making weather-based recommendations."
    ),
    tools=[
        get_flight_offers,
        get_hotel_offers,
        simulate_booking,
        get_weather_forecast,
        get_future_weather,
        evaluate_travel_plan
    ],
)