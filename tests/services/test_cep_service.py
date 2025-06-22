import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from app.services.cep_service import CEPService
from app.models.cep import CEP

# Interfaces are used for type hinting and for mock spec if needed
from app.interfaces.cep_api_service_interface import ICEPAPIService
from app.interfaces.cep_repository_interface import ICEPRepository


@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_api_service():
    return MagicMock(spec=ICEPAPIService)


@pytest.fixture
def mock_cep_repository():
    return MagicMock(spec=ICEPRepository)


@pytest.fixture
def cep_service(mock_db_session, mock_api_service, mock_cep_repository):
    return CEPService(
        db_session=mock_db_session,
        api_service=mock_api_service,
        cep_repository=mock_cep_repository,
    )


@pytest.fixture
def sample_valid_cep_str():
    return "12345678"


@pytest.fixture
def sample_invalid_cep_str():
    return "12345"


@pytest.fixture
def sample_api_response_data(sample_valid_cep_str):
    return {
        "cep": sample_valid_cep_str,
        "logradouro": "Rua API",
        "complemento": "API Comp",
        "bairro": "Bairro API",
        "localidade": "Cidade API",
        "uf": "AP",
        "ibge": "api123",
        "gia": "apigia",
        "ddd": "96",
        "siafi": "apisiafi",
    }


@pytest.fixture
def sample_cep_model_from_db(sample_valid_cep_str):
    return CEP(
        cep=sample_valid_cep_str,
        logradouro="Rua DB",
        complemento="DB Comp",
        bairro="Bairro DB",
        localidade="Cidade DB",
        uf="DB",
        ibge="db123",
        gia="dbgia",
        ddd="00",
        siafi="dbsiafi",
    )


def test_get_or_fetch_cep_invalid_format(
    cep_service: CEPService, sample_invalid_cep_str
):
    result = cep_service.get_or_fetch_cep_details(sample_invalid_cep_str)
    assert result is None
    cep_service.api_service.fetch_cep_data.assert_not_called()
    cep_service.cep_repository.create_cep.assert_not_called()


def test_get_or_fetch_cep_found_in_db(
    cep_service: CEPService,
    mock_cep_repository: MagicMock,
    sample_valid_cep_str,
    sample_cep_model_from_db: CEP,
):
    mock_cep_repository.get_cep.return_value = sample_cep_model_from_db

    result = cep_service.get_or_fetch_cep_details(sample_valid_cep_str)

    assert result == sample_cep_model_from_db
    mock_cep_repository.get_cep.assert_called_once_with(
        cep_service.db_session, sample_valid_cep_str
    )
    cep_service.api_service.fetch_cep_data.assert_not_called()
    mock_cep_repository.create_cep.assert_not_called()


def test_get_or_fetch_cep_not_in_db_found_in_api_and_created(
    cep_service: CEPService,
    mock_api_service: MagicMock,
    mock_cep_repository: MagicMock,
    sample_valid_cep_str,
    sample_api_response_data: dict,
):
    mock_cep_repository.get_cep.return_value = None  # Not in DB
    mock_api_service.fetch_cep_data.return_value = sample_api_response_data

    created_cep_model = CEP(
        **{
            k: v
            for k, v in sample_api_response_data.items()
            if k in CEP.__table__.columns
        }
    )
    mock_cep_repository.create_cep.return_value = created_cep_model

    result = cep_service.get_or_fetch_cep_details(sample_valid_cep_str)

    assert result == created_cep_model
    mock_cep_repository.get_cep.assert_called_once_with(
        cep_service.db_session, sample_valid_cep_str
    )
    mock_api_service.fetch_cep_data.assert_called_once_with(
        sample_valid_cep_str)

    # Prepare expected data for create_cep call (filtered, cep sanitized)
    expected_data_for_create = sample_api_response_data.copy()
    expected_data_for_create["cep"] = "".join(
        filter(str.isdigit, expected_data_for_create.get("cep", ""))
    )
    model_fields = {column.name for column in CEP.__table__.columns}
    filtered_expected_data = {
        k: v for k, v in expected_data_for_create.items() if k in model_fields
    }

    mock_cep_repository.create_cep.assert_called_once_with(
        cep_service.db_session, filtered_expected_data
    )


