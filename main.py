from app.database import Base, engine, get_db
from app.models.cep import CEP
from app.repositories.cep_repository import CEPRepository
from app.services.api_service import APIService
from sqlalchemy.orm import Session

def init_db():
    Base.metadata.create_all(bind=engine)

def consulta_cep(cep: str) -> CEP:
    """
    Função para consultar um CEP na API e guardar no banco de dados.
    :param cep: O CEP a ser consultado.
    :return: O objeto CEP correspondente ao CEP consultado.
    """
    db = get_db()
    db_session: Session = next(db)
    api = APIService()
    try:
        # Consulta o CEP na API
        cep_data = api.fetch_cep_data(cep)
        # Cria um repositório para o CEP
        cep_repository = CEPRepository()
        # Cria um novo objeto CEP no banco de dados
        new_cep = cep_repository.create_cep(db_session,cep_data)
        return new_cep
    except:
        return CEP()
    finally:
        db_session.close()
        db.close()


if __name__ == "__main__":
    init_db()
    cep = input("Digite o CEP para consulta: ")
    resultado = consulta_cep(cep)
     
    print(f"CEP consultado: {resultado.cep}")
    print(f"Logradouro: {resultado.logradouro}")
    print(f"Bairro: {resultado.bairro}")
    print(f"Cidade: {resultado.localidade}")
    print(f"Estado: {resultado.uf}")
    print(f"IBGE: {resultado.ibge}")
