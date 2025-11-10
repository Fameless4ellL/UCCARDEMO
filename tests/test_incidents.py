import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_incident():
    response = client.post("/incidents", json={
        "description": "Самокат не в сети",
        "status": "new",
        "source": "operator"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] > 0
    assert data["status"] == "new"
    assert data["source"] == "operator"

def test_get_incidents_by_status():
    # Создаём инцидент со статусом "resolved"
    client.post("/incidents", json={
        "description": "Точка не отвечает",
        "status": "resolved",
        "source": "monitoring"
    })

    response = client.get("/incidents?status=resolved")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(incident["status"] == "resolved" for incident in data)

def test_update_incident_status():
    # Создаём инцидент
    create_resp = client.post("/incidents", json={
        "description": "Отчёт не выгрузился",
        "status": "new",
        "source": "partner"
    })
    incident_id = create_resp.json()["id"]

    # Обновляем статус
    update_resp = client.patch(f"/incidents/{incident_id}", json={"status": "closed"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "closed"

def test_update_nonexistent_incident():
    response = client.patch("/incidents/999999", json={"status": "closed"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Incident not found"
