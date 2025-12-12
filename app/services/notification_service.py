# app/services/notification_service.py
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.notification import Notification


async def create_notification(
    session: AsyncSession,
    user_id: UUID,
    type: str,
    title: str,
    message: str,
):
    notif = Notification(
        user_id=user_id,
        type=type,
        title=title,
        message=message,
    )
    session.add(notif)
    await session.commit()
    await session.refresh(notif)
    return notif


async def list_notifications(session: AsyncSession, user_id: UUID):
    result = await session.execute(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
    )
    return list(result.scalars().all())


async def mark_read(session: AsyncSession, notification_id: UUID, user_id: UUID):
    notif = await session.get(Notification, notification_id)
    if not notif or notif.user_id != user_id:
        return None

    notif.is_read = True
    await session.commit()
    await session.refresh(notif)
    return notif


async def delete_notification(session: AsyncSession, notification_id: UUID, user_id: UUID):
    notif = await session.get(Notification, notification_id)
    if not notif or notif.user_id != user_id:
        return False

    await session.delete(notif)
    await session.commit()
    return True
