from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_app_health():
    response = client.get("/api/v1/health/app")
    assert response.status_code == 200
    assert response.json()["app"] == "running"

def test_db_health():
    response = client.get("/api/v1/health/db")
    assert response.status_code == 200
    assert response.json()["database"] == "connected"
