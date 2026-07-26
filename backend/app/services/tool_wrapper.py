from datetime import datetime
from typing import Tuple, List, Dict, Any, Optional
from app.services.flight_api import fetch_live_flights
from app.services.hotel_api import fetch_live_hotels
from app.services.weather_api import fetch_weather_forecast
from app.services.mock_data import get_mock_flights, get_mock_hotels, get_mock_activities

def get_timestamp() -> str:
    return datetime.now().strftime("%H:%M:%S")

async def get_flights(origin: str, destination: str, start_date: str) -> Tuple[List[Dict[str, Any]], str, Optional[str]]:
    """
    Fetches flights for origin -> destination on start_date.
    Tries live RapidAPI first. If live API fails or key is missing, falls back to local cached mock data.
    Returns (flights_list, source, flight_log_note).
    """
    try:
        live_flights = await fetch_live_flights(origin, destination, start_date)
        if live_flights:
            for f in live_flights:
                f["is_mock"] = False
                f["source_label"] = "RapidAPI Skyscanner Live"
            return live_flights, "live", None
    except Exception:
        pass

    mock_flights, is_degraded, note = get_mock_flights(origin, destination)
    for f in mock_flights:
        f["is_mock"] = True
        f["source_label"] = "Local Verified Mock Store"

    log_note = note if (is_degraded and note) else f"Retrieved {len(mock_flights)} flight options from local cache"
    return mock_flights, "cached", log_note

async def get_hotels(destination: str) -> Tuple[List[Dict[str, Any]], str, Optional[str]]:
    """
    Fetches hotels for destination city.
    Tries live RapidAPI Booking.com first. On failure, falls back to local cached mock data.
    Returns (hotels_list, source, hotel_log_note).
    """
    try:
        live_hotels = await fetch_live_hotels(destination)
        if live_hotels:
            for h in live_hotels:
                h["is_mock"] = False
                h["source_label"] = "RapidAPI Booking.com Live"
            return live_hotels, "live", None
    except Exception:
        pass

    mock_hotels, is_degraded, note = get_mock_hotels(destination)
    for h in mock_hotels:
        h["is_mock"] = True
        h["source_label"] = "Local Verified Mock Store"

    log_note = note if (is_degraded and note) else f"Retrieved {len(mock_hotels)} hotel options from local cache"
    return mock_hotels, "cached", log_note

async def get_activities(destination: str) -> Tuple[Dict[str, Any], bool, str]:
    """
    Retrieves curated attractions and food recommendations for destination.
    Returns (activities_data, is_fallback, note).
    """
    return get_mock_activities(destination)