def test_get_or_fetch_cep_not_in_db_not_in_api(
    cep_service: CEPService,
    mock_api_service: MagicMock,
    mock_cep_repository: MagicMock,
    sample_valid_cep_str,
):
    mock_cep_repository.get_cep.return_value = None
    mock_api_service.fetch_cep_data.return_value = None

    result = cep_service.get_or_fetch_cep_details(sample_valid_cep_str)

    assert result is None
    mock_cep_repository.get_cep.assert_called_once_with(
        cep_service.db_session, sample_valid_cep_str
    )
    mock_api_service.fetch_cep_data.assert_called_once_with(
        sample_valid_cep_str)
    mock_cep_repository.create_cep.assert_not_called()


def test_get_or_fetch_cep_api_returns_data_but_db_create_fails(
    cep_service: CEPService,
    mock_api_service: MagicMock,
    mock_cep_repository: MagicMock,
    sample_valid_cep_str,
    sample_api_response_data: dict,
):
    mock_cep_repository.get_cep.return_value = None
    mock_api_service.fetch_cep_data.return_value = sample_api_response_data
    mock_cep_repository.create_cep.return_value = None

    result = cep_service.get_or_fetch_cep_details(sample_valid_cep_str)

    assert result is None
    mock_cep_repository.get_cep.assert_called_once_with(
        cep_service.db_session, sample_valid_cep_str
    )
    mock_api_service.fetch_cep_data.assert_called_once_with(
        sample_valid_cep_str)

    expected_data_for_create = sample_api_response_data.copy()
    expected_data_for_create["cep"] = "".join(
        filter(str.isdigit, expected_data_for_create.get("cep", ""))
    )
    model_fields = {column.name for column in CEP.__table__.columns}
    filtered_expected_data = {
        k: v for k, v in expected_data_for_create.items() if k in model_fields
    }
    mock_cep_repository.create_cep.assert_called_once_with(
        cep_service.db_session, filtered_expected_data
    )


def test_get_or_fetch_cep_sanitizes_input_cep(
    cep_service: CEPService,
    mock_cep_repository: MagicMock,
    sample_cep_model_from_db: CEP,
):
    input_cep_with_hyphen = "12345-678"
    sanitized_cep = "12345678"
    mock_cep_repository.get_cep.return_value = sample_cep_model_from_db
    result = cep_service.get_or_fetch_cep_details(input_cep_with_hyphen)
    assert result == sample_cep_model_from_db
    mock_cep_repository.get_cep.assert_called_once_with(
        cep_service.db_session, sanitized_cep
    )


def test_cep_service_handles_api_data_with_extra_fields(
    cep_service: CEPService,
    mock_api_service: MagicMock,
    mock_cep_repository: MagicMock,
    sample_valid_cep_str,
):
    mock_cep_repository.get_cep.return_value = None

    api_data_with_extra = {
        "cep": sample_valid_cep_str,
        "logradouro": "Rua Teste",
        "bairro": "Bairro Teste",
        "localidade": "Cidade Teste",
        "uf": "TS",
        "ibge": "123",
        "ddd": "00",
        "extra_field_from_api": "should_be_ignored",
        "another_extra": 12345,
    }
    mock_api_service.fetch_cep_data.return_value = api_data_with_extra

    expected_data_for_db = {
        "cep": sample_valid_cep_str,
        "logradouro": "Rua Teste",
        "bairro": "Bairro Teste",
        "localidade": "Cidade Teste",
        "uf": "TS",
        "ibge": "123",
        "ddd": "00",
    }

    created_model = CEP(**expected_data_for_db)
    mock_cep_repository.create_cep.return_value = created_model

    result = cep_service.get_or_fetch_cep_details(sample_valid_cep_str)

    assert result is not None
    assert result.cep == sample_valid_cep_str
    assert result.logradouro == "Rua Teste"
    assert not hasattr(result, "extra_field_from_api")

    mock_cep_repository.create_cep.assert_called_once()
    call_args_dict = mock_cep_repository.create_cep.call_args[0][1]
    assert "extra_field_from_api" not in call_args_dict
    assert "another_extra" not in call_args_dict
    assert call_args_dict["logradouro"] == "Rua Teste"
