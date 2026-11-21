from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.database import Base


class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    farm_name = Column(String(100), nullable=False)
    soil_type = Column(String(100), nullable=True)
    crop_name = Column(String(100), nullable=True)
    crop_variety = Column(String(100), nullable=True)
    land_area = Column(String(50), nullable=True)
    area_unit = Column(String(20), default="acre")
    irrigation_type = Column(String(100), nullable=True)
    sowing_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)

    owner = relationship("User")