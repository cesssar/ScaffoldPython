import logging
from app.database import Base, engine, get_db
from app.repositories.cep_repository import CEPRepository
from app.services.api_service import APIService
from app.services.cep_service import CEPService
from app.schemas.cep_schema import CEPSchema
from app.config.logging_config import setup_logging
from sqlalchemy.orm import Session

# Setup logging first
setup_logging()
logger = logging.getLogger(__name__)


def init_db():
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized.")


def main():
    init_db()

    db_generator = get_db()
    db_session: Session = next(db_generator)

    try:
        # Instantiate concrete implementations
        api_service_instance = APIService()
        cep_repository_instance = CEPRepository()

        # Instantiate CEPService with dependencies
        cep_service = CEPService(
            db_session=db_session,
            api_service=api_service_instance,
            cep_repository=cep_repository_instance
        )

        cep_input = input("Digite o CEP para consulta: ")
        logger.info(f"User input CEP: {cep_input}")

        resultado_cep_model = cep_service.get_or_fetch_cep_details(cep_input)

        if resultado_cep_model:
            logger.info(f"CEP details found for {cep_input}: {resultado_cep_model.__dict__}")
            print("\n--- Detalhes do CEP ---")
            print(f"CEP: {resultado_cep_model.cep}")
            print(f"Logradouro: {resultado_cep_model.logradouro}")
            print(f"Complemento: {resultado_cep_model.complemento}")
            print(f"Bairro: {resultado_cep_model.bairro}")
            print(f"Localidade: {resultado_cep_model.localidade}")
            print(f"UF: {resultado_cep_model.uf}")
            print(f"IBGE: {resultado_cep_model.ibge}")
            print(f"GIA: {resultado_cep_model.gia}")
            print(f"DDD: {resultado_cep_model.ddd}")
            print(f"SIAFI: {resultado_cep_model.siafi}")

            print('\n--- Dados em formato JSON ---')
            # Use the model instance directly for validation if its attributes match schema
            # Or, if necessary, convert model to dict first, then validate
            try:
                cep_schema_validated = CEPSchema.model_validate(resultado_cep_model)
                print(cep_schema_validated.model_dump_json(indent=2))
            except Exception as e:
                logger.error(f"Error validating/serializing CEP model to CEPSchema for {cep_input}: {e}")
                print("Erro ao gerar JSON dos dados do CEP.")

        else:
            logger.warning(f"CEP {cep_input} não encontrado.")
            print(f"CEP {cep_input} não encontrado ou inválido.")

    except Exception as e:
        logger.exception(f"An unexpected error occurred in main execution: {e}")
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        logger.info("Closing database session.")
        db_session.close()


if __name__ == "__main__":
    main()
