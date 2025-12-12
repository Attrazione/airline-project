from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "dev"

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "flightdb"
    db_user: str = "appuser"
    db_password: str = "appsecret"

    jwt_secret: str = "super-secret-key-change-me"
    jwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url_async(self) -> str:
        # asyncpg драйвер для SQLAlchemy
        return (
            f"postgresql+asyncpg://{self.db_user}:"
            f"{self.db_password}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )
    
    @property
    def database_url_sync(self) -> str:
        # sync-драйвер для Alembic
        return (
            f"postgresql+psycopg2://{self.db_user}:"
            f"{self.db_password}@{self.db_host}:"
            f"{self.db_port}/{self.db_name}"
        )

    redis_url: str = "redis://localhost:6379/0"
    redis_availability_ttl_seconds: int = 300


# ленивый синглтон настроек
settings = Settings()
