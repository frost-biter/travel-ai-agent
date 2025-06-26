# 🌍 Travel Services Aggregator

This project integrates various free and commercial APIs to offer users a comprehensive and budget-aware travel planning platform. From checking flights and hotels to simulating bookings and suggesting itineraries — it's designed to cover every phase of travel planning.

## ✅ Completed Features

1. **Comprehensive Logging System**
   - Implemented file and console handlers
   - Added rotating file handler (5MB max, 5 backup files)
   - Detailed error logging and request/response tracking
   - Cross-service logging integration

2. **API Integration Improvements**
   - Fixed form data handling in API requests
   - Properly configured Amadeus authentication
   - Implemented correct data formats across services

3. **Flight Services**
   - Added Flight Cheapest Date Search API
   - Implemented multiple view modes (DATE/DURATION/WEEK)
   - Added parameters for one-way/round-trip, duration, non-stop flights
   - Price filtering and comprehensive error handling

4. **Hotel Services**
   - Updated Hotel Search API implementation
   - Added support for radius, chain codes, and amenities
   - Implemented parameter validation
   - Enhanced response parsing

---

## 🔌 Integrated APIs

1. **Skyscanner APIs**  
   *Category:* Travel (Flights)  
   *Use:* Alternative data source for flight pricing and routes.

2. **Amadeus for Developers**  
   *Categories:* Flights, Hotels, Points of Interest (POIs), Itineraries  
   *Use:* Core data provider for flight offers, hotel availability, and travel suggestions.  
   [Live Examples & Docs](https://developers.amadeus.com/self-service/apis-docs/guides/developer-guides/examples/live-examples/)

3. **OpenTripMap API**  
   *Category:* Tourist Attractions  
   *Use:* Discover tourist attractions and POIs with rich geolocation data.

4. **Payment & Booking Simulation**  
   *Custom module*  
   *Use:* Mimics the behavior of a live booking system for testing and user interaction.

5. **Budget-Based Travel Guidance**  
   *Planned Feature*  
   *Use:* Agent-driven discussions to help users plan within their budget constraints.

---

## 🎯 Upcoming Features & Improvements

### Technical Enhancements
1. **Multi-Source Integration**
   - Additional flight APIs integration
   - Train service APIs integration
   - API fallback mechanisms
   - Response aggregation and normalization

2. **Function Optimization**
   - Merge similar functions across services
   - Implement common utilities
   - Standardize error handling

3. **Web Scraping Integration**
   - Itinerary data collection
   - Price comparison
   - Travel reviews and recommendations

4. **Booking Simulation**
   - Mock booking flow
   - Payment simulation
   - Booking confirmation system

### Architecture & Intelligence

1. **Multi-Agent System**
   - Specialized agents for different tasks
   - Inter-agent communication
   - Task delegation and coordination

2. **Reasoning & Self-Evaluation**
   - Implementation of reasoning frameworks
   - Self-evaluation mechanisms
   - Performance metrics tracking
   - Decision explanation system

### Documentation & Research

1. **AI Limitations Documentation**
   - Agentic AI constraints
   - LLM capabilities and limitations
   - Edge cases and failure modes

2. **Instruction Improvements**
   - Open-ended instruction format
   - Context-aware guidance
   - Dynamic response handling

3. **Research Presentation**
   - Findings and insights
   - Performance metrics
   - Architecture overview
   - Future recommendations

---

## ✅ Feature Overview

| Feature                   | Source(s)                                |
|---------------------------|------------------------------------------|
| ✈️ Flight Availability     | **Amadeus API**                          |
| 🚆 Train Availability      | **APISetu (CRIS)**                       |
| 🏨 Hotel Availability      | **Amadeus API**                          |
| 🗺️ Tourist Spots & POIs    | **Amadeus**, **OpenTripMap**             |
| 🧭 Suggested Itineraries   | **Amadeus API**                          |

---

## 🧠 Extended Features & Suggestions

| Feature                          | Why It's Useful                     | Suggested APIs / Sources                              |
|----------------------------------|-------------------------------------|--------------------------------------------------------|
| 🌦️ Weather Info                 | Clothing and time planning          | **OpenWeatherMap**, **WeatherAPI**                     |
| 🎫 Tour Tickets / Activities     | Local tours, passes, events         | **Viator (via Amadeus)**, **Eventbrite**, **Musement** |
| 🚖 Local Transport Info          | Transfers and public transport      | **Navitia**, local metro/bus APIs, **OpenRoute**       |
| 🧾 Cost Estimation               | Help users plan budget              | Combine pricing from flights, hotels, attractions      |
| 🗓️ Calendar Planner             | Visual planning by date/time        | Custom calendar builder using itinerary data           |

---

## 🔧 Planned Features

- Payment and booking simulation engine
- Chat-based budget trip planning
- Personalized trip recommendations based on preferences
- Caching and optimization for API requests

---

## 📌 Notes

- Most services rely on **freely available or freemium APIs**.
- API keys and environment setup instructions will be documented separately.
- Rate limits and usage policies of each API should be reviewed individually.
- Implementation considers both technical feasibility and AI limitations.