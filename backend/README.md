# AviaPlan Backend

FastAPI service powering the **AviaPlan** autonomous trip-planning state machine (LangGraph).

## Features
- **LangGraph State Machine**: `planner` ➔ `flight_search` ➔ `hotel_search` ➔ `weather` ➔ `budget_check` ➔ `synthesizer`
- **Multi-Tool Orchestration**: RapidAPI (Skyscanner/Booking.com) + Open-Meteo REST API.
- **Fail-Safe API Fallback**: If RapidAPI keys are unconfigured or fail/timeout, seamlessly switches to verified mock datasets with explicit audit log entries.
- **Graceful Route Degradation**: Handles unseeded city pairs gracefully by degrading to representative hub routes and logging reasoning.

## Local Setup & Run

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Run Automated Graph Verification Script**:
```bash
python test_agent.py
```

3. **Start FastAPI Server**:
```bash
uvicorn app.main:app --reload --port 8000
```
FastAPI docs available at `http://localhost:8000/docs`.
