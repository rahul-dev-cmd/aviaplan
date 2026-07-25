from fastapi import APIRouter, HTTPException
from app.models import TripRequest, TripResponse
from app.agent.graph import run_trip_planner

router = APIRouter()

@router.post("/plan", response_model=TripResponse)
async def plan_trip_endpoint(request: TripRequest):
    try:
        effective_budget = request.budget_inr or request.max_budget or 15000.0
        effective_query = request.query or f"Plan a trip from {request.origin or 'DEL'} to {request.destination or 'GOA'} under ₹{effective_budget}"
        
        agent_result = await run_trip_planner(
            query=effective_query,
            origin=request.origin,
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            max_budget=effective_budget
        )
        
        logs = agent_result.get("action_logs", [])
        response = TripResponse(
            success=True,
            origin=agent_result.get("origin", "DEL"),
            destination=agent_result.get("destination", "GOA"),
            start_date=agent_result.get("start_date", ""),
            end_date=agent_result.get("end_date", ""),
            max_budget=agent_result.get("max_budget", 15000.0),
            total_cost=agent_result.get("total_cost", 0.0),
            is_within_budget=agent_result.get("is_within_budget", True),
            selected_flight=agent_result.get("selected_flight"),
            selected_hotel=agent_result.get("selected_hotel"),
            weather_info=agent_result.get("weather_info"),
            summary=agent_result.get("summary", ""),
            itinerary=agent_result.get("itinerary", {}),
            action_logs=logs,
            action_log=logs
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution error: {str(e)}")
