from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_pages():
    response = client.get("/api/v1/search/pages?q=goo")
    assert response.status_code == 200
