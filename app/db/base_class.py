from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.utils.config import get_settings

DATABASE_URL_ASYNC = get_settings().database_url_async
async_engine = create_async_engine(
    DATABASE_URL_ASYNC,
    future=True,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

DATABASE_URL_SYNC = get_settings().database_url_sync
sync_engine = create_engine(DATABASE_URL_SYNC)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=sync_engine
)

Base = declarative_base()


async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
