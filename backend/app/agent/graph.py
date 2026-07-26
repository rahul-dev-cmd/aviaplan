from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import (
    planner_node,
    flight_search_node,
    hotel_search_node,
    weather_node,
    activities_node,
    budget_check_node,
    synthesizer_node
)

def create_trip_planner_graph():
    """
    Constructs and compiles the linear LangGraph StateGraph workflow.

    Sequence:
    planner_node → flight_search_node → hotel_search_node → weather_node →
    activities_node → budget_check_node → synthesizer_node → END
    """
    workflow = StateGraph(AgentState)

    # 1. Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("flight_search", flight_search_node)
    workflow.add_node("hotel_search", hotel_search_node)
    workflow.add_node("weather", weather_node)
    workflow.add_node("activities", activities_node)
    workflow.add_node("budget_check", budget_check_node)
    workflow.add_node("synthesizer", synthesizer_node)

    # 2. Wire linear edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "flight_search")
    workflow.add_edge("flight_search", "hotel_search")
    workflow.add_edge("hotel_search", "weather")
    workflow.add_edge("weather", "activities")
    workflow.add_edge("activities", "budget_check")
    workflow.add_edge("budget_check", "synthesizer")
    workflow.add_edge("synthesizer", END)

    return workflow.compile()

# Global compiled graph instance
trip_planner_graph = create_trip_planner_graph()


async def run_trip_planner(
    origin: str = "DEL",
    destination: str = "GOA",
    start_date: str = "2026-08-01",
    budget_inr: int = 15000,
    **kwargs
) -> dict:
    """
    Executes the autonomous trip planning LangGraph workflow asynchronously.

    Initializes AgentState with input fields and empty/None defaults, invokes 
    the compiled graph, and returns the final state dictionary.
    """
    eff_origin = origin or kwargs.get("origin") or "DEL"
    eff_destination = destination or kwargs.get("destination") or "GOA"
    eff_start_date = start_date or kwargs.get("start_date") or "2026-08-01"
    
    raw_budget = budget_inr if budget_inr is not None else kwargs.get("max_budget")
    eff_budget_inr = int(raw_budget) if raw_budget else 15000

    initial_state: AgentState = {
        "origin": eff_origin,
        "destination": eff_destination,
        "start_date": eff_start_date,
        "budget_inr": eff_budget_inr,
        "flights": [],
        "flight_source": "",
        "flight_log_note": None,
        "hotels": [],
        "hotel_source": "",
        "hotel_log_note": None,
        "weather": None,
        "activities": None,
        "selected_flight": None,
        "selected_hotel": None,
        "total_cost": None,
        "budget_status": None,
        "action_log": [],
        "final_summary": None,
        # Helper fields for API/test compatibility
        "query": kwargs.get("query", f"Trip from {eff_origin} to {eff_destination}"),
        "end_date": kwargs.get("end_date", ""),
        "max_budget": float(eff_budget_inr),
        "flight_options": [],
        "hotel_options": [],
        "weather_info": None,
        "is_within_budget": True,
        "summary": "",
        "itinerary": {},
        "action_logs": []
    }

    final_state = await trip_planner_graph.ainvoke(initial_state)
    return dict(final_state)
