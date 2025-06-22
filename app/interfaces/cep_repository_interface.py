from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from app.models.cep import CEP


class ICEPRepository(ABC):
    @abstractmethod
    def get_cep(self, db: Session, cep: str) -> Optional[CEP]:
        """
        Retrieves a CEP record from the database.

        :param db: The SQLAlchemy database session.
        :param cep: The CEP string to look up.
        :return: A CEP model instance or None if not found.
        """
        pass

    @abstractmethod
    def create_cep(self, db: Session, cep_data: dict) -> Optional[CEP]:
        """
        Creates a new CEP record in the database.

        :param db: The SQLAlchemy database session.
        :param cep_data: A dictionary containing the CEP data.
        :return: The created CEP model instance or None if an error occurs.
        """
        pass
