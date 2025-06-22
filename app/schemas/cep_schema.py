from pydantic import BaseModel


class CEPSchema(BaseModel):
    cep: str
    logradouro: str
    complemento: str
    unidade: str
    bairro: str
    localidade: str
    uf: str
    estado: str
    regiao: str
    ibge: str
    gia: str
    ddd: int
    siafi: int

    model_config = {"from_attributes": True}
