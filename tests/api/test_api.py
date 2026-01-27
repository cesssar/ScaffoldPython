from fastapi.testclient import TestClient
from app.main_api import app, get_cep_service
from app.models.cep import CEP
from unittest.mock import MagicMock
import pytest

client = TestClient(app)

def test_read_cep_success():
    mock_cep = CEP(
        cep="01001000",
        logradouro="Praça da Sé",
        complemento="lado ímpar",
        unidade="",
        bairro="Sé",
        localidade="São Paulo",
        uf="SP",
        estado="São Paulo",
        regiao="Sudeste",
        ibge="3550308",
        gia="1004",
        ddd="11",
        siafi="7107"
    )

    # Mocking the service
    mock_service = MagicMock()
    mock_service.get_or_fetch_cep_details.return_value = mock_cep

    # Override dependency
    app.dependency_overrides[get_cep_service] = lambda: mock_service

    response = client.get("/cep/01001000")

    # Clear override
    app.dependency_overrides = {}

    assert response.status_code == 200
    data = response.json()
    assert data["cep"] == "01001000"
    assert data["localidade"] == "São Paulo"
    assert data["ddd"] == 11
    assert data["siafi"] == 7107

def test_read_cep_not_found():
    # Mocking the service
    mock_service = MagicMock()
    mock_service.get_or_fetch_cep_details.return_value = None

    # Override dependency
    app.dependency_overrides[get_cep_service] = lambda: mock_service

    response = client.get("/cep/99999999")

    # Clear override
    app.dependency_overrides = {}

    assert response.status_code == 404
    assert response.json() == {"detail": "CEP not found"}
