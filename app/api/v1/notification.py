# app/api/v1/notifications.py
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.api.v1.auth import get_current_user
from app.schemas.notifications import NotificationRead
from app.services.notification_service import (
    list_notifications,
    mark_read,
    delete_notification,
)

router = APIRouter()


@router.get("/my", response_model=list[NotificationRead])
async def get_my_notifications(
    session: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await list_notifications(session, user.id)


@router.patch("/{notif_id}/read", response_model=NotificationRead)
async def read_notification(
    notif_id: UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    notif = await mark_read(session, notif_id, user.id)
    if not notif:
        raise HTTPException(404, "Notification not found")
    return notif


@router.delete("/{notif_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notif(
    notif_id: UUID,
    session: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    ok = await delete_notification(session, notif_id, user.id)
    if not ok:
        raise HTTPException(404, "Notification not found")
    return
