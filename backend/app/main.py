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

# Configure CORS
cors_origins_raw = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000,*")
cors_origins = [origin.strip() for origin in cors_origins_raw.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in cors_origins else cors_origins,
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
    return {"status": "ok", "service": "aviaplan-backend"}
