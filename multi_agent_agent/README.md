# Travel Services Agent

A Google ADK-based travel services agent that helps users plan their trips by providing information about flights and hotels. The agent can search for available options and simulate bookings.

## Features

- Flight search using Amadeus API
- Hotel search using Amadeus API
- Booking simulation (for demonstration purposes)
- Budget-aware travel planning
- Clear presentation of travel options

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with your Amadeus API credentials:
```
AMADEUS_API_KEY=your_api_key_here
AMADEUS_SECRET_KEY=your_secret_key_here
```

## Project Structure

```
multi_tool_agent/
├── config/             # Configuration management
├── services/          # API service implementations
├── tools/             # Agent tools
├── agent.py          # Main agent configuration
├── run.py            # Application entry point
└── requirements.txt  # Project dependencies
```

## Usage

1. Start the agent:
```bash
python run.py
```

2. The agent can help with:
- Searching for flights between cities
- Finding hotels at destinations
- Simulating travel bookings
- Providing travel recommendations based on budget and preferences

## API Dependencies

- Amadeus API (for flights and hotels)
  - Documentation: https://developers.amadeus.com/self-service/apis-docs
  - Required for flight and hotel searches

## Notes

- This is a demonstration project - bookings are simulated and no actual reservations are made
- All prices in booking simulations are placeholder values
- The agent uses the Gemini 2.0 Flash model for natural language understanding 