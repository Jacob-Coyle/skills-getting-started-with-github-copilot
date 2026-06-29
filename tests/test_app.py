import copy

from fastapi.testclient import TestClient
from src.app import activities, app

client = TestClient(app)


def test_root_redirects_to_static_index():
    # Arrange
    expected_url = "/static/index.html"

    # Act
    response = client.get("/", allow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_url


def test_get_activities_returns_activity_list():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert "Programming Class" in response.json()


def test_signup_for_activity_adds_participant_and_returns_message():
    # Arrange
    activity_name = "Debate Team"
    email = "student@example.com"
    original_participants = copy.deepcopy(activities[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in activities[activity_name]["participants"]

    # Cleanup
    activities[activity_name]["participants"] = original_participants


def test_signup_for_activity_returns_400_if_already_signed_up():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_signup_for_missing_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@example.com"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
