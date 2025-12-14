def test_get_recent_posts(client):
    response = client.get("/api/v1/pages/google/posts/recent")
    assert response.status_code == 200

    data = response.json()
    assert "page_id" in data
    assert data["page_id"] == "google"
    assert "recent_posts" in data
    assert isinstance(data["recent_posts"], list)


def test_post_engagement(client):
    response = client.get("/api/v1/pages/google/engagement")
    assert response.status_code == 200

    data = response.json()
    assert "engagement" in data
    assert "total_posts" in data["engagement"]
