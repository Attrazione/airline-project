import redis.asyncio as redis

from app.core.config import settings


def get_redis_client() -> "redis.Redis":
    """
    Ленивый клиент Redis. Подключение устанавливается при первом запросе.
    """
    return redis.from_url(
        settings.redis_url,
        decode_responses=True,  # строки, а не bytes
    )
