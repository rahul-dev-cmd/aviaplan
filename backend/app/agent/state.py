from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    query: str
    origin: str
    destination: str
    start_date: str
    end_date: str
    max_budget: float
    flight_options: List[Dict[str, Any]]
    hotel_options: List[Dict[str, Any]]
    weather_info: Optional[Dict[str, Any]]
    selected_flight: Optional[Dict[str, Any]]
    selected_hotel: Optional[Dict[str, Any]]
    total_cost: float
    is_within_budget: bool
    flight_index: int
    hotel_index: int
    summary: str
    itinerary: Dict[str, Any]
    action_logs: List[Dict[str, Any]]
