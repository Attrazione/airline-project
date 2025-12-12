from datetime import datetime
import uuid

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Numeric,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    flight_id = Column(
        UUID(as_uuid=True),
        ForeignKey("flights.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    status = Column(String(32), nullable=False, default="PENDING")

    total_price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(8), nullable=False)

    idempotency_key = Column(String(64), unique=True, nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )