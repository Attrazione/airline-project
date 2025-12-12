from typing import Optional
import secrets
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import UserCreate
from app.core.security import hash_password, verify_password, create_access_token


async def get_user_by_email(
    session: AsyncSession,
    email: str,
) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(
    session: AsyncSession,
    user_in: UserCreate,
) -> User:
    """
    Создаёт нового пользователя. Бросаем исключение выше, если e-mail занят.
    """
    user = User(
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        full_name=user_in.full_name,
        phone=user_in.phone,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(
    session: AsyncSession,
    email: str,
    password: str,
) -> Optional[User]:
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    if not user.is_active:
        return None
    return user

async def enable_two_factor(
    session: AsyncSession,
    user: User,
) -> str:
    """
    Включает 2FA для пользователя, генерируя секрет.
    Возвращаем секрет, чтобы показать его юзеру (в реальном мире — QR/TOTP).
    """
    # генерим простой секрет, без pyotp для упрощения
    secret = secrets.token_hex(16)

    user.is_2fa_enabled = True
    user.two_factor_secret = secret

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return secret