import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.ai_service import generate_ai_response

logger = logging.getLogger("uvicorn.error")


router = APIRouter(
    prefix="/api/v1/ai",
    tags=["AI Assistant"]
)


class ChatRequest(BaseModel):
    message: str
    language: str = "gu"


@router.post("/chat")
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Please enter a question.")

    try:
        reply = generate_ai_response(
            message=message,
            language=request.language
        )
    except Exception as e:
        logger.exception("AI error: %s", e)
        if "503" in str(e) or "429" in str(e):
            raise HTTPException(
                status_code=503,
                detail="AI સેવા હાલ વ્યસ્ત છે. થોડી વાર પછી ફરી પ્રયત્ન કરો."
            )
        raise HTTPException(
            status_code=500,
            detail="AI જવાબ આપી શક્યું નથી. થોડી વાર પછી ફરી પ્રયત્ન કરો."
        )

    return {
        "status": "success",
        "message": message,
        "language": request.language,
        "reply": reply
    }