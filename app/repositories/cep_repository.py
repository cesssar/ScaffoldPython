from sqlalchemy.orm import Session
from app.models.cep import CEP


class CEPRepository:

    @staticmethod
    def get_cep(db: Session, cep: str):
        return db.query(CEP).filter(CEP.cep == cep).first()

    @staticmethod
    def create_cep(db: Session, cep_data: dict):
        db_cep = CEP(**cep_data)
        db.add(db_cep)
        db.commit()
        db.refresh(db_cep)
        return db_cep
