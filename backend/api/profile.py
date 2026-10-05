from fastapi import APIRouter, Depends

from models.user import User
from api.deps import get_current_user


router = APIRouter(
    prefix="/api/v1/profile",
    tags=["Profile"]
)


@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "status": "success",
        "user": {
            "user_id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
            "language": current_user.language,
            "village": current_user.village,
            "district": current_user.district,
            "state": current_user.state
        }
    }