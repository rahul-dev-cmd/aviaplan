from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import (
    planner_node,
    flight_search_node,
    hotel_search_node,
    weather_node,
    budget_check_node,
    synthesizer_node
)

def create_trip_planner_graph():
    workflow = StateGraph(AgentState)

    # 1. Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("flight_search", flight_search_node)
    workflow.add_node("hotel_search", hotel_search_node)
    workflow.add_node("weather", weather_node)
    workflow.add_node("budget_check", budget_check_node)
    workflow.add_node("synthesizer", synthesizer_node)

    # 2. Wire edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "flight_search")
    workflow.add_edge("flight_search", "hotel_search")
    workflow.add_edge("hotel_search", "weather")
    workflow.add_edge("weather", "budget_check")
    workflow.add_edge("budget_check", "synthesizer")
    workflow.add_edge("synthesizer", END)

    return workflow.compile()

# Global compiled graph instance
trip_planner_agent = create_trip_planner_graph()

async def run_trip_planner(
    query: str = "",
    origin: str = None,
    destination: str = None,
    start_date: str = None,
    end_date: str = None,
    max_budget: float = None
) -> AgentState:
    """
    Executes the full LangGraph state machine workflow asynchronously.
    """
    budget_val = int(max_budget) if max_budget else 15000
    
    initial_state: AgentState = {
        "query": query,
        "origin": origin or "DEL",
        "destination": destination or "GOA",
        "start_date": start_date or "2026-08-01",
        "end_date": end_date or "2026-08-03",
        "budget_inr": budget_val,
        "max_budget": float(budget_val),
        "flights": [],
        "flight_source": "",
        "flight_log_note": None,
        "hotels": [],
        "hotel_source": "",
        "hotel_log_note": None,
        "weather": None,
        "selected_flight": None,
        "selected_hotel": None,
        "total_cost": None,
        "budget_status": None,
        "action_log": [],
        "final_summary": None,
        "flight_options": [],
        "hotel_options": [],
        "weather_info": None,
        "is_within_budget": True,
        "summary": "",
        "itinerary": {},
        "action_logs": []
    }
    
    final_state = await trip_planner_agent.ainvoke(initial_state)
    return final_state

