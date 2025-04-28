import requests
from app.config.settings import settings


class APIService:

    @staticmethod
    def fetch_cep_data(cep: str) -> dict:
        url = f"{settings.EXTERNAL_API_URL}/{cep}/json/"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {}
