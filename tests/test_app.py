import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball" in data
    assert "participants" in data["Basketball"]

def test_signup_success():
    # Test signing up for an activity
    response = client.post("/activities/Basketball/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]

    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Basketball"]["participants"]

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Soccer/signup?email=duplicate@example.com")
    # Second signup should fail
    response = client.post("/activities/Soccer/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/InvalidActivity/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # First signup
    client.post("/activities/Art Club/signup?email=unregister@example.com")
    # Then unregister
    response = client.delete("/activities/Art Club/unregister?email=unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]

    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@example.com" not in data["Art Club"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Debate Team/unregister?email=notsigned@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_invalid_activity():
    response = client.delete("/activities/InvalidActivity/unregister?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]