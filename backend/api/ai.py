from fastapi import APIRouter
from pydantic import BaseModel

from services.ai_service import generate_ai_response


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
        return {
            "status": "error",
            "message": "Please enter a question."
        }

    reply = generate_ai_response(
        message=message,
        language=request.language
    )

    return {
        "status": "success",
        "message": message,
        "language": request.language,
        "reply": reply
    }