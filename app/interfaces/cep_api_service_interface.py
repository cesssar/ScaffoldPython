from abc import ABC, abstractmethod
from typing import Optional


class ICEPAPIService(ABC):

    @abstractmethod
    def fetch_cep_data(self, cep: str) -> Optional[dict]:
        pass
