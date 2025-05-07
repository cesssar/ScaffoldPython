from sqlalchemy.orm import Session
from app.models.cep import CEP
import logging


logger = logging.getLogger(__name__)


class CEPRepository:

    @staticmethod
    def get_cep(db: Session, cep: str):
        try:
            return db.query(CEP).filter(CEP.cep == cep).first()
        except Exception as e:
            logger.error(f'Erro ao recuperar dados do banco de dados: {e}')

    @staticmethod
    def create_cep(db: Session, cep_data: dict):
        try:
            db_cep = CEP(**cep_data)
            db.add(db_cep)
            db.commit()
            db.refresh(db_cep)
            return db_cep
        except Exception as e:
            logger.error(f'Erro ao gravar no banco de dados: {e}')
