# tests/test_dashboard.py

from fastapi.testclient import TestClient
import pytest
from dashboard.app import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert isinstance(data["timestamp"], float)

def test_metrics_endpoints():
    payload = {
        "profitability": 1.23,
        "drawdown": 0.05,
        "latency_ms": 150.5,
        "open_positions": 3
    }
    post_resp = client.post("/metrics", json=payload)
    assert post_resp.status_code == 200
    assert post_resp.json() == payload

    get_resp = client.get("/metrics")
    assert get_resp.status_code == 200
    assert get_resp.json() == payload

@pytest.mark.parametrize("endpoint", ["/metrics", "/health"])
def test_invalid_metrics_get_after_clear(endpoint):
    import dashboard.app as mod
    mod._last_run = None

    resp = client.get(endpoint)
    if endpoint == "/metrics":
        assert resp.status_code == 404
    else:
        assert resp.status_code == 200
