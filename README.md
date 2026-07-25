# AviaPlan (Working Name) — Autonomous Trip-Planning Agent

> Built for the Agentic AI Hackathon (24-Hour Build Window)

AviaPlan is an autonomous, multi-tool trip planning AI agent. Given a high-level natural language instruction (e.g. *"Plan a weekend trip to Goa under ₹15,000, leaving Friday"*), AviaPlan automatically decomposes the request, searches flights & hotels via live APIs with resilient fallback to local mock data, checks weather forecasts, performs budget optimization, and renders a realistic airline boarding pass and transparent execution audit log.

---

## Key Features & Hackathon Focus Areas

1. **Task Planning & Decomposition**:
   - Decomposes high-level instructions into concrete graph nodes (`planner` ➔ `flight_search` ➔ `hotel_search` ➔ `weather` ➔ `budget_check` ➔ `synthesizer`).
2. **Multi-Tool Orchestration & Fail-Safe Fallback**:
   - Integrates RapidAPI Skyscanner/Booking.com and Open-Meteo REST APIs.
   - Live API timeouts or missing credentials trigger a seamless fallback to verified local datasets, logged explicitly as a first-class feature (*"⚡ LIVE API FALLBACK TRIGGERED"*).
3. **National Geographic Scope & Graceful Degradation**:
   - Covers 7 major Indian hub airports (DEL, BOM, BLR, MAA, CCU, HYD, GOA).
   - Unseeded city pairs automatically degrade to representative hub routes with clear logged reasoning.
4. **Transparent Action Log**:
   - Timestamped timeline of all state node executions, tool invocations, API fallbacks, and budget retry attempts.
5. **Airline Livery Aesthetic**:
   - Light mode palette with warm cream background (`#FAF7F2`), slate text, sky blue & burnt orange livery accents.
   - Animated aircraft runway takeoff sequence (`TakeoffLoader.tsx`).
   - Authentic perforated boarding pass card with barcode (`BoardingPass.tsx`).

---

## Repository Structure

```
aviaplan/
├── backend/                  # FastAPI (Python) & LangGraph Agent Engine
│   ├── app/
│   │   ├── main.py           # FastAPI app entrypoint & CORS config
│   │   ├── models.py         # Pydantic domain schemas
│   │   ├── routes/plan.py    # POST /api/plan endpoint
│   │   ├── agent/            # LangGraph StateGraph, nodes & execution runner
│   │   ├── services/         # Flight, Hotel, Weather API callers & mock fallback
│   │   └── data/             # Mock datasets for 7 hub airports
│   ├── test_agent.py         # Standalone automated graph verification script
│   └── render.yaml           # Deployment setup for Render
│
├── frontend/                 # Next.js 15 App Router web interface
│   ├── app/
│   │   ├── page.tsx          # Main flow controller
│   │   ├── components/       # TripForm, TakeoffLoader, ActionLog, BoardingPass
│   │   └── globals.css       # Airline light palette & takeoff keyframes
│   ├── lib/api.ts            # Fetch client for backend communication
│   └── vercel.json           # Deployment setup for Vercel
│
└── docs/
    └── PROJECT_CONTEXT.md    # Hackathon project specification
```

---

## Quick Start Guide

### 1. Backend Setup & Automated Test
```bash
cd backend
pip install -r requirements.txt
python test_agent.py          # Run automated verification
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev                   # Starts Next.js on http://localhost:3000
```

Open `http://localhost:3000` to run trip planning searches!
