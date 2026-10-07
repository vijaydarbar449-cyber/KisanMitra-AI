from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone

from database.database import Base


class User(Base):
    __tablename__ = "users"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Basic Information
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

    # User Role
    role = Column(
        String(20),
        default="farmer",
        nullable=False
    )

    # Language & Location
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

    # Farmer Profile Information
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

    # Account Status
    is_active = Column(
        Boolean,
        default=True
    )

    # Account Creation Time
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )