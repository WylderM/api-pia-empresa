from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.cache import redis

async def check_database(db: AsyncSession) -> str:
    try:
        await db.execute(text("SELECT 1"))
        return "ok"
    except Exception:
        return "unreachable"

async def check_cache() -> str:
    try:
        return "ok" if await redis.ping() else "unreachable"
    except Exception:
        return "unreachable"
