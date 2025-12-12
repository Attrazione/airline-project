from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    phone: str | None = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: UUID
    is_active: bool
    role: str          # есть в models.User
    is_2fa_enabled: bool  # есть в models.User
    created_at: datetime
    updated_at: datetime  # тоже есть в models.User

    class Config:
        from_attributes = True  # для ORM-модели User


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TwoFactorEnableResponse(BaseModel):
    is_2fa_enabled: bool
    secret: str
