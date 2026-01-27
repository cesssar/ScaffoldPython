from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.cep_service import CEPService
from app.repositories.cep_repository import CEPRepository
from app.services.api_service import APIService
from app.schemas.cep_schema import CEPSchema

app = FastAPI(title="CEP API")

def get_cep_service(db: Session = Depends(get_db)) -> CEPService:
    return CEPService(
        db_session=db,
        api_service=APIService(),
        cep_repository=CEPRepository()
    )

@app.get("/cep/{cep}", response_model=CEPSchema)
def read_cep(cep: str, service: CEPService = Depends(get_cep_service)):
    result = service.get_or_fetch_cep_details(cep)
    if not result:
        raise HTTPException(status_code=404, detail="CEP not found")
    return result
