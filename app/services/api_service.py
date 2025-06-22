import requests
from app.config.settings import settings
import logging
from typing import Optional
from app.interfaces.cep_api_service_interface import ICEPAPIService


logger = logging.getLogger(__name__)


class APIService(ICEPAPIService):

    def fetch_cep_data(self, cep: str) -> Optional[dict]:
        try:
            url = f"{settings.EXTERNAL_API_URL}/{cep}/json/"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            data = response.json()
            if data.get("erro"):  # ViaCEP returns {"erro": true} for non-existent CEPs
                logger.info(f"CEP {cep} not found in external API (ViaCEP).")
                return None
            return data
        except requests.exceptions.HTTPError as http_err:
            logger.error(f'HTTP error occurred while fetching CEP {cep}: {http_err} - Response: {response.text}')
            return None
        except requests.exceptions.RequestException as req_err:
            logger.error(f'Request error occurred while fetching CEP {cep}: {req_err}')
            return None
        except Exception as e:
            logger.error(f'An unexpected error occurred while fetching CEP {cep}: {e}')
            return None
