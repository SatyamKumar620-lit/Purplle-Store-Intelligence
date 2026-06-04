# anomalies.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/anomalies",
    tags=["Anomalies"]
)

@router.get("/")
def get_anomalies():
    return {"message": "Anomalies API"}