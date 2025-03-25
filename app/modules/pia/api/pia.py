from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.modules.pia.schemas.pia import PIAOut
from app.modules.pia.services import pia as pia_service
from app.modules.auth.services.auth import get_current_user
from typing import List

router = APIRouter(prefix="/pia", tags=["PIA Empresa"])

@router.get("/", response_model=List[PIAOut])
async def fetch_pia_data(
    ano: int = Query(None),
    uf: str = Query(None),
    cnae_classe: str = Query(None),
    variavel: str = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await pia_service.get_pia_data(db, ano, uf, cnae_classe, variavel, skip, limit)
