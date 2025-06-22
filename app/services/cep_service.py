from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.interfaces.cep_api_service_interface import ICEPAPIService
from app.interfaces.cep_repository_interface import ICEPRepository
from app.models.cep import CEP
from app.schemas.cep_schema import CEPSchema

logger = logging.getLogger(__name__)

class CEPService:
    def __init__(
        self,
        db_session: Session,
        api_service: ICEPAPIService,
        cep_repository: ICEPRepository,
    ):
        self.db_session = db_session
        self.api_service = api_service
        self.cep_repository = cep_repository

    def get_or_fetch_cep_details(self, cep_str: str) -> Optional[CEP]:
        """
        Gets CEP details, first from the local repository, then from the external API if not found locally.
        If fetched from API, it's saved to the local repository.

        :param cep_str: The CEP string to look up.
        :return: A CEP model instance or None if not found anywhere or an error occurs.
        """
        # Sanitize CEP input: remove non-digits
        sanitized_cep = "".join(filter(str.isdigit, cep_str))
        if len(sanitized_cep) != 8:
            logger.warning(f"Invalid CEP format after sanitization: {cep_str} -> {sanitized_cep}")
            return None

        # 1. Try to get CEP from the local repository
        logger.info(f"Attempting to retrieve CEP {sanitized_cep} from local repository.")
        local_cep = self.cep_repository.get_cep(self.db_session, sanitized_cep)
        if local_cep:
            logger.info(f"CEP {sanitized_cep} found in local repository.")
            return local_cep

        logger.info(f"CEP {sanitized_cep} not found locally, attempting to fetch from external API.")

        # 2. If not found locally, fetch from the external API
        external_cep_data = self.api_service.fetch_cep_data(sanitized_cep)

        if not external_cep_data:
            logger.warning(f"CEP {sanitized_cep} not found in external API or an error occurred.")
            return None

        # 3. If found externally, adapt to schema (if necessary) and save to repository
        try:
            # Validate with CEPSchema to ensure all fields are present,
            # Pydantic will raise validation error if fields are missing or types are wrong.
            # The API returns 'ddd' and 'siafi' as strings, CEPSchema expects int.
            # This might require careful handling or schema adjustment if API is inconsistent.
            # For now, we assume the API returns data that can be coerced or is directly usable.

            # Ensure 'cep' in external_cep_data is sanitized if it comes with hyphen from API
            external_cep_data['cep'] = "".join(filter(str.isdigit, external_cep_data.get('cep', '')))


            # Filter external_cep_data to include only fields expected by CEP model
            # This avoids errors if the API returns extra fields not in the model.
            model_fields = {column.name for column in CEP.__table__.columns}
            filtered_cep_data = {k: v for k, v in external_cep_data.items() if k in model_fields}

            # Ensure all required fields for CEPSchema (and thus potentially for CEP model) are present
            # This is a bit tricky because the model itself doesn't enforce all fields from schema at creation
            # For now, we pass filtered_cep_data, assuming it's sufficient for CEP model.
            # A more robust solution might involve converting to CEPSchema first, then to dict for model.

            logger.info(f"CEP {sanitized_cep} fetched from external API. Saving to local repository.")
            new_cep = self.cep_repository.create_cep(self.db_session, filtered_cep_data)
            if new_cep:
                logger.info(f"CEP {sanitized_cep} successfully saved to local repository.")
                return new_cep
            else:
                logger.error(f"Failed to save CEP {sanitized_cep} (fetched from API) to local repository.")
                return None
        except Exception as e: # Catching broad exception for issues during data processing/saving
            logger.error(f"Error processing or saving CEP data for {sanitized_cep} from external API: {e}")
            return None
