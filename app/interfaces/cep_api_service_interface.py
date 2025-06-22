from abc import ABC, abstractmethod
from typing import Optional


class ICEPAPIService(ABC):
    @abstractmethod
    def fetch_cep_data(self, cep: str) -> Optional[dict]:
        """
        Fetches CEP data from an external API.

        :param cep: The CEP string to look up.
        :return: A dictionary containing CEP data or None if not found or an error occurs.
        """
        pass
