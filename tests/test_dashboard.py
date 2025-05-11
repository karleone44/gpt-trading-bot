# tests/test_dashboard.py

import time
from fastapi.testclient import TestClient
import pytest
from dashboard.app import app, Metrics

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert isinstance(data["timestamp"], float)

def test_metrics_endpoints():
    payload = {
        "profitability": 1.23,
        "drawdown": 0.05,
        "latency_ms": 150.5,
        "open_positions": 3
    }
    # POST /metrics
    post = client.post("/metrics", json=payload)
    assert post.status_code == 200
    assert post.json() == payload

    # GET /metrics
    get = client.get("/metrics")
    assert get.status_code == 200
    assert get.json() == payload

@pytest.mark.parametrize("endpoint", ["/metrics", "/health"])
def test_invalid_metrics_get_after_clear(endpoint):
    # Очищаємо внутрішнє сховище
    from dashboard.app import _last_run
    # прямо обнуляємо
    import dashboard.app as mod; mod._last_run = None

    resp = client.get(endpoint)
    if endpoint == "/metrics":
        assert resp.status_code == 404
    else:
        assert resp.status_code == 200
