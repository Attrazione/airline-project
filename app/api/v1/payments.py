# app/api/v1/payments.py
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.db import get_db
from app.schemas.payment import PaymentCreate, PaymentRead, PaymentWebhookIn
from app.services.payment_service import (
    create_payment_for_booking,
    get_payment_by_id,
    process_payment_webhook,
)
from app.api.v1.auth import get_current_user
router = APIRouter(
    prefix="/api/v1/payments",
    tags=["payments"],
)


@router.post(
    "",
    response_model=PaymentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    data: PaymentCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
    
):
    """
    Инициировать платёж по бронированию.
    На этом шаге мы НЕ обращаемся к реальному провайдеру,
    просто создаём запись со статусом PROCESSING.
    """
    payment = await create_payment_for_booking(session, data, current_user)
    return payment


@router.get(
    "/{payment_id}",
    response_model=PaymentRead,
)
async def get_payment(
    payment_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    """
    Получить статус платежа.
    """
    payment = await get_payment_by_id(session, payment_id)
    return payment


@router.post(
    "/webhook",
    response_model=PaymentRead,
)
async def payment_webhook(
    payload: PaymentWebhookIn,
    session: AsyncSession = Depends(get_db),
):
    """
    Это вебхук, который в реальности вызывал бы платёжный провайдер.
    Сейчас мы будем дергать его сами (из Postman) как mock-провайдер.
    """
    payment = await process_payment_webhook(session, payload)
    return payment
