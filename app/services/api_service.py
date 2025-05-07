import requests
from app.config.settings import settings
import logging


logger = logging.getLogger(__name__)


class APIService:

    @staticmethod
    def fetch_cep_data(cep: str) -> dict:
        try:
            url = f"{settings.EXTERNAL_API_URL}/{cep}/json/"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return {}
        except Exception as e:
            logger.error(f'Erro ao executar API externa: {e}')
