# app/schemas/notification.py
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class NotificationRead(BaseModel):
    id: UUID
    type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
