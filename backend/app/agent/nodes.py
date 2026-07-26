from datetime import datetime
import httpx
from app.agent.state import AgentState
from app.services.tool_wrapper import get_flights, get_hotels, get_activities

CITY_COORDINATES = {
    "DEL": {"lat": 28.6139, "lon": 77.2090, "name": "New Delhi"},
    "BOM": {"lat": 19.0760, "lon": 72.8777, "name": "Mumbai"},
    "BLR": {"lat": 12.9716, "lon": 77.5946, "name": "Bengaluru"},
    "MAA": {"lat": 13.0827, "lon": 80.2707, "name": "Chennai"},
    "CCU": {"lat": 22.5726, "lon": 88.3639, "name": "Kolkata"},
    "HYD": {"lat": 17.3850, "lon": 78.4867, "name": "Hyderabad"},
    "GOA": {"lat": 15.2993, "lon": 74.1240, "name": "Goa"},
}

def get_timestamp() -> str:
    """Returns a formatted timestamp string for logging."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_short_timestamp() -> str:
    """Returns a short time string HH:MM:SS."""
    return datetime.now().strftime("%H:%M:%S")


async def planner_node(state: AgentState) -> AgentState:
    """
    Initializes the trip planning process and logs the initial user request details.

    Why: Serves as the primary entry point node in the agent graph to establish the 
    trip parameters (origin, destination, budget) and append the starting log entry 
    to action_log.
    """
    origin = state.get("origin") or "DEL"
    destination = state.get("destination") or "GOA"
    budget_inr = state.get("budget_inr") or 15000
    start_date = state.get("start_date") or "2026-08-01"

    action_log = list(state.get("action_log") or [])
    action_logs = list(state.get("action_logs") or [])
    timestamp = get_timestamp()
    ts_short = get_short_timestamp()

    msg = f"Planning trip from {origin} to {destination}, budget ₹{budget_inr}"
    action_log.append(f"[{timestamp}] {msg}")
    action_logs.append({
        "timestamp": ts_short,
        "node": "planner",
        "status": "INFO",
        "message": msg
    })

    return {
        **state,
        "origin": origin,
        "destination": destination,
        "start_date": start_date,
        "budget_inr": budget_inr,
        "action_log": action_log,
        "action_logs": action_logs
    }


async def flight_search_node(state: AgentState) -> AgentState:
    """
    Fetches available flight options for the given route and travel date.

    Why: Queries live flight data via RapidAPI Skyscanner (falling back to cached data 
    if unavailable) using `get_flights`, updates flight fields in AgentState, and logs 
    the search outcome.
    """
    origin = state.get("origin", "")
    destination = state.get("destination", "")
    start_date = state.get("start_date", "")

    flights, flight_source, flight_log_note = await get_flights(origin, destination, start_date)

    action_log = list(state.get("action_log") or [])
    action_logs = list(state.get("action_logs") or [])
    timestamp = get_timestamp()
    ts_short = get_short_timestamp()

    if flight_source == "live":
        msg = f"Found {len(flights)} flight options (live data)"
        status = "SUCCESS"
    else:
        note_str = flight_log_note or f"Retrieved {len(flights)} flight options from local cache"
        msg = f"{note_str}"
        status = "FALLBACK" if "degradation" in (flight_log_note or "").lower() else "SUCCESS"

    action_log.append(f"[{timestamp}] {msg}")
    action_logs.append({
        "timestamp": ts_short,
        "node": "flight_search",
        "status": status,
        "message": msg
    })

    return {
        **state,
        "flights": flights,
        "flight_options": flights,
        "flight_source": flight_source,
        "flight_log_note": flight_log_note,
        "action_log": action_log,
        "action_logs": action_logs
    }


async def hotel_search_node(state: AgentState) -> AgentState:
    """
    Searches for accommodation options at the destination.

    Why: Queries hotel data using `get_hotels` (live RapidAPI Booking.com or cached fallback), 
    populates hotel options into state, and appends appropriate diagnostic audit logs.
    """
    destination = state.get("destination", "")

    hotels, hotel_source, hotel_log_note = await get_hotels(destination)

    action_log = list(state.get("action_log") or [])
    action_logs = list(state.get("action_logs") or [])
    timestamp = get_timestamp()
    ts_short = get_short_timestamp()

    if hotel_source == "live":
        msg = f"Found {len(hotels)} hotel options (live data)"
        status = "SUCCESS"
    else:
        note_str = hotel_log_note or f"Retrieved {len(hotels)} hotel options from local cache"
        msg = f"{note_str}"
        status = "FALLBACK" if "degradation" in (hotel_log_note or "").lower() else "SUCCESS"

    action_log.append(f"[{timestamp}] {msg}")
    action_logs.append({
        "timestamp": ts_short,
        "node": "hotel_search",
        "status": status,
        "message": msg
    })

    return {
        **state,
        "hotels": hotels,
        "hotel_options": hotels,
        "hotel_source": hotel_source,
        "hotel_log_note": hotel_log_note,
        "action_log": action_log,
        "action_logs": action_logs
    }


async def weather_node(state: AgentState) -> AgentState:
    """
    Fetches real-time 3-day weather forecast for destination from Open-Meteo REST API.

    Why: Provides weather insight for destination using hardcoded lat/long coordinates for 
    hub cities (DEL, BOM, BLR, MAA, CCU, HYD, GOA). If the API call fails or times out, 
    catches the error gracefully and sets weather to None so non-critical weather checks 
    never disrupt pipeline execution.
    """
    destination = (state.get("destination") or "").upper().strip()
    action_log = list(state.get("action_log") or [])
    action_logs = list(state.get("action_logs") or [])
    timestamp = get_timestamp()
    ts_short = get_short_timestamp()

    coords = CITY_COORDINATES.get(destination)
    if not coords:
        name_map = {
            "GOA": "GOA",
            "DELHI": "DEL",
            "NEW DELHI": "DEL",
            "MUMBAI": "BOM",
            "BENGALURU": "BLR",
            "BANGALORE": "BLR",
            "CHENNAI": "MAA",
            "KOLKATA": "CCU",
            "HYDERABAD": "HYD",
        }
        city_code = name_map.get(destination, "GOA")
        coords = CITY_COORDINATES.get(city_code, CITY_COORDINATES["GOA"])

    weather_result = None
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_mean"],
            "timezone": "Asia/Kolkata"
        }
        async with httpx.AsyncClient(timeout=4.0) as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                daily = data.get("daily", {})
                dates = daily.get("time", [])[:3]
                max_temps = daily.get("temperature_2m_max", [])[:3]
                min_temps = daily.get("temperature_2m_min", [])[:3]
                rain_probs = daily.get("precipitation_probability_mean", [])[:3]

                forecast_days = []
                for i in range(len(dates)):
                    rain = rain_probs[i] if i < len(rain_probs) else 10
                    cond = "Sunny & Pleasant" if rain < 20 else ("Partly Cloudy" if rain < 50 else "Scattered Showers")
                    forecast_days.append({
                        "date": dates[i],
                        "temp_max": max_temps[i] if i < len(max_temps) else 30.0,
                        "temp_min": min_temps[i] if i < len(min_temps) else 22.0,
                        "condition": cond,
                        "rain_prob": int(rain) if rain is not None else 10
                    })

                max_t = max_temps[0] if max_temps else 30.0
                summary = f"Pleasant conditions expected in {coords['name']} with high of {max_t}°C."
                weather_result = {
                    "city": coords["name"],
                    "forecast": forecast_days,
                    "summary": summary
                }
                msg = f"Checked weather for {destination}: {summary}"
                action_log.append(f"[{timestamp}] {msg}")
                action_logs.append({
                    "timestamp": ts_short,
                    "node": "weather",
                    "status": "SUCCESS",
                    "message": msg
                })
            else:
                raise RuntimeError(f"Open-Meteo status code {response.status_code}")
    except Exception:
        weather_result = None
        msg = "Weather check failed — proceeding without forecast"
        action_log.append(f"[{timestamp}] {msg}")
        action_logs.append({
            "timestamp": ts_short,
            "node": "weather",
            "status": "WARNING",
            "message": msg
        })

    return {
        **state,
        "weather": weather_result,
        "weather_info": weather_result,
        "action_log": action_log,
        "action_logs": action_logs
    }


async def activities_node(state: AgentState) -> AgentState:
    """
    Retrieves curated local attractions and food recommendations for the destination.

    Why: Queries `get_activities` from tool_wrapper to populate the `activities` state 
    field with city highlights and appends a log entry summarizing available activities.
    """
    destination = state.get("destination", "")

    activities_data, is_fallback, note = await get_activities(destination)

    action_log = list(state.get("action_log") or [])
    action_logs = list(state.get("action_logs") or [])
    timestamp = get_timestamp()
    ts_short = get_short_timestamp()

    attractions = activities_data.get("attractions", [])
    food = activities_data.get("food_recommendations", [])
    n = len(attractions) + len(food)

    if is_fallback and note:
        msg = note
    else:
        msg = f"Found {n} things to do in {destination}"

    action_log.append(f"[{timestamp}] {msg}")
    action_logs.append({
        "timestamp": ts_short,
        "node": "activities",
        "status": "FALLBACK" if is_fallback else "SUCCESS",
        "message": msg
    })

    return {
        **state,
        "activities": activities_data,
        "action_log": action_log,
        "action_logs": action_logs
    }


async def budget_check_node(state: AgentState) -> AgentState:
    """
    Evaluates combinations of flights and hotels sorted by price to optimize budget allocation.

    Why: Tries the cheapest flight + cheapest hotel combo first. If within budget_inr, 
    selects it. If over budget, iterates through next-cheapest combinations until one fits 
    or options are exhausted. If no combo fits within budget, selects the overall cheapest 
    combo and sets budget_status to 'over_budget'. Appends detailed evaluation logs.
    """
    flights = list(state.get("flights") or [])
    hotels = list(state.get("hotels") or [])
    budget_inr = state.get("budget_inr") or 15000
    action_log = list(state.get("action_log") or [])
    action_logs = list(state.get("action_logs") or [])
    timestamp = get_timestamp()
    ts_short = get_short_timestamp()

    sorted_flights = sorted(flights, key=lambda x: x.get("price_inr", 0))
    sorted_hotels = sorted(hotels, key=lambda x: x.get("total_price_inr", 0))

    if not sorted_flights or not sorted_hotels:
        selected_flight = sorted_flights[0] if sorted_flights else None
        selected_hotel = sorted_hotels[0] if sorted_hotels else None
        total_cost = (selected_flight.get("price_inr", 0) if selected_flight else 0) + \
                     (selected_hotel.get("total_price_inr", 0) if selected_hotel else 0)
        msg = "Insufficient flight or hotel options to complete budget check."
        action_log.append(f"[{timestamp}] {msg}")
        action_logs.append({
            "timestamp": ts_short,
            "node": "budget_check",
            "status": "WARNING",
            "message": msg
        })
        return {
            **state,
            "selected_flight": selected_flight,
            "selected_hotel": selected_hotel,
            "total_cost": total_cost,
            "budget_status": "over_budget",
            "is_within_budget": False,
            "action_log": action_log,
            "action_logs": action_logs
        }

    cheapest_flight = sorted_flights[0]
    cheapest_hotel = sorted_hotels[0]
    cheapest_total = cheapest_flight.get("price_inr", 0) + cheapest_hotel.get("total_price_inr", 0)

    selected_flight = None
    selected_hotel = None
    total_cost = None
    budget_status = None

    if cheapest_total <= budget_inr:
        selected_flight = cheapest_flight
        selected_hotel = cheapest_hotel
        total_cost = cheapest_total
        budget_status = "within_budget"
    else:
        exceed_amount = cheapest_total - budget_inr
        msg = f"Cheapest combo (₹{cheapest_total}) exceeds budget by ₹{exceed_amount} — trying next option"
        action_log.append(f"[{timestamp}] {msg}")
        action_logs.append({
            "timestamp": ts_short,
            "node": "budget_check",
            "status": "RETRY",
            "message": msg
        })

        found_fit = False
        for h_idx in range(len(sorted_hotels)):
            for f_idx in range(len(sorted_flights)):
                if f_idx == 0 and h_idx == 0:
                    continue
                
                candidate_flight = sorted_flights[f_idx]
                candidate_hotel = sorted_hotels[h_idx]
                combo_cost = candidate_flight.get("price_inr", 0) + candidate_hotel.get("total_price_inr", 0)

                if combo_cost <= budget_inr:
                    selected_flight = candidate_flight
                    selected_hotel = candidate_hotel
                    total_cost = combo_cost
                    budget_status = "within_budget"
                    found_fit = True
                    break
                else:
                    diff = combo_cost - budget_inr
                    fail_msg = f"Combo (₹{combo_cost}) exceeds budget by ₹{diff} — trying next option"
                    action_log.append(f"[{timestamp}] {fail_msg}")
                    action_logs.append({
                        "timestamp": ts_short,
                        "node": "budget_check",
                        "status": "RETRY",
                        "message": fail_msg
                    })
            if found_fit:
                break

        if not found_fit:
            selected_flight = cheapest_flight
            selected_hotel = cheapest_hotel
            total_cost = cheapest_total
            budget_status = "over_budget"

    flight_str = selected_flight.get("airline", "Flight")
    if selected_flight.get("flight_number"):
        flight_str += f" ({selected_flight['flight_number']})"
    hotel_str = selected_hotel.get("name", "Hotel")

    final_msg = f"Selected: {flight_str} + {hotel_str}, total ₹{total_cost} ({budget_status})"
    action_log.append(f"[{timestamp}] {final_msg}")
    action_logs.append({
        "timestamp": ts_short,
        "node": "budget_check",
        "status": "SUCCESS" if budget_status == "within_budget" else "WARNING",
        "message": final_msg
    })

    return {
        **state,
        "selected_flight": selected_flight,
        "selected_hotel": selected_hotel,
        "total_cost": total_cost,
        "budget_status": budget_status,
        "is_within_budget": (budget_status == "within_budget"),
        "action_log": action_log,
        "action_logs": action_logs
    }


async def synthesizer_node(state: AgentState) -> AgentState:
    """
    Synthesizes the overall trip recommendation into a clean plain-English summary.

    Why: Combines selected flight, hotel, budget breakdown, weather outlook, activity 
    highlights, and data provenance into a 3-4 sentence paragraph. Finalizes the action_log.
    """
    origin = state.get("origin", "")
    destination = state.get("destination", "")
    budget_inr = state.get("budget_inr", 0)
    total_cost = state.get("total_cost", 0)
    budget_status = state.get("budget_status", "within_budget")
    selected_flight = state.get("selected_flight") or {}
    selected_hotel = state.get("selected_hotel") or {}
    weather = state.get("weather")
    activities = state.get("activities") or {}
    flight_source = state.get("flight_source", "cached")
    hotel_source = state.get("hotel_source", "cached")

    action_log = list(state.get("action_log") or [])
    action_logs = list(state.get("action_logs") or [])
    timestamp = get_timestamp()
    ts_short = get_short_timestamp()

    flight_name = selected_flight.get("airline", "Flight")
    if selected_flight.get("flight_number"):
        flight_name += f" ({selected_flight['flight_number']})"
    hotel_name = selected_hotel.get("name", "Hotel")

    comparison = "within" if budget_status == "within_budget" else "over"

    sentence1 = f"Trip plan for {origin} to {destination} selects flight {flight_name} and stay at {hotel_name}."
    sentence2 = f"The estimated total cost is ₹{total_cost}, which is {comparison} your budget of ₹{budget_inr}."
    
    if weather and isinstance(weather, dict) and weather.get("summary"):
        sentence3 = f"Weather forecast for {destination}: {weather['summary']}"
    else:
        sentence3 = f"No weather forecast was available for {destination} during planning."

    # Mention 1-2 activity highlights
    attractions = activities.get("attractions", [])
    food_recs = activities.get("food_recommendations", [])
    activity_highlights = ""
    if attractions or food_recs:
        parts = []
        if attractions:
            parts.append(f"visiting {attractions[0]['name']}")
        if food_recs:
            parts.append(f"dining at {food_recs[0]['name']}")
        activity_highlights = f" Recommended experiences include {' and '.join(parts)}."

    sentence4 = f"Flight information was obtained via {flight_source} data, and hotel information via {hotel_source} data."

    final_summary = f"{sentence1} {sentence2} {sentence3}{activity_highlights} {sentence4}"

    final_msg = "Trip plan finalized"
    action_log.append(f"[{timestamp}] {final_msg}")
    action_logs.append({
        "timestamp": ts_short,
        "node": "synthesizer",
        "status": "SUCCESS",
        "message": final_msg
    })

    itinerary = {
        "title": f"Trip Plan: {origin} to {destination}",
        "dates": state.get("start_date", ""),
        "total_cost": total_cost,
        "is_within_budget": (budget_status == "within_budget"),
        "flight": selected_flight,
        "hotel": selected_hotel,
        "weather": weather,
        "activities": activities,
        "schedule": [
            {
                "day": "Day 1",
                "title": "Arrival & Check-in",
                "activities": [f"Board flight {flight_name}", f"Check in at {hotel_name}"]
            },
            {
                "day": "Day 2",
                "title": "Exploration & Local Sights",
                "activities": [
                    attractions[0]['name'] if attractions else "City Sightseeing",
                    f"Sample local cuisine at {food_recs[0]['name']}" if food_recs else "Local dining"
                ]
            }
        ]
    }

    return {
        **state,
        "final_summary": final_summary,
        "summary": final_summary,
        "itinerary": itinerary,
        "action_log": action_log,
        "action_logs": action_logs
    }

