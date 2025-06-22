import pytest
import requests_mock
from app.services.api_service import APIService
from app.config.settings import settings # Import settings to build the URL consistently


@pytest.fixture
def api_service():
    return APIService()


def test_fetch_cep_data_success(api_service: APIService):
    cep = "12345678"
    url = f"{settings.EXTERNAL_API_URL}/{cep}/json/"
    mock_response_data = {
        "cep": "12345-678", # API might return with hyphen
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
    with requests_mock.Mocker() as mock:
        mock.get(url, json=mock_response_data, status_code=200)
        result = api_service.fetch_cep_data(cep)

        assert result is not None
        assert result["cep"] == "12345-678"
        assert result["logradouro"] == "Rua Teste"
        # ... (assert other fields as needed) ...

def test_fetch_cep_data_not_found(api_service: APIService):
    cep = "00000000"
    url = f"{settings.EXTERNAL_API_URL}/{cep}/json/"
    # ViaCEP returns {"erro": true} for not found CEPs with status 200
    mock_response_data = {"erro": True}
    with requests_mock.Mocker() as mock:
        mock.get(url, json=mock_response_data, status_code=200)
        result = api_service.fetch_cep_data(cep)
        assert result is None

def test_fetch_cep_data_http_error(api_service: APIService):
    cep = "12345678"
    url = f"{settings.EXTERNAL_API_URL}/{cep}/json/"
    with requests_mock.Mocker() as mock:
        mock.get(url, status_code=500)
        result = api_service.fetch_cep_data(cep)
        assert result is None

def test_fetch_cep_data_request_exception(api_service: APIService):
    cep = "12345678"
    url = f"{settings.EXTERNAL_API_URL}/{cep}/json/"
    with requests_mock.Mocker() as mock:
        import requests
        mock.get(url, exc=requests.exceptions.ConnectTimeout)
        result = api_service.fetch_cep_data(cep)
        assert result is None
