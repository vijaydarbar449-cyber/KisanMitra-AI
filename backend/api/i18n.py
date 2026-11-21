import logging

from fastapi import APIRouter, HTTPException

from services.i18n_service import LANGUAGES, get_translations

logger = logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix="/api/v1/i18n",
    tags=["Languages"]
)


@router.get("/languages")
def languages():
    """એપમાં ઉપલબ્ધ ભાષાઓ (જાહેર, લૉગિન જરૂરી નથી)."""
    return {"languages": LANGUAGES}


@router.get("/{code}")
def strings(code: str):
    """પસંદ કરેલી ભાષાના શબ્દો."""
    try:
        data = get_translations(code)
    except KeyError:
        raise HTTPException(status_code=404, detail="Unknown language")
    except Exception as e:
        logger.exception("i18n error for %s: %s", code, e)
        raise HTTPException(status_code=503, detail="Translation not available right now")
    return {"code": code, "strings": data}