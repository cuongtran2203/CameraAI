"""
Database Configuration
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database - Support both SQLite and PostgreSQL
    # SQLite: sqlite:///./camera_analyst.db
    # PostgreSQL: postgresql+asyncpg://user:pass@host:port/dbname
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./camera_analyst.db"
    )
    DATABASE_URL_SYNC: str = os.getenv(
        "DATABASE_URL_SYNC",
        "sqlite:///./camera_analyst.db"
    )

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # AI service
    AI_SERVICE_URL: str = os.getenv("AI_SERVICE_URL", "http://localhost:8000")

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

# Check if using SQLite
is_sqlite = settings.DATABASE_URL.startswith("sqlite")

# Convert sqlite to aiosqlite for async support
if is_sqlite:
    db_url = settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
else:
    db_url = settings.DATABASE_URL

# Async engine (for FastAPI)
engine = create_async_engine(
    db_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=10 if not is_sqlite else 5,
    max_overflow=20 if not is_sqlite else 5
)

# Sync engine (for migrations)
engine_sync = create_engine(
    settings.DATABASE_URL_SYNC.replace("sqlite+aiosqlite://", "sqlite://"),
    echo=False,
    pool_pre_ping=True
)

# Session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

SessionLocal = sessionmaker(
    engine_sync,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()


async def get_db():
    """Dependency for getting async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_db_sync():
    """Dependency for getting sync database session"""
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()
