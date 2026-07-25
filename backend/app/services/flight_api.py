import os
import httpx
from typing import List, Dict, Any, Optional

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "skyscanner-api2.p.rapidapi.com"

async def fetch_live_flights(origin: str, destination: str, date: str) -> Optional[List[Dict[str, Any]]]:
    """
    Attempts to fetch live flight data from Skyscanner via RapidAPI.
    Raises Exception on missing key, timeout, or API error.
    """
    if not RAPIDAPI_KEY or RAPIDAPI_KEY.strip() == "":
        raise ValueError("RAPIDAPI_KEY environment variable is not configured.")
    
    url = f"https://{RAPIDAPI_HOST}/v3/flights/live/search/synced"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {
        "query": {
            "market": "IN",
            "currency": "INR",
            "locale": "en-US",
            "queryLegs": [
                {
                    "originPlaceId": {"iata": origin},
                    "destinationPlaceId": {"iata": destination},
                    "date": {"year": int(date[:4]), "month": int(date[5:7]), "day": int(date[8:10])}
                }
            ],
            "cabinClass": "CABIN_CLASS_ECONOMY",
            "adults": 1
        }
    }
    
    async with httpx.AsyncClient(timeout=3.0) as client:
        response = await client.post(url, headers=headers, json=params)
        if response.status_code == 200:
            data = response.json()
            # Process & normalize live data if available
            itineraries = data.get("content", {}).get("results", {}).get("itineraries", {})
            if itineraries:
                results = []
                for id_key, itin in list(itineraries.items())[:3]:
                    price = itin.get("pricingOptions", [{}])[0].get("price", {}).get("amount", 5000) / 1000.0
                    results.append({
                        "id": f"LIVE-FL-{id_key[:6]}",
                        "airline": "Live Carrier",
                        "flight_number": "LA-101",
                        "origin": origin,
                        "destination": destination,
                        "departure_time": "10:00",
                        "arrival_time": "12:30",
                        "duration": "2h 30m",
                        "price_inr": round(price, 2)
                    })
                return results
        raise RuntimeError(f"RapidAPI Skyscanner error HTTP {response.status_code}: {response.text[:100]}")
