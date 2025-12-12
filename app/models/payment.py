# app/models/payment.py
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


class Payment(Base):
    __tablename__ = "payments"

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

    booking_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(8), nullable=False)

    status = Column(
        String(32),
        nullable=False,
        default="PENDING",  # PENDING / SUCCEEDED / FAILED
    )

    provider = Column(String(32), nullable=True, default="mock")
    provider_payment_id = Column(String(64), nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
