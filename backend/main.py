from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

from api.auth import router as auth_router
from api.profile import router as profile_router


app = FastAPI(
    title="KisanMitra AI",
    description=(
        "A multilingual AI-powered Rural Decision Assistant "
        "for agriculture, weather, water, markets and "
        "government schemes."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# -------------------------
# CORS Configuration
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# API Routers
# -------------------------

app.include_router(auth_router)
app.include_router(profile_router)


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():
    return {
        "project": "KisanMitra AI",
        "message": "AI Rural Decision Assistant is running",
        "status": "success",
        "version": "1.0.0",
    }


# -------------------------
# Health Check
# -------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "KisanMitra AI Backend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# -------------------------
# API Information
# -------------------------

@app.get("/api")
def api_information():
    return {
        "project": "KisanMitra AI",
        "api_version": "v1",
        "modules": [
            "Authentication",
            "User Profile",
            "AI Assistant",
            "Weather",
            "Crop Assistant",
            "Water Advisory",
            "Market Information",
            "Government Schemes",
            "Voice Assistant",
            "Smart Alerts",
        ],
        "status": "active",
    }


# -------------------------
# Project Status
# -------------------------

@app.get("/api/v1/status")
def project_status():
    return {
        "project": "KisanMitra AI",
        "backend": "FastAPI",
        "authentication": "active",
        "jwt_authentication": "active",
        "user_profile": "active",
        "ai_assistant": "planned",
        "rag_system": "planned",
        "weather_service": "planned",
        "market_service": "planned",
        "scheme_service": "planned",
        "voice_service": "planned",
        "database": "active",
        "status": "development",
    }