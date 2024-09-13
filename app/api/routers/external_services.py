from fastapi import APIRouter
router = APIRouter()

@router.get("/external")
def external_service():
    return {"message": "External services endpoint"}