from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from app.models.cep import CEP


class ICEPRepository(ABC):

    @abstractmethod
    def get_cep(self, db: Session, cep: str) -> Optional[CEP]:
        pass

    @abstractmethod
    def create_cep(self, db: Session, cep_data: dict) -> Optional[CEP]:
        pass
