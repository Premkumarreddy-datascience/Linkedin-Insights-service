def test_db_health(client):
    response = client.get("/api/v1/health/db")
    assert response.status_code == 200
    assert response.json()["database"] == "connected"
