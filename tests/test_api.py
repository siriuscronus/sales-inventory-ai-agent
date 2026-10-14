from fastapi.testclient import TestClient

from app.api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy"
    }


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"
    assert data["version"] == "1.0.0"


def test_agent_price_endpoint():
    response = client.post(
        "/agent",
        json={
            "query": (
                "¿Cuánto cuesta el SKU "
                "IJOIST-16-20?"
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["intent"] == "price"
    assert data["model"] == "local-operational-router"
