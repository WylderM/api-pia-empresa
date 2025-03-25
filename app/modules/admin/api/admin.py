from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.modules.admin.services.monitor import check_database, check_cache

router = APIRouter(tags=["Admin"])

@router.get("/status")
async def status():
    return {"status": "ok", "message": "API is running!"}

@router.get("/health")
async def healthcheck(db: AsyncSession = Depends(get_db)):
    db_status = await check_database(db)
    cache_status = await check_cache()
    return {
        "database": db_status,
        "cache": cache_status
    }
