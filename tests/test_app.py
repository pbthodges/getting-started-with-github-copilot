from fastapi.testclient import TestClient

from src.app import activities, app


def test_activities_endpoint_disables_browser_caching():
    client = TestClient(app)

    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"].startswith("no-store")


def test_unregister_participant_removes_participant():
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original_participants = activities[activity_name]["participants"][:]

    try:
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
        assert email not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants
