from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.security import create_access_token, decode_access_token
from app.schemas.auth import UserCreate, UserLogin, UserRead, Token, TwoFactorEnableResponse
from app.services.auth_service import (
    create_user,
    authenticate_user,
    get_user_by_email,
    enable_two_factor,
)
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    user = await get_user_by_email(session, email=email)
    if user is None:
        raise credentials_exception

    return user


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db),
):
    existing = await get_user_by_email(session, user_in.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    user = await create_user(session, user_in)
    return user


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    session: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(session, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=60)
    token = create_access_token(
        subject=user.email,
        expires_delta=access_token_expires,
    )
    return Token(access_token=token)


@router.get("/me", response_model=UserRead)
async def read_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.post("/2fa/enable", response_model=TwoFactorEnableResponse)
async def enable_2fa(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Включение двухфакторной аутентификации для текущего пользователя.
    Возвращаем флаг и секрет.
    """
    secret = await enable_two_factor(session=session, user=current_user)
    return TwoFactorEnableResponse(
        is_2fa_enabled=True,
        secret=secret,
    )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
):
    """
    Заглушка для логаута. На самом деле при использовании JWT на сервере
    """
    return {"detail": "Logged out. Please discard your token on client side."}
