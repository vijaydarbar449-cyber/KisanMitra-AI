from datetime import date
from pydantic import BaseModel


class FarmCreate(BaseModel):
    farm_name: str
    soil_type: str | None = None
    crop_name: str | None = None
    crop_variety: str | None = None
    land_area: str | None = None
    area_unit: str = "acre"
    irrigation_type: str | None = None
    sowing_date: date | None = None
    notes: str | None = None


class FarmResponse(BaseModel):
    id: int
    user_id: int
    farm_name: str
    soil_type: str | None = None
    crop_name: str | None = None
    crop_variety: str | None = None
    land_area: str | None = None
    area_unit: str
    irrigation_type: str | None = None
    sowing_date: date | None = None
    notes: str | None = None

    class Config:
        from_attributes = True


class FarmUpdate(BaseModel):
    farm_name: str | None = None
    soil_type: str | None = None
    crop_name: str | None = None
    crop_variety: str | None = None
    land_area: str | None = None
    area_unit: str | None = None
    irrigation_type: str | None = None
    sowing_date: date | None = None
    notes: str | None = None