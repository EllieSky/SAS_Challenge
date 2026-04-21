import pytest
import os
from tests.utils import META_KEYS


def test_login_success(client):
    email = os.getenv("TEST_EMAIL")
    password = os.getenv("TEST_PASSWORD")
    response = client.login(email, password)
    
    assert response.status_code == 200
    data = response.json()
    assert "token" in data, "Expected token to be present in response"
    assert isinstance(data["token"], str)
    
    assert "_meta" in data
    assert META_KEYS.issubset(data["_meta"].keys())


@pytest.mark.parametrize(
    "email,password,description,expected_error", [
        (lambda test_email: test_email, "", "empty password", "Missing password"),
        ("", "testPassword", "empty email", "Missing email or username"),
        ("", "", "empty email and password", "Missing email or username"),
        ("invalid-email", "password", "invalid email format", "user not found"),
    ]
)
def test_login_invalid(client, email, password, description, expected_error, test_email):
    # Resolve lambda function if needed
    test_email = email(test_email) if callable(email) else email

    response = client.login(test_email, password)
    
    assert response.status_code == 400, "Expected 400 Bad Request for invalid login"
    data = response.json()
    assert "error" in data
    assert expected_error.lower() in data["error"].lower()
