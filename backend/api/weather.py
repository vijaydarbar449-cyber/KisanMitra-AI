import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from api.deps import get_current_user
from services.weather_service import (
    PlaceNotFound,
    find_place,
    get_forecast,
    search_places,
    weather_advice,
)

logger = logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix="/api/v1/weather",
    tags=["Weather"]
)


class WeatherRequest(BaseModel):
    location: str = Field(default="", max_length=100)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    place_name: str = Field(default="", max_length=150)
    crop: str = Field(default="", max_length=100)
    language: str = "gu"


@router.get("/places")
def places(
    q: str = Query(..., min_length=2, max_length=100),
    current_user=Depends(get_current_user),
):
    """ગામ/શહેર શોધો (સૂચનો માટે)."""
    try:
        results = search_places(q.strip(), count=10)
    except httpx.HTTPError as e:
        logger.exception("Place search error: %s", e)
        raise HTTPException(
            status_code=503,
            detail="સ્થળની શોધ હાલ થઈ શકતી નથી. થોડી વાર પછી ફરી પ્રયત્ન કરો."
        )
    return {"results": results}


@router.post("/advice")
def get_weather_advice(
    request: WeatherRequest,
    current_user=Depends(get_current_user),
):
    """ગામ/શહેર કે GPS સ્થાનનું હવામાન જોઈને ખેતીની સલાહ આપે છે."""
    try:
        if request.latitude is not None and request.longitude is not None:
            place = {
                "name": request.place_name.strip() or "તમારું સ્થાન",
                "taluka": None,
                "district": None,
                "state": None,
                "latitude": request.latitude,
                "longitude": request.longitude,
            }
        elif len(request.location.strip()) >= 2:
            place = find_place(request.location.strip())
        else:
            raise HTTPException(
                status_code=400,
                detail="ગામ/શહેરનું નામ લખો અથવા તમારું સ્થાન પસંદ કરો."
            )
        current, days = get_forecast(place["latitude"], place["longitude"])
    except PlaceNotFound:
        raise HTTPException(
            status_code=404,
            detail="આ સ્થળ મળ્યું નહીં. નજીકના મોટા શહેરનું નામ લખો, અથવા 📍 મારું સ્થાન વાપરો."
        )
    except httpx.HTTPError as e:
        logger.exception("Weather API error: %s", e)
        raise HTTPException(
            status_code=503,
            detail="હવામાનની માહિતી હાલ મળી શકતી નથી. થોડી વાર પછી ફરી પ્રયત્ન કરો."
        )

    try:
        advice = weather_advice(
            place=place,
            current=current,
            days=days,
            crop=request.crop.strip(),
            language=request.language,
        )
    except Exception as e:
        logger.exception("AI error: %s", e)
        raise HTTPException(
            status_code=503,
            detail="AI સલાહ હાલ મળી શકતી નથી. થોડી વાર પછી ફરી પ્રયત્ન કરો."
        )

    return {
        "status": "success",
        "place": place,
        "current": current,
        "days": days,
        "advice": advice,
    }