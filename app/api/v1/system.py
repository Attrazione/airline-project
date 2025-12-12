from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.config import settings
from fastapi import Response
router = APIRouter(tags=["system"])


@router.get("/health")
async def health_check(
    session: AsyncSession = Depends(get_db),
):
    """
    Простейший health-check.

    Проверяем:
    - что приложение живо
    - что база доступна (простым SELECT 1)
    """
    try:
        # лёгкая проверка БД
        await session.execute("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "db": db_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@router.get("/api/v1/version")
async def version():
    """
    Версия приложения / билд-метаданные.
    Можно привязать к settings или переменным окружения.
    """
    return {
        "service": "flight-booking-platform",
        "version": getattr(settings, "app_version", "1.0.0"),
        "build": getattr(settings, "build_sha", "local-dev"),
        "env": getattr(settings, "env", "local"),
    }


@router.get("/metrics", response_class=Response)
async def metrics():
    body = "\n".join([
        "# HELP app_info Application info",
        "# TYPE app_info gauge",
        'app_info{service="flight-booking-platform",version="1.0.0"} 1',
    ])
    return Response(content=body, media_type="text/plain")
