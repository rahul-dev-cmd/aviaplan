# AviaPlan Project Context

PROJECT: AviaPlan — an autonomous trip-planning agent built for an Agentic AI hackathon.

WHAT IT DOES:
User gives one high-level instruction (e.g. "Plan a weekend trip to Goa under ₹15,000, leaving Friday"). An AI agent autonomously:
1. Breaks the instruction into sub-tasks (flights, hotels, weather, budget check)
2. Calls tools to gather real data (RapidAPI for flights/hotels, Open-Meteo for weather)
3. If a live API call fails, silently falls back to local mock data — this failure handling is a core, visible feature, not an edge case
4. Checks combined cost against budget; if over, retries with the next-cheapest combo and logs why
5. Produces a final itinerary + plain-English summary
6. Shows a transparent, timestamped action log of every step/decision it took — this log is a first-class UI element, not a debug output

ARCHITECTURE:
- Backend: FastAPI (Python), deployed on Render
- Agent orchestration: LangGraph — state graph with nodes: planner → flight_search → hotel_search → weather → budget_check → synthesizer
- LLM: Groq (Llama 3.3-70b-versatile)
- Data sources: RapidAPI (Skyscanner/Booking.com) as primary, local JSON mock data as fallback on any API failure/timeout
- Frontend: Next.js 15 (app router), deployed on Vercel
- No database needed — mock data is static JSON files, no user accounts/persistence required for this build

DESIGN DIRECTION:
- Warm cream/off-white background, charcoal text, sky-blue/burnt-orange accent, light mode
- Boarding-pass style card for final itinerary (perforated edge, barcode block, labeled field grid)
- Loading state: animated takeoff sequence (plane accelerates on a runway, pitches up, climbs off-screen)
