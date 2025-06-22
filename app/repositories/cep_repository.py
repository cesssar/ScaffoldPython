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
            logger.error(f'Error retrieving CEP {cep} from database: {e}')
            return None

    def create_cep(self, db: Session, cep_data: dict) -> Optional[CEP]:
        try:
            # Ensure 'id' is not in cep_data if it's auto-generated
            cep_data.pop('id', None)
            db_cep = CEP(**cep_data)
            db.add(db_cep)
            db.commit()
            db.refresh(db_cep)
            return db_cep
        except Exception as e:
            logger.error(f'Error creating CEP in database with data {cep_data}: {e}')
            db.rollback() # Rollback in case of error
            return None
