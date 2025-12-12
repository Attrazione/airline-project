from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """Базовый класс для всех ORM-моделей."""
    pass


# Создаём асинхронный engine
engine = create_async_engine(
    settings.database_url_async,
    echo=False,          # можно True, если хочешь видеть SQL в логах
    future=True,
)


# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# Dependency для FastAPI (будем использовать в эндпоинтах)
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
