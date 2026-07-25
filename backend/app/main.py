import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from app.routes.plan import router as plan_router

app = FastAPI(
    title="AviaPlan Autonomous Trip Planning Agent API",
    description="Backend API powering AviaPlan hackathon trip planning agent.",
    version="1.0.0"
)

# Configure CORS dynamically using FRONTEND_URL and CORS_ORIGINS env vars
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
cors_origins_raw = os.getenv("CORS_ORIGINS", "")

allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

if frontend_url:
    for url in frontend_url.split(","):
        cleaned = url.strip()
        if cleaned and cleaned not in allowed_origins:
            allowed_origins.append(cleaned)

if cors_origins_raw:
    for url in cors_origins_raw.split(","):
        cleaned = url.strip()
        if cleaned and cleaned not in allowed_origins:
            allowed_origins.append(cleaned)

allow_all = "*" in allowed_origins or "*" in cors_origins_raw

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plan_router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "AviaPlan Agentic AI Engine",
        "health": "/api/health"
    }

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
