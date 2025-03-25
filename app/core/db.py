from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.db_base import Base

def get_engine():
    return create_async_engine(settings.database_url, echo=False, future=True)

def get_sessionmaker(engine):
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession
    )

engine = get_engine()
AsyncSessionLocal = get_sessionmaker(engine)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

