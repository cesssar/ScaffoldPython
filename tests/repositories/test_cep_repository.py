from app.repositories.cep_repository import CEPRepository
from app.models.cep import CEP


def test_create_and_get_cep(db_session):
    cep_repository = CEPRepository()
    cep_data = {
        "cep": "12345678",
        "logradouro": "Rua Teste",
        "complemento": "Apto 101",
        "bairro": "Bairro Teste",
        "localidade": "Cidade Teste",
        "uf": "SP",
        "ibge": "1234567",
        "gia": "1234",
        "ddd": "11",
        "siafi": "1234",
    }

    created_cep: CEP = cep_repository.create_cep(db_session, cep_data)
    retrieved_cep: CEP = cep_repository.get_cep(db_session, created_cep.cep)

    assert created_cep.cep == retrieved_cep.cep
    assert created_cep.logradouro == retrieved_cep.logradouro
    assert created_cep.complemento == retrieved_cep.complemento
    assert created_cep.bairro == retrieved_cep.bairro
    assert created_cep.localidade == retrieved_cep.localidade
    assert created_cep.uf == retrieved_cep.uf
    assert created_cep.ibge == retrieved_cep.ibge
    assert created_cep.gia == retrieved_cep.gia
    assert created_cep.ddd == retrieved_cep.ddd
    assert created_cep.siafi == retrieved_cep.siafi
