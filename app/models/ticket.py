from datetime import datetime
import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.core.db import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    booking_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bookings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    passenger_name = Column(String(255), nullable=False)
    passenger_document = Column(String(64), nullable=True)
    seat_number = Column(String(16), nullable=True)

    ticket_number = Column(String(64), unique=True, nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
