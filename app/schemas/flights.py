from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID


class FlightRead(BaseModel):
    id: UUID
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    base_price: float
    currency: str
    seats_total: int
    seats_available: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
