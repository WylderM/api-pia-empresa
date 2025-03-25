from sqlalchemy import Column, Integer, String, Float
from app.core.db_base import Base

class PIA(Base):
    __tablename__ = "pia_empresa"

    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, index=True)
    uf = Column(String, index=True)
    cnae_classe = Column(String, index=True)
    variavel = Column(String, index=True)
    valor = Column(Float)
