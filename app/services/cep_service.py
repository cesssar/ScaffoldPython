from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.interfaces.cep_api_service_interface import ICEPAPIService
from app.interfaces.cep_repository_interface import ICEPRepository
from app.models.cep import CEP

logger = logging.getLogger(__name__)


class CEPService:
    def __init__(
        self,
        db_session: Session,
        api_service: ICEPAPIService,
        cep_repository: ICEPRepository,
    ):
        self.db_session = db_session
        self.api_service = api_service
        self.cep_repository = cep_repository

    def get_or_fetch_cep_details(self, cep_str: str) -> Optional[CEP]:
        # Limpeza dos dados
        sanitized_cep = "".join(filter(str.isdigit, cep_str))
        if len(sanitized_cep) != 8:
            logger.warning(f"CEP inválido: {cep_str} -> {sanitized_cep}")
            return None

        # 1. tentar recuperar o CEP do repositório local
        logger.info(f"Tentando localizar CEP {sanitized_cep} da base local.")
        local_cep = self.cep_repository.get_cep(self.db_session, sanitized_cep)
        if local_cep:
            logger.info(f"CEP {sanitized_cep} encontrado na base local.")
            return local_cep

        logger.info(f"CEP {sanitized_cep} não encontrado na base local.")

        # 2. tentar recuperar o CEP de uma API externa
        external_cep = self.api_service.fetch_cep_data(sanitized_cep)

        if not external_cep:
            logger.warning(f"CEP {sanitized_cep} não encontrado na API.")
            return None

        # 3. dado retornado pela API, tentar salvar no repositório local
        try:
            external_cep["cep"] = "".join(
                filter(str.isdigit, external_cep.get("cep", ""))
            )

            model_fields = {column.name for column in CEP.__table__.columns}
            filtered_cep_data = {
                k: v for k, v in external_cep.items() if k in model_fields
            }

            logger.info(f"CEP {sanitized_cep} encontrado na API externa.")
            new_cep = self.cep_repository.create_cep(
                self.db_session,
                filtered_cep_data
            )
            if new_cep:
                logger.info(f"CEP {sanitized_cep} salvo.")
                return new_cep
            else:
                logger.error(f"Falha ao salvar os dados {sanitized_cep}.")
                return None
        except Exception as e:
            logger.error(f"Erro ao processar CEP {sanitized_cep}: {e}")
            return None
