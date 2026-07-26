import json
import os
from typing import List, Dict, Any, Tuple

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
FLIGHTS_FILE = os.path.join(DATA_DIR, "mock_flights.json")
HOTELS_FILE = os.path.join(DATA_DIR, "mock_hotels.json")
ACTIVITIES_FILE = os.path.join(DATA_DIR, "mock_activities.json")

def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def get_mock_flights(origin: str, destination: str) -> Tuple[List[Dict[str, Any]], bool, str]:
    """
    Returns (flights_list, is_generic_fallback, reason)
    1. Filters JSON by exact origin + destination match.
    2. If no direct data exists for origin-destination, falls back to a representative proxy route (DEL-GOA or BOM-GOA),
       adapts the returned objects to the requested origin/destination, and sets is_generic_fallback=True with explicit reason.
    """
    all_flights = load_json_file(FLIGHTS_FILE)
    orig_clean = origin.upper().strip() if origin else "DEL"
    dest_clean = destination.upper().strip() if destination else "GOA"
    
    # 1. Exact match filter
    exact_matches = [
        f for f in all_flights
        if f["origin"].upper() == orig_clean and f["destination"].upper() == dest_clean
    ]
    if exact_matches:
        exact_matches.sort(key=lambda x: x["price_inr"])
        return exact_matches, False, ""

    # 2. Destination match filter (e.g. any flight to GOA or DEL)
    dest_matches = [f for f in all_flights if f["destination"].upper() == dest_clean]
    if dest_matches:
        adapted_flights = []
        for f in dest_matches:
            item = dict(f)
            item["origin"] = orig_clean
            adapted_flights.append(item)
        adapted_flights.sort(key=lambda x: x["price_inr"])
        reason = f"No direct data for {orig_clean}-{dest_clean}, showing representative pricing for a comparable route"
        return adapted_flights, True, reason

    # 3. Proxy route fallback (default to DEL-GOA)
    proxy_flights = [f for f in all_flights if f["origin"] == "DEL" and f["destination"] == "GOA"]
    if not proxy_flights:
        proxy_flights = all_flights[:3]

    adapted_flights = []
    for f in proxy_flights:
        item = dict(f)
        item["origin"] = orig_clean
        item["destination"] = dest_clean
        adapted_flights.append(item)
    
    adapted_flights.sort(key=lambda x: x["price_inr"])
    reason = f"No direct data for {orig_clean}-{dest_clean}, showing representative pricing for a comparable route"
    return adapted_flights, True, reason


def get_mock_hotels(destination: str) -> Tuple[List[Dict[str, Any]], bool, str]:
    """
    Returns (hotels_list, is_generic_fallback, reason)
    1. Filters JSON by exact destination city match.
    2. If no direct hotel data exists for destination, falls back to a proxy city (GOA), adapts the location area,
       and sets is_generic_fallback=True with explicit reason.
    """
    all_hotels = load_json_file(HOTELS_FILE)
    dest_clean = destination.upper().strip() if destination else "GOA"

    # 1. Exact match filter
    exact_matches = [
        h for h in all_hotels
        if dest_clean in h.get("location_area", "").upper()
        or dest_clean in h.get("location", "").upper()
        or dest_clean in h.get("id", "").upper()
    ]
    if exact_matches:
        exact_matches.sort(key=lambda x: x["total_price_inr"])
        return exact_matches, False, ""

    # 2. Fallback to GOA hotels adapted for requested destination
    proxy_hotels = [h for h in all_hotels if "GOA" in h.get("id", "").upper()]
    if not proxy_hotels:
        proxy_hotels = all_hotels[:4]

    adapted_hotels = []
    for h in proxy_hotels:
        item = dict(h)
        item["location_area"] = f"Central {dest_clean.title()}"
        item["location"] = f"Central {dest_clean.title()}"
        adapted_hotels.append(item)

    adapted_hotels.sort(key=lambda x: x["total_price_inr"])
    reason = f"No direct hotel data for {dest_clean}, showing representative pricing for a comparable city"
    return adapted_hotels, True, reason


def get_mock_activities(destination: str) -> Tuple[Dict[str, Any], bool, str]:
    """
    Returns (activities_dict, is_generic_fallback, reason)
    1. Matches JSON entry by city_code or city_name.
    2. If no direct match exists for destination, falls back to GOA activities adapted for destination,
       setting is_generic_fallback=True with explicit reason.
    """
    all_activities = load_json_file(ACTIVITIES_FILE)
    dest_clean = destination.upper().strip() if destination else "GOA"

    # 1. Exact match by city_code or city_name
    for act in all_activities:
        code = act.get("city_code", "").upper()
        name = act.get("city_name", "").upper()
        if dest_clean == code or dest_clean == name or dest_clean in name:
            return act, False, ""

    # 2. Fallback to proxy city (default GOA or first entry)
    proxy = None
    for act in all_activities:
        if act.get("city_code") == "GOA":
            proxy = dict(act)
            break
    if not proxy and all_activities:
        proxy = dict(all_activities[0])

    if proxy:
        adapted = dict(proxy)
        adapted["city_code"] = dest_clean
        adapted["city_name"] = dest_clean.title()
        reason = f"No direct activities data for {dest_clean}, showing representative experiences for a comparable destination"
        return adapted, True, reason

    return {
        "city_code": dest_clean,
        "city_name": dest_clean.title(),
        "attractions": [
            {
                "name": f"Central {dest_clean.title()} Sightseeing",
                "category": "Culture",
                "short_description": f"Explore popular landmark sights in {dest_clean.title()}."
            }
        ],
        "food_recommendations": [
            {
                "name": f"Local {dest_clean.title()} Cuisine",
                "cuisine_type": "Regional",
                "short_description": f"Sample authentic regional dishes at top-rated local dining spots."
            }
        ]
    }, True, f"No direct activities data for {dest_clean}"

