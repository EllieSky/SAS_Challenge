import pytest
import os
from tests.utils import META_KEYS


def test_login_success(client):
    email = os.getenv("TEST_EMAIL")
    password = os.getenv("TEST_PASSWORD")
    response = client.login(email, password)
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert isinstance(data["token"], str)
    
    assert "_meta" in data
    assert META_KEYS.issubset(data["_meta"].keys())


@pytest.mark.parametrize(
    "email,password,description,expected_error", [
        (os.getenv("TEST_EMAIL"), "", "empty password", "Missing password"),
        ("", os.getenv("TEST_PASSWORD"), "empty email", "Missing email or username"),
        ("", "", "empty email and password", "Missing email or username"),
        ("invalid-email", "password", "invalid email format", "user not found"),
    ]
)
def test_login_invalid(client, email, password, description, expected_error):
    response = client.login(email, password)
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert expected_error.lower() in data["error"].lower()
