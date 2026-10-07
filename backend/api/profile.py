from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.database import get_db
from models.user import User
from api.auth import get_current_user


router = APIRouter(
    prefix="/api/v1/profile",
    tags=["Profile"]
)


class ProfileUpdate(BaseModel):
    language: str | None = None
    village: str | None = None
    district: str | None = None
    state: str | None = None
    main_crop: str | None = None
    land_area: str | None = None
    irrigation_type: str | None = None
    mobile: str | None = None


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
            "state": current_user.state,
            "main_crop": current_user.main_crop,
            "land_area": current_user.land_area,
            "irrigation_type": current_user.irrigation_type,
            "mobile": current_user.mobile
        }
    }


@router.put("/me")
def update_my_profile(
    profile: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if profile.language is not None:
        current_user.language = profile.language

    if profile.village is not None:
        current_user.village = profile.village

    if profile.district is not None:
        current_user.district = profile.district

    if profile.state is not None:
        current_user.state = profile.state

    if profile.main_crop is not None:
        current_user.main_crop = profile.main_crop

    if profile.land_area is not None:
        current_user.land_area = profile.land_area

    if profile.irrigation_type is not None:
        current_user.irrigation_type = profile.irrigation_type

    if profile.mobile is not None:
        current_user.mobile = profile.mobile

    db.commit()
    db.refresh(current_user)

    return {
        "status": "success",
        "message": "Profile updated successfully",
        "user": {
            "user_id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
            "language": current_user.language,
            "village": current_user.village,
            "district": current_user.district,
            "state": current_user.state,
            "main_crop": current_user.main_crop,
            "land_area": current_user.land_area,
            "irrigation_type": current_user.irrigation_type,
            "mobile": current_user.mobile
        }
    }