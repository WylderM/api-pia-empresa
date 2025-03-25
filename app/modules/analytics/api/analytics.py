from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.modules.auth.services.auth import get_current_user
from app.modules.analytics.services import analytics as analytics_service
from typing import List, Dict

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/top-setores", response_model=List[Dict])
async def top_setores(
    ano: int = Query(...),
    uf: str = Query(None),
    variavel: str = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await analytics_service.get_top_setores(db, ano, uf, variavel)

@router.get("/evolucao-variavel", response_model=List[Dict])
async def evolucao_variavel(
    cnae_classe: str = Query(...),
    uf: str = Query(None),
    variavel: str = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await analytics_service.get_evolucao_variavel(db, cnae_classe, uf, variavel)

@router.get("/comparativo-uf", response_model=List[Dict])
async def comparativo_uf(
    ano: int = Query(...),
    variavel: str = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await analytics_service.get_comparativo_uf(db, ano, variavel)
