from google.adk.agents import Agent
import logging
from google.adk.tools import google_search
from google.adk.tools import agent_tool
from .config.agent_config import AGENT_CONFIG       
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

search_agent = Agent(
    model=AGENT_CONFIG['search']['model'],
    name='SearchAgent',
    instruction=AGENT_CONFIG['search']['instruction'],
    tools=[google_search],
)

root_agent = TravelAgent(
    name="travel_services_agent",
    model=AGENT_CONFIG['root']['model'],
    description=AGENT_CONFIG['root']['description'],
    instruction=AGENT_CONFIG['root']['instruction'],
    tools=[
        get_flight_offers,
        get_hotel_offers,
        simulate_booking,
        get_weather,
        get_current_datetime,
        agent_tool.AgentTool(agent=search_agent)
    ],
)

logger.info("Travel Services Agent initialized successfully")