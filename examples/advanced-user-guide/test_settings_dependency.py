from fastapi.testclient import TestClient

from config_dependency import Settings
from .main import app, get_settings

client = TestClient(app)


def get_settings_override():
    """We set a new value for the `admin_email` when creating the new `Settings` object,
    and then we return that new object.
    Then, we can test that it is used.
    """
    return Settings(admin_email="testing_admin@example.com")


app.dependency_overrides[get_settings] = get_settings_override


def test_app():
    response = client.get("/info")
    data = response.json()
    assert data == {
        "app_name": "Awesome API",
        "admin_email": "testing_admin@example.com",
        "items_per_user": 50
    }