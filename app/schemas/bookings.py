from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BookingBase(BaseModel):
    flight_id: UUID


class BookingCreate(BookingBase):
    """
    Тело запроса при создании бронирования.
    Цена берётся из Flight.base_price, поэтому тут только flight_id.
    """
    pass


class BookingRead(BaseModel):
    id: UUID
    user_id: UUID
    flight_id: UUID
    status: str
    total_price: Decimal
    currency: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
