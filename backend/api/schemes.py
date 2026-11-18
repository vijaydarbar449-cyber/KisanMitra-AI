import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from api.deps import get_current_user
from services.scheme_service import answer_scheme_question
from services.schemes_data import LAST_VERIFIED, SCHEMES, TIPS

logger = logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix="/api/v1/schemes",
    tags=["Government Schemes"]
)


class SchemeQuestion(BaseModel):
    question: str = Field(min_length=2, max_length=1000)
    language: str = "gu"
    scheme_id: str = Field(default="", max_length=50)


@router.get("")
def list_schemes():
    """ચકાસેલી યોજનાઓની યાદી (જાહેર માહિતી, લૉગિન જરૂરી નથી)."""
    return {
        "last_verified": LAST_VERIFIED,
        "tips": TIPS,
        "schemes": SCHEMES,
    }


@router.post("/ask")
def ask_about_schemes(
    request: SchemeQuestion,
    current_user=Depends(get_current_user),
):
    """યોજના વિશેના પ્રશ્નનો AI જવાબ (ચકાસેલી યાદીના આધારે)."""
    try:
        answer = answer_scheme_question(
            question=request.question.strip(),
            language=request.language,
            scheme_id=request.scheme_id.strip(),
        )
    except Exception as e:
        logger.exception("Scheme AI error: %s", e)
        raise HTTPException(
            status_code=503,
            detail="AI જવાબ હાલ મળી શકતો નથી. થોડી વાર પછી ફરી પ્રયત્ન કરો."
        )

    return {
        "status": "success",
        "last_verified": LAST_VERIFIED,
        "answer": answer,
    }