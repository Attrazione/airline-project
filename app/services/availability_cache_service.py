# app/services/availability_cache_service.py
import json
from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status

from app.core.config import settings
from app.core.redis_client import get_redis_client
from app.schemas.availability import (
    AvailabilitySetRequest,
    AvailabilityResponse,
)


def _make_key(flight_id: UUID, date_str: str) -> str:
    """
    Ключ в Redis: availability:<flight_id>:<date>
    Пример: availability:52a3...:2025-12-20
    """
    return f"availability:{flight_id}:{date_str}"


async def get_availability_from_cache(flight_id: UUID, date_str: str) -> AvailabilityResponse:
    redis = get_redis_client()
    key = _make_key(flight_id, date_str)

    raw = await redis.get(key)
    if raw is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability cache not found",
        )

    data = json.loads(raw)
    return AvailabilityResponse(**data)


async def set_availability_to_cache(payload: AvailabilitySetRequest) -> AvailabilityResponse:
    redis = get_redis_client()

    now = datetime.utcnow()
    date_str = payload.date.isoformat()

    key = _make_key(payload.flight_id, date_str)

    stored = {
        "flight_id": str(payload.flight_id),
        "date": date_str,
        "seats_available": payload.seats_available,
        "price": str(payload.price),
        "currency": payload.currency,
        "updated_at": now.isoformat() + "Z",
        "from_cache": True,
    }

    # TTL берём из настроек (по умолчанию 300 секунд)
    await redis.set(
        key,
        json.dumps(stored),
        ex=settings.redis_availability_ttl_seconds,
    )

    return AvailabilityResponse(**stored)
