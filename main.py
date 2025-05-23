from app.database import Base, engine, get_db
from app.models.cep import CEP
from app.repositories.cep_repository import CEPRepository
from app.services.api_service import APIService
from app.schemas.cep_schema import CEPSchema
from app.config.logging_config import setup_logging
from sqlalchemy.orm import Session


setup_logging()


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
    except Exception as e:
        print(f"Erro ao consultar o CEP: {e}")
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

    if resultado:
        print('\n')
        print('Dados em formato JSON\n')
        dados_dict = CEPSchema.model_validate(resultado).model_dump_json()
        print(dados_dict)
