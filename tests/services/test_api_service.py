import requests_mock
from app.services.api_service import APIService


def test_get_cep_data_success():
    with requests_mock.Mocker() as mock:
        url = "https://viacep.com.br/ws/12345678/json/"
        mock.get(
            url,
            json={
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
            },
        )
        result = APIService.fetch_cep_data("12345678")
        assert result["cep"] == "12345678"
        assert result["logradouro"] == "Rua Teste"
        assert result["complemento"] == "Apto 101"
        assert result["bairro"] == "Bairro Teste"
        assert result["localidade"] == "Cidade Teste"
        assert result["uf"] == "SP"
        assert result["ibge"] == "1234567"
        assert result["gia"] == "1234"
        assert result["ddd"] == "11"
        assert result["siafi"] == "1234"
