from http import HTTPStatus


def test_health_endpoint_returns_expected_payload(client):
    response = client.get("/health")

    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "feature-flag-hub"
    assert data["version"] == "1.0.0"
