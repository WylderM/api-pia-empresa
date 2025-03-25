import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import AsyncSessionLocal
from app.modules.pia.models.pia import PIA

sample_data = [
    {
        "ano": 2021,
        "uf": "CE",
        "cnae_classe": "10.11-2",
        "variavel": "Valor da transformação industrial",
        "valor": 123456.78
    },
    {
        "ano": 2021,
        "uf": "CE",
        "cnae_classe": "10.12-1",
        "variavel": "Pessoal ocupado total",
        "valor": 987.65
    },
    {
        "ano": 2022,
        "uf": "SP",
        "cnae_classe": "10.11-2",
        "variavel": "Valor da transformação industrial",
        "valor": 456789.00
    },
    {
        "ano": 2022,
        "uf": "SP",
        "cnae_classe": "10.12-1",
        "variavel": "Pessoal ocupado total",
        "valor": 543.21
    }
]

async def run_seed():
    async with AsyncSessionLocal() as session:
        for row in sample_data:
            session.add(PIA(**row))
        await session.commit()

if __name__ == "__main__":
    asyncio.run(run_seed())
