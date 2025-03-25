from pydantic import BaseModel

class PIABase(BaseModel):
    ano: int
    uf: str
    cnae_classe: str
    variavel: str
    valor: float

class PIAOut(PIABase):
    id: int

    class Config:
        orm_mode = True
