from copy import deepcopy
from fastapi.testclient import TestClient

from src.app import app, activities


def setup_function(function):
    # Make a deep copy of activities before each test to avoid cross-test pollution
    function._activities_backup = deepcopy(activities)


def teardown_function(function):
    # Restore original activities after test
    activities.clear()
    activities.update(function._activities_backup)


def test_get_activities():
    client = TestClient(app)
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_unregister_participant():
    client = TestClient(app)
    activity = "Chess Club"
    test_email = "test_student@mergington.edu"

    # Ensure not already present
    assert test_email not in activities[activity]["participants"]

    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert signup_resp.status_code == 200
    assert test_email in activities[activity]["participants"]

    # Unregister
    del_resp = client.delete(f"/activities/{activity}/participants?email={test_email}")
    assert del_resp.status_code == 200
    assert test_email not in activities[activity]["participants"]
