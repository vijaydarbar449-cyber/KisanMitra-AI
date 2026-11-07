import logging

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from api.deps import get_current_user
from services.ai_service import analyze_crop_image, generate_ai_response

logger = logging.getLogger("uvicorn.error")

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 MB


router = APIRouter(
    prefix="/api/v1/ai",
    tags=["AI Assistant"]
)


class ChatRequest(BaseModel):
    message: str
    language: str = "gu"


def _handle_ai_error(e: Exception):
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


@router.post("/chat")
def chat(
    request: ChatRequest,
    current_user=Depends(get_current_user),
):
    message = request.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Please enter a question.")

    try:
        reply = generate_ai_response(
            message=message,
            language=request.language
        )
    except Exception as e:
        _handle_ai_error(e)

    return {
        "status": "success",
        "message": message,
        "language": request.language,
        "reply": reply
    }


@router.post("/diagnose")
def diagnose(
    image: UploadFile = File(...),
    question: str = Form(""),
    current_user=Depends(get_current_user),
):
    """પાકના પાનનો ફોટો અપલોડ કરો, AI રોગ/જીવાતની ઓળખ આપશે."""
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="ફક્ત JPG, PNG કે WEBP ફોટો અપલોડ કરો."
        )

    image_bytes = image.file.read(MAX_IMAGE_BYTES + 1)

    if not image_bytes:
        raise HTTPException(status_code=400, detail="ફોટો ખાલી છે.")

    if len(image_bytes) > MAX_IMAGE_BYTES:
        raise HTTPException(
            status_code=413,
            detail="ફોટો 5 MB થી નાનો હોવો જોઈએ."
        )

    try:
        reply = analyze_crop_image(
            image_bytes=image_bytes,
            mime_type=image.content_type,
            question=question.strip(),
        )
    except Exception as e:
        _handle_ai_error(e)

    return {
        "status": "success",
        "reply": reply
    }