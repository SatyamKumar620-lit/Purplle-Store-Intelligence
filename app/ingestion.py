# ingestion.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"]
)

@router.get("/")
def get_ingestion():
    return {"message": "Ingestion API"}