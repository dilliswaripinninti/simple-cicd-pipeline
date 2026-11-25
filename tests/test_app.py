import pytest

from app import APP_VERSION, app as flask_app


@pytest.fixture()
def client():
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as test_client:
        yield test_client


def test_home_page_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.content_type


def test_home_page_shows_title_and_version(client):
    html = client.get("/").get_data(as_text=True)
    assert "Simple CI/CD Pipeline" in html
    assert APP_VERSION in html


def test_health_endpoint_returns_healthy(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_api_status_returns_200_and_json(client):
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.is_json


def test_api_status_expected_data(client):
    data = client.get("/api/status").get_json()
    assert data["status"] == "ok"
    assert data["service"] == "simple-cicd-pipeline"
    assert data["version"] == APP_VERSION
    assert data["environment"] in {"Local", "Render"}
    assert isinstance(data["uptime_seconds"], int)
    assert data["uptime_seconds"] >= 0
    assert "timestamp" in data


def test_invalid_route_returns_404_page(client):
    response = client.get("/does-not-exist")
    assert response.status_code == 404
    assert "text/html" in response.content_type


def test_invalid_api_route_returns_json_404(client):
    response = client.get("/api/unknown")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Not found"


def test_health_rejects_post(client):
    assert client.post("/health").status_code == 405
