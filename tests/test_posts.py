from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_page_posts():
    response = client.get("/api/v1/pages/deepsolv/posts?limit=5")
    assert response.status_code in [200, 404]

def test_top_posts():
    response = client.get("/api/v1/pages/deepsolv/top-posts")
    assert response.status_code in [200, 404]
