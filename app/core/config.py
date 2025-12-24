from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "postgres"
    DATABASE_DB: str = "postgres"
    DATABASE_HOST: str = "db"
    DATABASE_PORT: int = 5432
    DATABASE_URL: str | None = None
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    PUBLIC_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+asyncpg://{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/{self.DATABASE_DB}"
        )

    @property
    def database_url_sync(self) -> str:
        """url síncrona para Alembic (ya q usa psycopg2)"""
        if self.DATABASE_URL:
            return self.DATABASE_URL.replace("+asyncpg", "")
        return (
            f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/"
            f"{self.DATABASE_DB}"
        )
