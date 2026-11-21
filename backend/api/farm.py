from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from models.farm import Farm
from models.user import User
from api.auth import get_current_user
from schemas.farm import FarmCreate, FarmUpdate


router = APIRouter(
    prefix="/api/v1/farms",
    tags=["Farm Profile"]
)


@router.post("/")
def create_farm(
    farm_data: FarmCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_farm = Farm(
        user_id=current_user.id,
        farm_name=farm_data.farm_name,
        soil_type=farm_data.soil_type,
        crop_name=farm_data.crop_name,
        crop_variety=farm_data.crop_variety,
        land_area=farm_data.land_area,
        area_unit=farm_data.area_unit,
        irrigation_type=farm_data.irrigation_type,
        sowing_date=farm_data.sowing_date,
        notes=farm_data.notes
    )

    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)

    return {
        "status": "success",
        "message": "Farm created successfully",
        "farm": {
            "id": new_farm.id,
            "user_id": new_farm.user_id,
            "farm_name": new_farm.farm_name,
            "soil_type": new_farm.soil_type,
            "crop_name": new_farm.crop_name,
            "crop_variety": new_farm.crop_variety,
            "land_area": new_farm.land_area,
            "area_unit": new_farm.area_unit,
            "irrigation_type": new_farm.irrigation_type,
            "sowing_date": (
                new_farm.sowing_date.isoformat()
                if new_farm.sowing_date else None
            ),
            "notes": new_farm.notes
        }
    }


@router.get("/")
def get_my_farms(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    farms = db.query(Farm).filter(
        Farm.user_id == current_user.id
    ).all()

    return {
        "status": "success",
        "total_farms": len(farms),
        "farms": [
            {
                "id": farm.id,
                "user_id": farm.user_id,
                "farm_name": farm.farm_name,
                "soil_type": farm.soil_type,
                "crop_name": farm.crop_name,
                "crop_variety": farm.crop_variety,
                "land_area": farm.land_area,
                "area_unit": farm.area_unit,
                "irrigation_type": farm.irrigation_type,
                "sowing_date": (
                    farm.sowing_date.isoformat()
                    if farm.sowing_date else None
                ),
                "notes": farm.notes
            }
            for farm in farms
        ]
    }
@router.put("/{farm_id}")
def update_farm(
    farm_id: int,
    farm_data: FarmUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    farm = db.query(Farm).filter(
        Farm.id == farm_id,
        Farm.user_id == current_user.id
    ).first()

    if not farm:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    update_data = farm_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(farm, key, value)

    db.commit()
    db.refresh(farm)

    return {
        "status": "success",
        "message": "Farm updated successfully",
        "farm": {
            "id": farm.id,
            "farm_name": farm.farm_name,
            "soil_type": farm.soil_type,
            "crop_name": farm.crop_name,
            "crop_variety": farm.crop_variety,
            "land_area": farm.land_area,
            "area_unit": farm.area_unit,
            "irrigation_type": farm.irrigation_type,
            "sowing_date": (
                farm.sowing_date.isoformat()
                if farm.sowing_date else None
            ),
            "notes": farm.notes
        }
    }
@router.delete("/{farm_id}")
def delete_farm(
    farm_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    farm = db.query(Farm).filter(
        Farm.id == farm_id,
        Farm.user_id == current_user.id
    ).first()

    if not farm:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Farm not found"
        )

    db.delete(farm)
    db.commit()

    return {
        "status": "success",
        "message": "Farm deleted successfully",
        "farm_id": farm_id
    }