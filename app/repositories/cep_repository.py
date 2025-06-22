from sqlalchemy.orm import Session
from app.models.cep import CEP
import logging
from typing import Optional
from app.interfaces.cep_repository_interface import ICEPRepository


logger = logging.getLogger(__name__)


class CEPRepository(ICEPRepository):

    def get_cep(self, db: Session, cep: str) -> Optional[CEP]:
        try:
            return db.query(CEP).filter(CEP.cep == cep).first()
        except Exception as e:
            logger.error(f"Erro ao recuperar o CEP {cep} da base: {e}")
            return None

    def create_cep(self, db: Session, cep_data: dict) -> Optional[CEP]:
        try:
            cep_data.pop("id", None)
            db_cep = CEP(**cep_data)
            db.add(db_cep)
            db.commit()
            db.refresh(db_cep)
            return db_cep
        except Exception as e:
            logger.error(f"Erro ao gravar CEP na base {cep_data}: {e}")
            db.rollback()
            return None
