# app/services/payment_service.py
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.models.payment import Payment
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentWebhookIn
import uuid


async def create_payment_for_booking(
    session: AsyncSession,
    data: PaymentCreate,
    current_user: User,
) -> Payment:
    # 1. Ищем бронирование
    stmt = select(Booking).where(Booking.id == data.booking_id)
    result = await session.execute(stmt)
    booking: Booking | None = result.scalar_one_or_none()

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to pay for this booking",
        )

    amount = data.amount or booking.total_price
    currency = data.currency or booking.currency

    # генерируем ID, который якобы выдал бы провайдер
    provider_payment_id = f"MOCK-{uuid.uuid4()}"

    payment = Payment(
        user_id=booking.user_id,
        booking_id=booking.id,
        amount=amount,
        currency=currency,
        status="PROCESSING",
        provider="mock",
        provider_payment_id=provider_payment_id,
    )

    session.add(payment)
    await session.flush()
    await session.commit()
    await session.refresh(payment)

    return payment


async def get_payment_by_id(
    session: AsyncSession,
    payment_id: UUID,
) -> Payment:
    stmt = select(Payment).where(Payment.id == payment_id)
    result = await session.execute(stmt)
    payment = result.scalar_one_or_none()

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )

    return payment


async def process_payment_webhook(
    session: AsyncSession,
    payload: PaymentWebhookIn,
) -> Payment:
    """
    Обработка вебхука от провайдера:
    - ищем платеж по provider_payment_id
    - обновляем статус
    """
    # 1. Ищем платёж по provider_payment_id
    stmt = select(Payment).where(
        Payment.provider_payment_id == payload.provider_payment_id
    )
    result = await session.execute(stmt)
    payment: Payment | None = result.scalar_one_or_none()

    if payment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found for this provider_payment_id",
        )

    # 2. Нормализуем статус
    status_map = {
        "succeeded": "SUCCEEDED",
        "failed": "FAILED",
        "processing": "PROCESSING",
    }
    new_status = status_map.get(payload.status.lower())

    if new_status is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported status: {payload.status}",
        )

    payment.status = new_status
    payment.updated_at = datetime.utcnow()

    session.add(payment)
    await session.commit()
    await session.refresh(payment)

    return payment
