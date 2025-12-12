from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.core.db import get_db
from app.models.user import User
from app.models.booking import Booking
from app.models.notification import Notification
from app.schemas.auth import UserRead
from app.schemas.bookings import BookingRead

router = APIRouter(
    prefix="/api/v1/admin",
    tags=["admin"],
)

@router.get("/users", response_model=list[UserRead])
async def admin_list_users(
    session: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    stmt = select(User)
    result = await session.execute(stmt)
    return result.scalars().all()
@router.get("/bookings", response_model=list[BookingRead])
async def admin_list_bookings(
    session: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    stmt = select(Booking)
    result = await session.execute(stmt)
    return result.scalars().all()
@router.post("/flights/sync")
async def sync_flights(
    admin: User = Depends(require_admin),
):
    # Здесь можно вызывать внешний API или скрипт
    return {"status": "ok", "message": "Flights synced (mock)"}
@router.post("/notifications/retry/{notification_id}")
async def retry_notification(
    notification_id: str,
    session: AsyncSession = Depends(get_db),
    admin: User = Depends(require_admin),
):
    stmt = select(Notification).where(Notification.id == notification_id)
    result = await session.execute(stmt)
    notif = result.scalar_one_or_none()

    if notif is None:
        return {"error": "Notification not found"}

    # Логика повторной отправки
    notif.status = "RETRY"
    await session.commit()

    return {"status": "ok", "notification_id": notification_id}
@router.get("/audit")
async def audit_log(
    admin: User = Depends(require_admin),
):
    return {
        "logs": [
            {"event": "user_login", "timestamp": "2025-01-01T12:00:00"},
            {"event": "booking_create", "timestamp": "2025-01-01T12:10:00"},
        ]
    }
