# 🌍 Travel Services Aggregator

This project integrates various free and commercial APIs to offer users a comprehensive and budget-aware travel planning platform. From checking flights and hotels to simulating bookings and suggesting itineraries — it's designed to cover every phase of travel planning.

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

| Feature                          | Why It’s Useful                     | Suggested APIs / Sources                              |
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