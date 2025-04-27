from sqlalchemy import Column, Integer, String
from app.database import Base


class CEP(Base):
    __tablename__ = "CEP"

    id = Column(Integer, primary_key=True, index=True)
    cep = Column(String(9), index=True)
    logradouro = Column(String(255))
    complemento = Column(String(100))
    unidade = Column(String(100))
    bairro = Column(String(100))
    localidade = Column(String(100))
    uf = Column(String(2))
    estado = Column(String(100))
    regiao = Column(String(100))
    ibge = Column(String(7))
    gia = Column(String(7))
    ddd = Column(String(2))
    siafi = Column(String(7))
