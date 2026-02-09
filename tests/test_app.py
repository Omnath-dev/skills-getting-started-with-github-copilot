import uuid

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Basic sanity: known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = f"test+{uuid.uuid4().hex}@example.com"

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json().get("message", "")

    # Confirm participant added
    resp2 = client.get("/activities")
    participants = resp2.json()[activity]["participants"]
    assert email in participants

    # Unregister
    resp3 = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert resp3.status_code == 200
    assert f"Unregistered {email}" in resp3.json().get("message", "")

    # Confirm participant removed
    resp4 = client.get("/activities")
    participants2 = resp4.json()[activity]["participants"]
    assert email not in participants2
