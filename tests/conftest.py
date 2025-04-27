import pytest
from app.database import SessionLocal, Base, engine
from sqlalchemy.orm import Session


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine) -> Session:
    """
    Cria uma sessão de banco de dados para testes
    e faz rollback após cada teste.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
