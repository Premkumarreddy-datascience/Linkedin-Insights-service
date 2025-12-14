from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_pages():
    response = client.get("/api/v1/pages?page=1&limit=5")
    assert response.status_code == 200
    assert "pages" in response.json()

def test_get_page_details():
    response = client.get("/api/v1/pages/deepsolv")
    assert response.status_code in [200, 404]

def test_pages_filter():
    response = client.get("/api/v1/pages?industry=Technology")
    assert response.status_code == 200
