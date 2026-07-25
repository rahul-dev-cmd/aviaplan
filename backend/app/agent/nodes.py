import os
import re
import json
from datetime import datetime, timedelta
from typing import Dict, Any
from app.agent.state import AgentState
from app.services.tool_wrapper import (
    execute_flight_search_tool,
    execute_hotel_search_tool,
    execute_weather_tool,
    get_timestamp
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def planner_node(state: AgentState) -> Dict[str, Any]:
    query = state.get("query", "")
    action_logs = list(state.get("action_logs", []))
    
    action_logs.append({
        "timestamp": get_timestamp(),
        "node": "planner",
        "status": "INFO",
        "message": f"Agent initialized with user request: '{query}'"
    })

    # Heuristic parsing fallback for fast, reliable extraction
    origin = state.get("origin")
    destination = state.get("destination")
    max_budget = state.get("max_budget")
    
    # 1. Parse Origin (e.g. from Delhi, DEL, from Mumbai, BOM, from Bangalore, BLR)
    if not origin:
        if re.search(r'\b(mumbai|bom)\b', query, re.IGNORECASE):
            origin = "BOM"
        elif re.search(r'\b(bangalore|bengaluru|blr)\b', query, re.IGNORECASE):
            origin = "BLR"
        elif re.search(r'\b(chennai|maa)\b', query, re.IGNORECASE):
            origin = "MAA"
        elif re.search(r'\b(kolkata|ccu)\b', query, re.IGNORECASE):
            origin = "CCU"
        elif re.search(r'\b(hyderabad|hyd)\b', query, re.IGNORECASE):
            origin = "HYD"
        else:
            origin = "DEL"

    # 2. Parse Destination (e.g. Goa, Mumbai, Delhi)
    if not destination:
        if re.search(r'\b(goa)\b', query, re.IGNORECASE):
            destination = "GOA"
        elif re.search(r'\b(mumbai|bom)\b', query, re.IGNORECASE):
            destination = "BOM"
        elif re.search(r'\b(delhi|del)\b', query, re.IGNORECASE):
            destination = "DEL"
        elif re.search(r'\b(bangalore|bengaluru|blr)\b', query, re.IGNORECASE):
            destination = "BLR"
        elif re.search(r'\b(hyderabad|hyd)\b', query, re.IGNORECASE):
            destination = "HYD"
        else:
            destination = "GOA"

    # 3. Parse Budget
    if not max_budget or max_budget <= 0:
        budget_match = re.search(r'(?:under|budget|below|₹|\bRs\.?)\s*([\d,]+)', query, re.IGNORECASE)
        if budget_match:
            try:
                max_budget = float(budget_match.group(1).replace(',', ''))
            except ValueError:
                max_budget = 15000.0
        else:
            max_budget = 15000.0

    # 4. Dates
    today = datetime.now()
    # Find next Friday
    days_until_friday = (4 - today.weekday()) % 7
    if days_until_friday == 0:
        days_until_friday = 7
    start_dt = today + timedelta(days=days_until_friday)
    end_dt = start_dt + timedelta(days=2)
    
    start_date = state.get("start_date") or start_dt.strftime("%Y-%m-%d")
    end_date = state.get("end_date") or end_dt.strftime("%Y-%m-%d")

    action_logs.append({
        "timestamp": get_timestamp(),
        "node": "planner",
        "status": "SUCCESS",
        "message": f"Decomposed query into sub-tasks: [1] Search flights ({origin}➔{destination}), [2] Search hotels ({destination}), [3] Check 3-day weather forecast, [4] Verify budget constraint ≤ ₹{max_budget:,.0f}."
    })

    return {
        "origin": origin,
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "max_budget": max_budget,
        "flight_index": 0,
        "hotel_index": 0,
        "action_logs": action_logs
    }


async def flight_search_node(state: AgentState) -> Dict[str, Any]:
    origin = state["origin"]
    destination = state["destination"]
    start_date = state["start_date"]
    
    flights, logs = await execute_flight_search_tool(origin, destination, start_date)
    current_logs = list(state.get("action_logs", [])) + logs
    
    return {
        "flight_options": flights,
        "action_logs": current_logs
    }


async def hotel_search_node(state: AgentState) -> Dict[str, Any]:
    destination = state["destination"]
    
    hotels, logs = await execute_hotel_search_tool(destination)
    current_logs = list(state.get("action_logs", [])) + logs
    
    return {
        "hotel_options": hotels,
        "action_logs": current_logs
    }


async def weather_node(state: AgentState) -> Dict[str, Any]:
    destination = state["destination"]
    
    weather_data, logs = await execute_weather_tool(destination)
    current_logs = list(state.get("action_logs", [])) + logs
    
    return {
        "weather_info": weather_data,
        "action_logs": current_logs
    }


async def budget_check_node(state: AgentState) -> Dict[str, Any]:
    flight_options = state.get("flight_options", [])
    hotel_options = state.get("hotel_options", [])
    max_budget = state.get("max_budget", 15000.0)
    current_logs = list(state.get("action_logs", []))
    
    if not flight_options or not hotel_options:
        current_logs.append({
            "timestamp": get_timestamp(),
            "node": "budget_check",
            "status": "WARNING",
            "message": "Insufficient flight/hotel data to perform budget evaluation."
        })
        return {
            "selected_flight": None,
            "selected_hotel": None,
            "total_cost": 0.0,
            "is_within_budget": False,
            "action_logs": current_logs
        }

    # Evaluate combinations from cheapest to premium
    best_combo = None
    within_budget_combo = None
    
    current_logs.append({
        "timestamp": get_timestamp(),
        "node": "budget_check",
        "status": "INFO",
        "message": f"Evaluating travel combinations against max target budget of ₹{max_budget:,.0f}..."
    })

    # Sort candidates by price
    sorted_flights = sorted(flight_options, key=lambda x: x["price_inr"])
    sorted_hotels = sorted(hotel_options, key=lambda x: x["total_price_inr"])

    for f_idx, flight in enumerate(sorted_flights):
        for h_idx, hotel in enumerate(sorted_hotels):
            total = flight["price_inr"] + hotel["total_price_inr"]
            if total <= max_budget:
                within_budget_combo = (flight, hotel, total)
                current_logs.append({
                    "timestamp": get_timestamp(),
                    "node": "budget_check",
                    "status": "SUCCESS",
                    "message": f"Optimal combination verified within budget: {flight['airline']} ({flight['flight_number']}) ₹{flight['price_inr']:,.0f} + {hotel['name']} ₹{hotel['total_price_inr']:,.0f} = Total ₹{total:,.0f} (Savings: ₹{max_budget - total:,.0f})."
                })
                break
            else:
                current_logs.append({
                    "timestamp": get_timestamp(),
                    "node": "budget_check",
                    "status": "RETRY",
                    "message": f"Combination rejected (₹{total:,.0f} > ₹{max_budget:,.0f}): {flight['airline']} + {hotel['name']}. Trying lower tier combination..."
                })
        if within_budget_combo:
            break

    if within_budget_combo:
        flight, hotel, total = within_budget_combo
        return {
            "selected_flight": flight,
            "selected_hotel": hotel,
            "total_cost": total,
            "is_within_budget": True,
            "action_logs": current_logs
        }
    
    # If no combination fits under budget, pick cheapest available combo & flag budget breach clearly
    cheapest_flight = sorted_flights[0]
    cheapest_hotel = sorted_hotels[0]
    min_total = cheapest_flight["price_inr"] + cheapest_hotel["total_price_inr"]
    
    current_logs.append({
        "timestamp": get_timestamp(),
        "node": "budget_check",
        "status": "WARNING",
        "message": f"No combination strictly under ₹{max_budget:,.0f} found. Selected best available budget package at ₹{min_total:,.0f} (Exceeds target by ₹{min_total - max_budget:,.0f})."
    })
    
    return {
        "selected_flight": cheapest_flight,
        "selected_hotel": cheapest_hotel,
        "total_cost": min_total,
        "is_within_budget": False,
        "action_logs": current_logs
    }


async def synthesizer_node(state: AgentState) -> Dict[str, Any]:
    origin = state["origin"]
    destination = state["destination"]
    start_date = state["start_date"]
    end_date = state["end_date"]
    total_cost = state.get("total_cost", 0.0)
    is_within_budget = state.get("is_within_budget", True)
    flight = state.get("selected_flight") or {}
    hotel = state.get("selected_hotel") or {}
    weather = state.get("weather_info") or {}
    current_logs = list(state.get("action_logs", []))

    summary = (
        f"Trip plan for {origin} ➔ {destination} ({start_date} to {end_date}) generated successfully. "
        f"Fly with {flight.get('airline', 'Airline')} ({flight.get('flight_number', 'N/A')}) for ₹{flight.get('price_inr', 0):,.0f} "
        f"and stay at {hotel.get('name', 'Hotel')} ({hotel.get('location', destination)}) for ₹{hotel.get('total_price_inr', 0):,.0f}. "
        f"Total cost is ₹{total_cost:,.0f} ({'within' if is_within_budget else 'over'} your target budget)."
    )

    itinerary = {
        "title": f"Weekend Getaway: {origin} to {destination}",
        "dates": f"{start_date} - {end_date}",
        "total_cost": total_cost,
        "is_within_budget": is_within_budget,
        "flight": flight,
        "hotel": hotel,
        "weather": weather,
        "schedule": [
            {
                "day": "Day 1 (Friday)",
                "title": "Arrival & Sunset Chill",
                "activities": [
                    f"Board flight {flight.get('flight_number', '')} from {origin} at {flight.get('departure_time', '08:00')}.",
                    f"Check in at {hotel.get('name', 'Hotel')} in {hotel.get('location', destination)}.",
                    "Enjoy local seafood or beachside evening sunset."
                ]
            },
            {
                "day": "Day 2 (Saturday)",
                "title": "Exploration & Coastal Sights",
                "activities": [
                    "Breakfast at resort.",
                    "Sightseeing & water activities based on weather recommendations.",
                    "Dinner at popular local dining spot."
                ]
            },
            {
                "day": "Day 3 (Sunday)",
                "title": "Relaxation & Departure",
                "activities": [
                    "Morning cafe visit & souvenir shopping.",
                    "Check out from hotel.",
                    "Head to airport for return journey."
                ]
            }
        ]
    }

    current_logs.append({
        "timestamp": get_timestamp(),
        "node": "synthesizer",
        "status": "SUCCESS",
        "message": "Synthesized final trip summary, boarding pass dataset, and day-by-day itinerary."
    })

    return {
        "summary": summary,
        "itinerary": itinerary,
        "action_logs": current_logs
    }
