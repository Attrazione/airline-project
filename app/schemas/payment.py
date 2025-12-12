# app/schemas/payments.py
from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PaymentCreate(BaseModel):
    booking_id: UUID = Field(..., description="ID бронирования")
    amount: Decimal = Field(..., description="Сумма платежа")
    currency: str = Field(..., description="Валюта, например 'USD'")


class PaymentRead(BaseModel):
    id: UUID
    booking_id: UUID
    amount: Decimal
    currency: str
    status: str
    provider_payment_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # для SQLAlchemy моделей


class PaymentWebhookIn(BaseModel):
    """
    То, что как будто присылает внешний провайдер в вебхук.
    """
    event: str = Field(..., description="payment_succeeded / payment_failed / payment_refunded")
    payment_id: UUID = Field(..., description="ID платежа в нашей системе")
    provider_payment_id: str = Field(..., description="ID в системе провайдера")
    amount: Decimal = Field(..., description="Сумма, которую провайдер считает оплаченной")
    currency: str = Field(..., description="Валюта платежа")
    status: str = Field(..., description="succeeded / failed / refunded")
