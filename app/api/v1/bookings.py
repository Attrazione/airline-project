from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.user import User
from app.schemas.bookings import BookingCreate, BookingRead
from app.services.booking_service import (
    create_booking,
    get_booking_by_id_for_user,
    list_bookings_for_user,
    cancel_booking,
)
from app.api.v1.auth import get_current_user  # уже есть в проекте


router = APIRouter()


@router.post(
    "/",
    response_model=BookingRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking_endpoint(
    booking_in: BookingCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    try:
        booking = await create_booking(
            session=session,
            user_id=current_user.id,
            flight_id=booking_in.flight_id,
        )
    except ValueError as e:
        if str(e) == "flight_not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Flight not found",
            )
        if str(e) == "no_seats_available":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No seats available on this flight",
            )
        raise

    return booking

@router.get(
    "/my",
    response_model=list[BookingRead],
)
async def list_my_bookings_endpoint(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    bookings = await list_bookings_for_user(
        session=session,
        user_id=current_user.id,
    )
    return bookings

@router.get(
    "/{booking_id}",
    response_model=BookingRead,
)
async def get_booking_endpoint(
    booking_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    booking = await get_booking_by_id_for_user(
        session=session,
        booking_id=booking_id,
        user_id=current_user.id,
    )
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    return booking





@router.post(
    "/{booking_id}/cancel",
    response_model=BookingRead,
)
async def cancel_booking_endpoint(
    booking_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    booking = await get_booking_by_id_for_user(
        session=session,
        booking_id=booking_id,
        user_id=current_user.id,
    )
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )

    booking = await cancel_booking(session=session, booking=booking)
    return booking