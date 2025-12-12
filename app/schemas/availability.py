# app/schemas/availability.py
import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class AvailabilityBase(BaseModel):
    flight_id: UUID = Field(..., description="ID рейса")
    date: datetime.date = Field(..., description="Дата вылета (без времени)")
    seats_available: int = Field(..., ge=0)
    price: Decimal = Field(..., ge=0)
    currency: str = Field(..., min_length=3, max_length=8)


class AvailabilitySetRequest(AvailabilityBase):
    pass


class AvailabilityResponse(AvailabilityBase):
    updated_at: datetime.datetime
    from_cache: bool = True
