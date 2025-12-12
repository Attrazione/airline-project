# app/api/v1/flights.py
from datetime import date, datetime, time, timedelta
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.db import get_db              # <<< ТАК ЖЕ, как в auth.py
from app.models.flight import Flight
from app.schemas.flights import FlightRead

router = APIRouter(prefix="/api/v1/flights", tags=["flights"])


@router.get("/search", response_model=List[FlightRead])
async def search_flights(
    origin: Optional[str] = Query(None, min_length=3, max_length=3),
    destination: Optional[str] = Query(None, min_length=3, max_length=3),
    departure_date: Optional[date] = Query(None),
    limit: int = 20,
    offset: int = 0,
    session: AsyncSession = Depends(get_db),  # <<< тоже заменяем
):
    stmt = select(Flight).order_by(Flight.departure_time).limit(limit).offset(offset)
    conditions = []

    if origin:
        conditions.append(Flight.origin == origin.upper())
    if destination:
        conditions.append(Flight.destination == destination.upper())
    if departure_date:
        start = datetime.combine(departure_date, time.min)
        end = start + timedelta(days=1)
        conditions.append(and_(Flight.departure_time >= start,
                               Flight.departure_time < end))

    if conditions:
        stmt = stmt.where(and_(*conditions))

    result = await session.execute(stmt)
    return result.scalars().all()


@router.get("/{flight_id}", response_model=FlightRead)
async def get_flight(
    flight_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    stmt = select(Flight).where(Flight.id == flight_id)
    result = await session.execute(stmt)
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Flight not found")
    return obj


@router.get("/availability/{flight_id}")
async def get_availability(
    flight_id: UUID,
    session: AsyncSession = Depends(get_db),
):
    stmt = select(Flight).where(Flight.id == flight_id)
    result = await session.execute(stmt)
    flight = result.scalar_one_or_none()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    return {
        "flight_id": str(flight.id),
        "seats_total": flight.seats_total,
        "seats_available": flight.seats_available,
    }