async def execute_flight_search_tool(origin: str, destination: str, date: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Executes flight tool: tries live RapidAPI first.
    On failure/missing key, silently falls back to local mock data & logs explicit audit log.
    Returns (flight_list, action_logs).
    """
    logs = []
    t_start = get_timestamp()
    logs.append({
        "timestamp": t_start,
        "node": "flight_search",
        "status": "INFO",
        "message": f"Initiating live flight query for route {origin} ➔ {destination} via RapidAPI Skyscanner..."
    })
    
    try:
        live_flights = await fetch_live_flights(origin, destination, date)
        if live_flights:
            for f in live_flights:
                f["is_mock"] = False
                f["source_label"] = "RapidAPI Skyscanner Live"
            logs.append({
                "timestamp": get_timestamp(),
                "node": "flight_search",
                "status": "SUCCESS",
                "message": f"Successfully retrieved {len(live_flights)} live flight options from RapidAPI."
            })
            return live_flights, logs
    except Exception as err:
        reason = str(err)
        if "RAPIDAPI_KEY" in reason:
            fail_desc = "RapidAPI key not provided in environment."
        else:
            fail_desc = f"API connection error/timeout ({reason[:60]})."
            
        logs.append({
            "timestamp": get_timestamp(),
            "node": "flight_search",
            "status": "FALLBACK",
            "message": f"⚡ LIVE API FALLBACK TRIGGERED: {fail_desc} Switching seamlessly to local mock flight store."
        })
    
    # Mock data fallback (with route degradation handling if unseeded)
    mock_flights, is_degraded, note = get_mock_flights(origin, destination)
    for f in mock_flights:
        f["is_mock"] = True
        f["source_label"] = "Local Verified Mock Store"
    
    if is_degraded:
        logs.append({
            "timestamp": get_timestamp(),
            "node": "flight_search",
            "status": "WARNING",
            "message": f"ℹ️ GEOGRAPHIC DEGRADATION: {note}"
        })
    
    logs.append({
        "timestamp": get_timestamp(),
        "node": "flight_search",
        "status": "SUCCESS",
        "message": f"Retrieved {len(mock_flights)} flight candidates from mock dataset (Prices: ₹{mock_flights[0]['price_inr']} - ₹{mock_flights[-1]['price_inr']})."
    })
    return mock_flights, logs


async def execute_hotel_search_tool(destination: str) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Executes hotel tool: tries live RapidAPI first.
    On failure/missing key, silently falls back to local mock data & logs explicit audit log.
    Returns (hotel_list, action_logs).
    """
    logs = []
    logs.append({
        "timestamp": get_timestamp(),
        "node": "hotel_search",
        "status": "INFO",
        "message": f"Initiating hotel search for destination '{destination}' via RapidAPI Booking.com..."
    })
    
    try:
        live_hotels = await fetch_live_hotels(destination)
        if live_hotels:
            for h in live_hotels:
                h["is_mock"] = False
                h["source_label"] = "RapidAPI Booking.com Live"
            logs.append({
                "timestamp": get_timestamp(),
                "node": "hotel_search",
                "status": "SUCCESS",
                "message": f"Retrieved {len(live_hotels)} live hotel options."
            })
            return live_hotels, logs
    except Exception as err:
        reason = str(err)
        fail_desc = "RapidAPI key missing or endpoint timeout." if "RAPIDAPI_KEY" in reason else f"API issue ({reason[:50]})."
        logs.append({
            "timestamp": get_timestamp(),
            "node": "hotel_search",
            "status": "FALLBACK",
            "message": f"⚡ LIVE API FALLBACK TRIGGERED: {fail_desc} Switching seamlessly to local mock hotel store."
        })

    # Mock hotel fallback (with location degradation handling if unseeded)
    mock_hotels, is_degraded, note = get_mock_hotels(destination)
    for h in mock_hotels:
        h["is_mock"] = True
        h["source_label"] = "Local Verified Mock Store"

    if is_degraded:
        logs.append({
            "timestamp": get_timestamp(),
            "node": "hotel_search",
            "status": "WARNING",
            "message": f"ℹ️ LOCATION DEGRADATION: {note}"
        })

    logs.append({
        "timestamp": get_timestamp(),
        "node": "hotel_search",
        "status": "SUCCESS",
        "message": f"Retrieved {len(mock_hotels)} hotel properties from mock dataset (Nightly: ₹{mock_hotels[0]['price_per_night_inr']} - ₹{mock_hotels[-1]['price_per_night_inr']})."
    })
    return mock_hotels, logs


async def execute_weather_tool(destination: str) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Fetches destination weather forecast from Open-Meteo REST API.
    Returns (weather_info, action_logs).
    """
    logs = []
    logs.append({
        "timestamp": get_timestamp(),
        "node": "weather",
        "status": "INFO",
        "message": f"Querying Open-Meteo public REST API for 3-day meteorological forecast in '{destination}'..."
    })
    
    weather_data = await fetch_weather_forecast(destination)
    if weather_data.get("is_mock"):
        logs.append({
            "timestamp": get_timestamp(),
            "node": "weather",
            "status": "FALLBACK",
            "message": "Open-Meteo REST service unreachable; used offline climatological baseline."
        })
    else:
        logs.append({
            "timestamp": get_timestamp(),
            "node": "weather",
            "status": "SUCCESS",
            "message": f"Successfully retrieved live weather for {weather_data['city']}: {weather_data['summary']}"
        })
    
    return weather_data, logs
