from typing import TypedDict

class AgentState(TypedDict, total=False):
    origin: str
    destination: str
    start_date: str
    budget_inr: int
    flights: list
    flight_source: str
    flight_log_note: str | None
    hotels: list
    hotel_source: str
    hotel_log_note: str | None
    weather: dict | None
    activities: dict | None
    selected_flight: dict | None
    selected_hotel: dict | None
    total_cost: int | None
    budget_status: str | None  # "within_budget" or "over_budget"
    action_log: list[str]  # timestamped human-readable steps
    final_summary: str | None

    # Optional fields for backward compatibility with frontend/routes
    query: str
    end_date: str
    max_budget: float
    is_within_budget: bool
    weather_info: dict | None
    summary: str
    itinerary: dict
    action_logs: list
