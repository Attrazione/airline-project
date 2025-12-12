from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from app.models.flight import Flight

from app.services.notification_service import create_notification



async def create_booking(
    session: AsyncSession,
    user_id: UUID,
    flight_id: UUID,
) -> Booking:
    # 1. Проверяем, что рейс существует
    result = await session.execute(
        select(Flight).where(Flight.id == flight_id)
    )
    flight = result.scalar_one_or_none()

    if not flight:
        raise ValueError("flight_not_found")

    # 2. Проверяем наличие свободных мест
    if flight.seats_available <= 0:
        raise ValueError("no_seats_available")

    # 3. Бронируем: уменьшаем seats_available и создаём Booking
    flight.seats_available -= 1

    booking = Booking(
        user_id=user_id,
        flight_id=flight_id,
        status="CONFIRMED",
        total_price=flight.base_price,
        currency=flight.currency,
    )

    session.add(booking)
    await session.commit()
    await session.refresh(booking)
    await create_notification(
    session,
    user_id=booking.user_id,
    type="BOOKING_CREATED",
    title="Booking successfully created",
    message=f"Your booking {booking.id} for flight {flight.flight_number} was created.",
)

    return booking



async def get_booking_by_id_for_user(
    session: AsyncSession,
    booking_id: UUID,
    user_id: UUID,
) -> Booking | None:
    result = await session.execute(
        select(Booking).where(
            Booking.id == booking_id,
            Booking.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def list_bookings_for_user(
    session: AsyncSession,
    user_id: UUID,
) -> list[Booking]:
    result = await session.execute(
        select(Booking)
        .where(Booking.user_id == user_id)
        .order_by(Booking.created_at.desc())
    )
    return list(result.scalars().all())


async def cancel_booking(
    session: AsyncSession,
    booking: Booking,
) -> Booking:
    # Уже отменено — просто возвращаем
    if booking.status == "CANCELLED":
        return booking

    # Пытаемся вернуть место на рейс
    result = await session.execute(
        select(Flight).where(Flight.id == booking.flight_id)
    )
    flight = result.scalar_one_or_none()
    if flight:
        flight.seats_available += 1

    booking.status = "CANCELLED"
    await session.commit()
    await session.refresh(booking)
    return booking


