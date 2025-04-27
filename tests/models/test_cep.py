from app.models.cep import CEP


def test_cep_model():
    cep = CEP(
        id=1,
        cep="12345678",
        logradouro="Rua Teste",
        complemento="Apto 101",
        bairro="Bairro Teste",
        localidade="Cidade Teste",
        uf="SP",
        ibge="1234567",
        gia="1234",
        ddd="11",
        siafi="1234",
    )
    assert cep.cep == "12345678"
    assert cep.logradouro == "Rua Teste"
    assert cep.complemento == "Apto 101"
    assert cep.bairro == "Bairro Teste"
    assert cep.localidade == "Cidade Teste"
    assert cep.uf == "SP"
    assert cep.ibge == "1234567"
    assert cep.gia == "1234"
    assert cep.ddd == "11"
    assert cep.siafi == "1234"
