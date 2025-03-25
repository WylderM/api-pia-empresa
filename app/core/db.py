from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Engine assíncrono
engine = create_async_engine(settings.database_url, echo=False)

# Session assíncrona
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base para os modelos
Base = declarative_base()

# Dependency Injection no FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
