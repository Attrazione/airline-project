from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.schemas.availability import (
    AvailabilitySetRequest,
    AvailabilityResponse,
)
from app.services.availability_cache_service import (
    get_availability_from_cache,
    set_availability_to_cache,
)

router = APIRouter(
    prefix="/api/v1/cache/availability",
    tags=["availability-cache"],
)


@router.get("", response_model=AvailabilityResponse)
async def get_availability(
    flight_id: UUID = Query(..., description="ID рейса"),
    date_: date = Query(..., alias="date", description="Дата вылета (YYYY-MM-DD)"),
):
    """
    INTERNAL: получить кэш доступности по рейсу и дате.
    """
    return await get_availability_from_cache(flight_id, date_.isoformat())


@router.put("", response_model=AvailabilityResponse)
async def put_availability(payload: AvailabilitySetRequest):
    """
    INTERNAL: установить/обновить кэш доступности.
    """
    return await set_availability_to_cache(payload)
