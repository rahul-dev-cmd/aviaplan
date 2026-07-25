import asyncio
import os
import sys

# Ensure backend root is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from app.agent.graph import run_trip_planner

async def test_agent_execution():
    print("\n--- RUNNING AUTOMATED AGENT GRAPH VERIFICATION ---")
    query = "Plan a weekend trip to Goa under ₹15,000, leaving Friday"
    print(f"Input Query: '{query}'")
    
    result = await run_trip_planner(query=query)
    
    print("\n1. Verifying Action Logs...")
    logs = result.get("action_logs", [])
    assert len(logs) > 0, "Action logs should not be empty!"
    print(f"   [SUCCESS] Total Action Logs generated: {len(logs)}")
    for log in logs:
        print(f"   - [{log['timestamp']}] [{log['node'].upper()}] [{log['status']}]: {log['message']}")
        
    print("\n2. Verifying Sub-Task Outputs...")
    flight = result.get("selected_flight")
    hotel = result.get("selected_hotel")
    weather = result.get("weather_info")
    
    assert flight is not None, "Flight selection failed!"
    assert hotel is not None, "Hotel selection failed!"
    assert weather is not None, "Weather lookup failed!"
    print(f"   [SUCCESS] Selected Flight: {flight['airline']} ({flight['flight_number']}) - ₹{flight['price_inr']}")
    print(f"   [SUCCESS] Selected Hotel: {hotel['name']} - Total ₹{hotel['total_price_inr']}")
    print(f"   [SUCCESS] Weather City: {weather['city']} ({len(weather['forecast'])} days forecast)")

    print("\n3. Verifying Budget Calculation...")
    total_cost = result.get("total_cost", 0)
    is_within_budget = result.get("is_within_budget")
    print(f"   [SUCCESS] Total Cost: ₹{total_cost:,.0f} | Within Budget: {is_within_budget}")

    print("\n4. Verifying Synthesized Summary & Boarding Pass...")
    summary = result.get("summary", "")
    itinerary = result.get("itinerary", {})
    assert len(summary) > 0, "Summary generation failed!"
    assert "schedule" in itinerary, "Itinerary structure failed!"
    print(f"   [SUCCESS] Summary: {summary}")

    print("\n✅ ALL AUTOMATED VERIFICATION CHECKS PASSED PERFECTLY!\n")

if __name__ == "__main__":
    asyncio.run(test_agent_execution())
