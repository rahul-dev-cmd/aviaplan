from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TripRequest(BaseModel):
    query: Optional[str] = Field(None, description="High level natural language prompt, e.g. 'Plan a trip to Goa under 15000'")
    origin: Optional[str] = Field(None, description="Departure airport city (e.g., DEL, BOM, BLR)")
    destination: Optional[str] = Field(None, description="Arrival airport city (e.g., GOA, DEL, BOM)")
    start_date: Optional[str] = Field(None, description="Travel start date YYYY-MM-DD")
    end_date: Optional[str] = Field(None, description="Travel end date YYYY-MM-DD")
    max_budget: Optional[float] = Field(None, description="Maximum total budget in INR")
    budget_inr: Optional[float] = Field(None, description="Budget in INR (alias for max_budget)")

class ActionLogItem(BaseModel):
    timestamp: str
    node: str
    status: str  # "INFO", "SUCCESS", "FALLBACK", "WARNING", "RETRY"
    message: str
    details: Optional[Dict[str, Any]] = None

class FlightOption(BaseModel):
    id: str
    airline: str
    flight_number: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    duration: str
    price_inr: float
    is_mock: bool = True
    source_label: str = "Mock Data Store"

class HotelOption(BaseModel):
    id: str
    name: str
    location: str
    rating: float
    price_per_night_inr: float
    total_price_inr: float
    nights: int = 2
    amenities: List[str] = []
    image_url: Optional[str] = None
    is_mock: bool = True
    source_label: str = "Mock Data Store"

class WeatherForecastDay(BaseModel):
    date: str
    temp_max: float
    temp_min: float
    condition: str
    rain_prob: int

class WeatherInfo(BaseModel):
    city: str
    forecast: List[WeatherForecastDay]
    summary: str
    is_mock: bool = False

class TripResponse(BaseModel):
    success: bool
    origin: str
    destination: str
    start_date: str
    end_date: str
    max_budget: float
    total_cost: float
    is_within_budget: bool
    selected_flight: Optional[FlightOption] = None
    selected_hotel: Optional[HotelOption] = None
    weather_info: Optional[WeatherInfo] = None
    summary: str
    itinerary: Dict[str, Any] = {}
    action_logs: List[ActionLogItem] = []
    action_log: List[ActionLogItem] = []
