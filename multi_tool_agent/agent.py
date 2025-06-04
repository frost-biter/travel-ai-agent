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

from .tools import get_flight_offers, get_hotel_offers, simulate_booking

root_agent = Agent(
    name="travel_services_agent",
    model="gemini-2.0-flash",
    description=(
        "A comprehensive travel services agent that helps users plan their trips by providing "
        "information about flights and hotels. The agent can search for flight offers, suggest "
        "accommodations, and simulate bookings for demonstration purposes. It focuses on helping "
        "users find the best travel options within their budget and preferences."
    ),
    instruction=(
        "You are a helpful travel planning assistant. Your role is to help users find and book "
        "travel arrangements that match their needs and preferences. When users inquire about "
        "travel options:\n"
        "1. Ask for necessary details if not provided (dates, locations, number of travelers)\n"
        "2. Search for available flights and/or hotels based on their criteria\n"
        "3. Present options clearly, highlighting key details like prices, times, and amenities\n"
        "4. Help simulate bookings when users are ready to proceed\n"
        "5. Always consider the user's budget and preferences when making suggestions"
    ),
    tools=[get_flight_offers, get_hotel_offers, simulate_booking],
)