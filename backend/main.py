from database.database import create_db_and_tables
from models.farm import Farm
from models.expense import Expense
from pathlib import Path
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.auth import router as auth_router
from api.profile import router as profile_router
from api.ai import router as ai_router
from api.weather import router as weather_router
from api.schemes import router as schemes_router
from api.farm import router as farm_router
from api.expense import router as expense_router
from api.i18n import router as i18n_router


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
@app.on_event("startup")
def startup_event():
    create_db_and_tables()

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API ROUTERS
# ============================================================

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(ai_router)
app.include_router(weather_router)
app.include_router(schemes_router)
app.include_router(farm_router)
app.include_router(expense_router)
app.include_router(i18n_router)


# ============================================================
# FRONTEND (KisanMitra-AI\frontend\index.html) -> http://127.0.0.1:8000/app/
# ============================================================

FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"

if FRONTEND_DIR.is_dir():
    app.mount(
        "/app",
        StaticFiles(directory=FRONTEND_DIR, html=True),
        name="frontend",
    )


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return {
        "project": "KisanMitra AI",
        "message": "AI Rural Decision Assistant is running",
        "status": "success",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "KisanMitra AI Backend",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ============================================================
# API INFORMATION
# ============================================================

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


# ============================================================
# PROJECT STATUS
# ============================================================

@app.get("/api/v1/status")
def project_status():
    return {
        "project": "KisanMitra AI",
        "backend": "FastAPI",
        "authentication": "active",
        "jwt_authentication": "active",
        "user_profile": "active",
        "ai_assistant": "active",
        "rag_system": "planned",
        "weather_service": "active",
        "market_service": "planned",
        "scheme_service": "planned",
        "voice_service": "planned",
        "database": "active",
        "status": "development",
    }