from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.modules.pia.models.pia import PIA

async def get_top_setores(db: AsyncSession, ano: int, uf: str, variavel: str):
    query = (
        select(PIA.cnae_classe, func.sum(PIA.valor).label("total"))
        .where(PIA.ano == ano, PIA.variavel == variavel)
    )
    if uf:
        query = query.where(PIA.uf == uf)
    query = query.group_by(PIA.cnae_classe).order_by(func.sum(PIA.valor).desc()).limit(5)
    result = await db.execute(query)
    return [{"cnae_classe": row[0], "total": row[1]} for row in result.all()]

async def get_evolucao_variavel(db: AsyncSession, cnae_classe: str, uf: str, variavel: str):
    query = (
        select(PIA.ano, func.sum(PIA.valor).label("total"))
        .where(PIA.cnae_classe == cnae_classe, PIA.variavel == variavel)
    )
    if uf:
        query = query.where(PIA.uf == uf)
    query = query.group_by(PIA.ano).order_by(PIA.ano)
    result = await db.execute(query)
    return [{"ano": row[0], "total": row[1]} for row in result.all()]

async def get_comparativo_uf(db: AsyncSession, ano: int, variavel: str):
    query = (
        select(PIA.uf, func.sum(PIA.valor).label("total"))
        .where(PIA.ano == ano, PIA.variavel == variavel)
        .group_by(PIA.uf)
        .order_by(func.sum(PIA.valor).desc())
    )
    result = await db.execute(query)
    return [{"uf": row[0], "total": row[1]} for row in result.all()]
