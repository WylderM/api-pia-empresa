from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.modules.pia.models.pia import PIA
from typing import List
from app.core.cache import make_cache_key, get_cache, set_cache
import json

async def get_pia_data(
    db: AsyncSession,
    ano: int = None,
    uf: str = None,
    cnae_classe: str = None,
    variavel: str = None,
    skip: int = 0,
    limit: int = 100
) -> List[PIA]:
    # Geração da chave
    params = {
        "ano": ano,
        "uf": uf,
        "cnae_classe": cnae_classe,
        "variavel": variavel,
        "skip": skip,
        "limit": limit
    }
    key = await make_cache_key("/pia", params)

    # Busca no cache
    cached = await get_cache(key)
    if cached:
        return [PIA(**row) for row in json.loads(cached)]

    # Se não achar no cache, consulta banco
    query = select(PIA)
    if ano:
        query = query.where(PIA.ano == ano)
    if uf:
        query = query.where(PIA.uf == uf)
    if cnae_classe:
        query = query.where(PIA.cnae_classe == cnae_classe)
    if variavel:
        query = query.where(PIA.variavel == variavel)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    data = result.scalars().all()

    # Cacheia o resultado
    await set_cache(key, [item.__dict__ for item in data])

    return data