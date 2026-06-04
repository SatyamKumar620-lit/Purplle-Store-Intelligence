from fastapi import APIRouter
from pipeline.analytics import calculate_metrics

router = APIRouter()


@router.get("/analytics")
def analytics():

    return calculate_metrics()