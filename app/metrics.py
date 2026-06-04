from fastapi import APIRouter

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

@router.get("/")
def get_metrics():
    return {"message": "Metrics API"}