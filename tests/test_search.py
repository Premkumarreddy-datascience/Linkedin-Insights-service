def test_search_employees(client):
    response = client.get(
        "/api/v1/pages/google/employees/search?name=Rahul"
    )
    assert response.status_code == 200

    data = response.json()
    assert "page_id" in data
    assert data["page_id"] == "google"
    assert "employees" in data
    assert isinstance(data["employees"], list)
