import json
import os
from typing import List, Dict, Any, Tuple

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FLIGHTS_FILE = os.path.join(DATA_DIR, "mock_flights.json")
HOTELS_FILE = os.path.join(DATA_DIR, "mock_hotels.json")

def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_mock_flights(origin: str, destination: str) -> Tuple[List[Dict[str, Any]], bool, str]:
    """
    Returns (flights_list, is_degraded, fallback_note)
    If exact origin+destination match exists, returns it.
    If not, degrades gracefully to a representative hub route rather than returning empty.
    """
    all_flights = load_json_file(FLIGHTS_FILE)
    origin_clean = origin.upper().strip() if origin else "DEL"
    dest_clean = destination.upper().strip() if destination else "GOA"
    
    # 1. Exact match search
    exact_matches = [
        f for f in all_flights
        if f["origin"].upper() == origin_clean and f["destination"].upper() == dest_clean
    ]
    if exact_matches:
        exact_matches.sort(key=lambda x: x["price_inr"])
        return exact_matches, False, ""
    
    # 2. Destination match search (e.g. any flight to GOA)
    dest_matches = [f for f in all_flights if f["destination"].upper() == dest_clean]
    if dest_matches:
        adapted_flights = []
        for f in dest_matches:
            item = dict(f)
            item["origin"] = origin_clean
            adapted_flights.append(item)
        adapted_flights.sort(key=lambda x: x["price_inr"])
        note = f"Route {origin_clean}->{dest_clean} not explicitly seeded in mock DB; matched destination {dest_clean} using representative hub flights."
        return adapted_flights, True, note

    # 3. Universal Fallback: return default DEL->GOA set labeled for the requested route
    default_flights = [f for f in all_flights if f["origin"] == "DEL" and f["destination"] == "GOA"]
    if not default_flights:
        default_flights = all_flights[:3]
    
    adapted_flights = []
    for f in default_flights:
        item = dict(f)
        item["origin"] = origin_clean
        item["destination"] = dest_clean
        adapted_flights.append(item)
    
    adapted_flights.sort(key=lambda x: x["price_inr"])
    note = f"Route {origin_clean}->{dest_clean} outside standard seed set; degraded gracefully to representative distance route pricing."
    return adapted_flights, True, note

def get_mock_hotels(destination: str) -> Tuple[List[Dict[str, Any]], bool, str]:
    """
    Returns (hotels_list, is_degraded, fallback_note)
    """
    all_hotels = load_json_file(HOTELS_FILE)
    dest_clean = destination.upper().strip() if destination else "GOA"
    
    # Check exact location match
    matches = [h for h in all_hotels if dest_clean in h["location"].upper() or dest_clean in h["id"].upper()]
    if matches:
        matches.sort(key=lambda x: x["total_price_inr"])
        return matches, False, ""
    
    # Fallback to GOA hotels adapted for requested city
    default_hotels = [h for h in all_hotels if "GOA" in h["id"].upper()]
    if not default_hotels:
        default_hotels = all_hotels[:3]
    
    adapted_hotels = []
    for h in default_hotels:
        item = dict(h)
        item["location"] = f"Central {destination.title()}"
        adapted_hotels.append(item)
    
    adapted_hotels.sort(key=lambda x: x["total_price_inr"])
    note = f"Hotels for {dest_clean} unseeded; degraded gracefully to representative hotel accommodation rates."
    return adapted_hotels, True, note
