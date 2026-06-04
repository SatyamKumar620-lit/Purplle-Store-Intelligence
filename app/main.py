from fastapi import FastAPI

from app.health import router as health_router
from app.analytics import router as analytics_router
from app.metrics import router as metrics_router
from app.anomalies import router as anomalies_router
from app.ingestion import router as ingestion_router

app = FastAPI(
    title="Purplle Store Intelligence API",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(analytics_router)
app.include_router(metrics_router)
app.include_router(anomalies_router)
app.include_router(ingestion_router)