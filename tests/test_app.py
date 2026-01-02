import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_and_unregister():
    email = "testuser@mergington.edu"
    activity = "Art Club"
    # Réinitialiser la liste des participants pour ce test
    activities[activity]["participants"] = []
    # Inscription
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Double inscription doit échouer
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    # Désinscription
    response3 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response3.status_code == 200
    assert email in response3.json()["message"]
    # Désinscription d'un non-inscrit doit échouer
    response4 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response4.status_code == 404

def test_signup_activity_not_found():
    response = client.post("/activities/UnknownActivity/signup?email=foo@bar.com")
    assert response.status_code == 404

def test_unregister_activity_not_found():
    response = client.delete("/activities/UnknownActivity/unregister?email=foo@bar.com")
    assert response.status_code == 404
