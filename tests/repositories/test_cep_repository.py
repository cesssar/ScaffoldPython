import pytest
from sqlalchemy.orm import Session
from app.repositories.cep_repository import CEPRepository
from app.models.cep import CEP
from app.schemas.cep_schema import CEPSchema # For data structure reference


@pytest.fixture
def cep_repository_instance():
    return CEPRepository()

@pytest.fixture
def sample_cep_data():
    return {
        "cep": "87654321", # Different from other tests
        "logradouro": "Avenida Principal",
        "complemento": "Sala 303",
        "bairro": "Centro Histórico",
        "localidade": "Cidade Exemplo",
        "uf": "RJ",
        "ibge": "7654321",
        "gia": "4321",
        "ddd": "21", # Keep as string to match typical API response before schema validation
        "siafi": "4321", # Keep as string
    }

def test_create_cep_success(db_session: Session, cep_repository_instance: CEPRepository, sample_cep_data: dict):
    created_cep = cep_repository_instance.create_cep(db_session, sample_cep_data)

    assert created_cep is not None
    assert created_cep.id is not None # Should have an ID after creation
    assert created_cep.cep == sample_cep_data["cep"]
    assert created_cep.logradouro == sample_cep_data["logradouro"]
    # ... assert other fields ...
    assert created_cep.ddd == sample_cep_data["ddd"] # In the model, these are strings
    assert created_cep.siafi == sample_cep_data["siafi"]

def test_get_cep_found(db_session: Session, cep_repository_instance: CEPRepository, sample_cep_data: dict):
    # First, create a CEP to ensure it exists
    cep_repository_instance.create_cep(db_session, sample_cep_data.copy()) # Use .copy() if data is modified

    retrieved_cep = cep_repository_instance.get_cep(db_session, sample_cep_data["cep"])

    assert retrieved_cep is not None
    assert retrieved_cep.cep == sample_cep_data["cep"]
    assert retrieved_cep.logradouro == sample_cep_data["logradouro"]
    # ... assert other fields ...

def test_get_cep_not_found(db_session: Session, cep_repository_instance: CEPRepository):
    retrieved_cep = cep_repository_instance.get_cep(db_session, "00000000") # A non-existent CEP
    assert retrieved_cep is None

def test_create_cep_database_error(db_session: Session, cep_repository_instance: CEPRepository, sample_cep_data: dict, mocker):
    # Mock db.commit() to raise an exception
    mocker.patch.object(db_session, 'commit', side_effect=Exception("Simulated DB error"))
    mocker.patch.object(db_session, 'rollback') # Ensure rollback is called

    created_cep = cep_repository_instance.create_cep(db_session, sample_cep_data)

    assert created_cep is None
    db_session.rollback.assert_called_once()

def test_get_cep_database_error(db_session: Session, cep_repository_instance: CEPRepository, mocker):
    # Mock db.query() to raise an exception
    mocker.patch.object(db_session, 'query', side_effect=Exception("Simulated DB query error"))

    retrieved_cep = cep_repository_instance.get_cep(db_session, "12345678")
    assert retrieved_cep is None
