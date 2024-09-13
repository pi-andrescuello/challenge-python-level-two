from app.schemas.client import ClientSchema
from fastapi import APIRouter
router = APIRouter()

@router.get("/client", response_model=ClientSchema)
def get_client() -> ClientSchema:
    return ClientSchema(name="John Doe", email="john.doe@example.com")