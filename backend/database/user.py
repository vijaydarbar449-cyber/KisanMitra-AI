from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password = Column(
        String(255),
        nullable=False
    )

    role = Column(
        String(20),
        default="farmer",
        nullable=False
    )

    language = Column(
        String(20),
        default="gu",
        nullable=False
    )

    village = Column(
        String(100),
        nullable=True
    )

    district = Column(
        String(100),
        nullable=True
    )

    state = Column(
        String(100),
        default="Gujarat",
        nullable=True
    )

    main_crop = Column(
        String(100),
        nullable=True
    )

    land_area = Column(
        String(50),
        nullable=True
    )

    irrigation_type = Column(
        String(100),
        nullable=True
    )

    mobile = Column(
        String(20),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )