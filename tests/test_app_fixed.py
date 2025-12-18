from fastapi.testclient import TestClient
import uuid

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    # Use a unique email to avoid test interference
    email = f"test+{uuid.uuid4().hex}@example.com"
    activity = "Basketball Team"

    # Ensure activity exists
    assert activity in activities

    # Signup
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert f"Signed up {email}" in res.json().get("message", "")

    # Verify participant present
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert email in data[activity]["participants"]

    # Attempt duplicate signup -> should fail
    res_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert res_dup.status_code == 400

    # Unregister
    res_del = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res_del.status_code == 200
    assert f"Removed {email}" in res_del.json().get("message", "")

    # Verify participant removed
    res = client.get("/activities")
    data = res.json()
    assert email not in data[activity]["participants"]
