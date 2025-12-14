def test_list_pages(client):
    response = client.get("/api/v1/pages")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data.get("pages"), list)


def test_get_page_details(client):
    response = client.get("/api/v1/pages/google")
    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["id"].lower() == "google"

    assert "name" in data
    assert "industry" in data
    assert "followers" in data
