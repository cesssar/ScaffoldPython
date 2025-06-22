import pytest
from sqlalchemy.orm import Session
from app.repositories.cep_repository import CEPRepository
from app.models.cep import CEP
from app.schemas.cep_schema import CEPSchema


@pytest.fixture
def cep_repository_instance():
    return CEPRepository()


@pytest.fixture
def sample_cep_data():
    return {
        "cep": "87654321",
        "logradouro": "Avenida Principal",
        "complemento": "Sala 303",
        "bairro": "Centro Histórico",
        "localidade": "Cidade Exemplo",
        "uf": "RJ",
        "ibge": "7654321",
        "gia": "4321",
        "ddd": "21",
        "siafi": "4321",
    }


def test_create_cep_success(
    db_session: Session, cep_repository_instance: CEPRepository, sample_cep_data: dict
):
    created_cep = cep_repository_instance.create_cep(db_session, sample_cep_data)

    assert created_cep is not None
    assert created_cep.id is not None
    assert created_cep.cep == sample_cep_data["cep"]
    assert created_cep.logradouro == sample_cep_data["logradouro"]
    assert created_cep.ddd == sample_cep_data["ddd"]
    assert created_cep.siafi == sample_cep_data["siafi"]


def test_get_cep_found(
    db_session: Session, cep_repository_instance: CEPRepository, sample_cep_data: dict
):
    cep_repository_instance.create_cep(db_session, sample_cep_data.copy())
    retrieved_cep = cep_repository_instance.get_cep(db_session, sample_cep_data["cep"])
    assert retrieved_cep is not None
    assert retrieved_cep.cep == sample_cep_data["cep"]
    assert retrieved_cep.logradouro == sample_cep_data["logradouro"]


def test_get_cep_not_found(db_session: Session, cep_repository_instance: CEPRepository):
    retrieved_cep = cep_repository_instance.get_cep(db_session, "00000000")
    assert retrieved_cep is None


def test_create_cep_database_error(
    db_session: Session,
    cep_repository_instance: CEPRepository,
    sample_cep_data: dict,
    mocker,
):
    mocker.patch.object(
        db_session, "commit", side_effect=Exception("Simulated DB error")
    )
    mocker.patch.object(db_session, "rollback")
    created_cep = cep_repository_instance.create_cep(db_session, sample_cep_data)
    assert created_cep is None
    db_session.rollback.assert_called_once()


def test_get_cep_database_error(
    db_session: Session, cep_repository_instance: CEPRepository, mocker
):
    mocker.patch.object(
        db_session, "query", side_effect=Exception("Simulated DB query error")
    )
    retrieved_cep = cep_repository_instance.get_cep(db_session, "12345678")
    assert retrieved_cep is None
