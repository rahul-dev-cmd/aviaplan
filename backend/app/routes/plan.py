from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.models import TripRequest, TripResponse
from app.agent.graph import run_trip_planner

router = APIRouter()

@router.post("/plan", response_model=TripResponse)
async def plan_trip_endpoint(request: TripRequest):
    """
    Executes the autonomous trip planning workflow using the LangGraph StateGraph agent.
    """
    try:
        origin = request.origin or "DEL"
        destination = request.destination or "GOA"
        start_date = request.start_date or datetime.now().strftime("%Y-%m-%d")
        budget_inr = int(request.budget_inr or request.max_budget or 15000)

        # Run the compiled trip planner graph
        final_state = await run_trip_planner(
            origin=origin,
            destination=destination,
            start_date=start_date,
            budget_inr=budget_inr
        )

        selected_flight = final_state.get("selected_flight")
        selected_hotel = final_state.get("selected_hotel")
        total_cost = float(final_state.get("total_cost") or 0.0)
        budget_status = final_state.get("budget_status") or "within_budget"
        is_within = (budget_status == "within_budget")
        weather = final_state.get("weather") or final_state.get("weather_info")
        final_summary = final_state.get("final_summary") or final_state.get("summary") or ""

        # Map logs for Pydantic response model compatibility
        raw_logs_dicts = final_state.get("action_logs") or []
        raw_log_strings = final_state.get("action_log") or []

        log_items = []
        if raw_logs_dicts:
            log_items = raw_logs_dicts
        else:
            for s in raw_log_strings:
                log_items.append({
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "node": "agent",
                    "status": "INFO",
                    "message": str(s)
                })

        activities = final_state.get("activities")

        return TripResponse(
            success=True,
            origin=final_state.get("origin", origin),
            destination=final_state.get("destination", destination),
            start_date=final_state.get("start_date", start_date),
            end_date=final_state.get("end_date", ""),
            max_budget=float(budget_inr),
            total_cost=total_cost,
            is_within_budget=is_within,
            selected_flight=selected_flight,
            selected_hotel=selected_hotel,
            weather_info=weather,
            weather=weather,
            activities=activities,
            summary=final_summary,
            final_summary=final_summary,
            itinerary=final_state.get("itinerary", {}),
            action_logs=log_items,
            action_log=log_items
        )
    except Exception as err:
        raise HTTPException(
            status_code=500,
            detail=f"Trip planner graph execution error: {str(err)}"
        )
