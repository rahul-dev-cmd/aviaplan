import httpx
from typing import Dict, Any, List
from datetime import datetime, timedelta

CITY_COORDINATES = {
    "GOA": {"lat": 15.2993, "lon": 74.1240, "name": "Goa"},
    "DEL": {"lat": 28.6139, "lon": 77.2090, "name": "New Delhi"},
    "BOM": {"lat": 19.0760, "lon": 72.8777, "name": "Mumbai"},
    "BLR": {"lat": 12.9716, "lon": 77.5946, "name": "Bengaluru"},
    "MAA": {"lat": 13.0827, "lon": 80.2707, "name": "Chennai"},
    "CCU": {"lat": 22.5726, "lon": 88.3639, "name": "Kolkata"},
    "HYD": {"lat": 17.3850, "lon": 78.4867, "name": "Hyderabad"},
}

async def fetch_weather_forecast(city_code: str) -> Dict[str, Any]:
    """
    Fetches real-time weather from Open-Meteo API.
    Does not require an API key.
    """
    city_key = city_code.upper().strip() if city_code else "GOA"
    coords = CITY_COORDINATES.get(city_key, CITY_COORDINATES["GOA"])
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_probability_mean", "weathercode"],
        "timezone": "Asia/Kolkata"
    }
    
    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            res = await client.get(url, params=params)
            if res.status_code == 200:
                data = res.json()
                daily = data.get("daily", {})
                dates = daily.get("time", [])[:3]
                max_temps = daily.get("temperature_2m_max", [])[:3]
                min_temps = daily.get("temperature_2m_min", [])[:3]
                rain_probs = daily.get("precipitation_probability_mean", [])[:3]
                
                forecast_days = []
                for idx in range(len(dates)):
                    rain = rain_probs[idx] if idx < len(rain_probs) else 10
                    condition = "Sunny & Pleasant" if rain < 20 else ("Partly Cloudy" if rain < 50 else "Scattered Showers")
                    forecast_days.append({
                        "date": dates[idx],
                        "temp_max": round(max_temps[idx], 1) if idx < len(max_temps) else 31.0,
                        "temp_min": round(min_temps[idx], 1) if idx < len(min_temps) else 24.0,
                        "condition": condition,
                        "rain_prob": int(rain) if rain is not None else 10
                    })
                
                return {
                    "city": coords["name"],
                    "forecast": forecast_days,
                    "summary": f"Pleasant coastal conditions expected in {coords['name']} with high of {max_temps[0]}°C.",
                    "is_mock": False
                }
    except Exception as e:
        # Fallback to realistic mock weather if Open-Meteo times out
        pass
    
    # Mock Weather Fallback
    today = datetime.now()
    return {
        "city": coords["name"],
        "forecast": [
            {
                "date": (today + timedelta(days=i)).strftime("%Y-%m-%d"),
                "temp_max": 31.5 - i * 0.5,
                "temp_min": 24.0,
                "condition": "Partly Cloudy" if i == 1 else "Sunny & Breezy",
                "rain_prob": 15 + i * 5
            }
            for i in range(3)
        ],
        "summary": f"Warm and sunny conditions expected across {coords['name']}.",
        "is_mock": True
    }
