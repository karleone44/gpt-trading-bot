# dashboard/app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI()

class Metrics(BaseModel):
    profitability: float
    drawdown: float
    latency_ms: float
    open_positions: int

# Внутрішнє сховище для демо
_last_run: Metrics = None

@app.post("/metrics", response_model=Metrics)
def post_metrics(metrics: Metrics):
    """Приймає та зберігає метрики з Orchestrator."""
    global _last_run
    _last_run = metrics
    return metrics

@app.get("/metrics", response_model=Metrics)
def get_metrics():
    """Повертає останні збережені метрики."""
    if _last_run is None:
        raise HTTPException(status_code=404, detail="No metrics available")
    return _last_run

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": time.time()}
