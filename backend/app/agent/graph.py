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
    query: str,
    origin: str = None,
    destination: str = None,
    start_date: str = None,
    end_date: str = None,
    max_budget: float = None
) -> AgentState:
    """
    Executes the full LangGraph state machine workflow asynchronously.
    """
    initial_state: AgentState = {
        "query": query,
        "origin": origin or "",
        "destination": destination or "",
        "start_date": start_date or "",
        "end_date": end_date or "",
        "max_budget": max_budget or 0.0,
        "flight_options": [],
        "hotel_options": [],
        "weather_info": None,
        "selected_flight": None,
        "selected_hotel": None,
        "total_cost": 0.0,
        "is_within_budget": True,
        "flight_index": 0,
        "hotel_index": 0,
        "summary": "",
        "itinerary": {},
        "action_logs": []
    }
    
    final_state = await trip_planner_agent.ainvoke(initial_state)
    return final_state
