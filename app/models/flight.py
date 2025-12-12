# app/models/flight.py

from sqlalchemy import Column, String, DateTime, Integer, Numeric, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.core.db import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),  # требует расширение pgcrypto в БД
    )

    # Например: "ALA-IST-123"
    flight_number = Column(String(20), nullable=False, index=True)

    # IATA-код аэропорта отправления, например "ALA"
    origin = Column(String(3), nullable=False, index=True)

    # IATA-код аэропорта прибытия, например "IST"
    destination = Column(String(3), nullable=False, index=True)

    departure_time = Column(DateTime(timezone=True), nullable=False, index=True)
    arrival_time = Column(DateTime(timezone=True), nullable=False)

    base_price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")

    seats_total = Column(Integer, nullable=False)
    seats_available = Column(Integer, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
