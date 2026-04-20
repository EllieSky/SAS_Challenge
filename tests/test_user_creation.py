import pytest
from tests.utils import CREATED_USER_KEYS, META_KEYS


def test_create_user(client):
    name = "John Doe"
    job = "Software Engineer"
    response = client.create_user(name, job)
    
    assert response.status_code == 201
    assert response.reason == "Created"
    data = response.json()
    assert CREATED_USER_KEYS.issubset(data.keys())
    
    assert data["name"] == name
    assert data["job"] == job
    assert isinstance(data["id"], int)
    assert isinstance(data["createdAt"], str)
    
    assert "_meta" in data
    assert META_KEYS.issubset(data["_meta"].keys())


@pytest.mark.xfail(reason="reqres.in API does not persist created users")
def test_create_user_persistence(client):
    name = "Jane Smith"
    job = "Data Scientist"
    response = client.create_user(name, job)
    
    assert response.status_code == 201
    data = response.json()
    user_id = data["id"]
    
    get_response = client.get_user(user_id)
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["data"]["id"] == user_id
    assert get_data["data"]["name"] == name
    assert get_data["data"]["job"] == job


@pytest.mark.xfail(reason="reqres.in API does not validate input, returns 201 for invalid data")
@pytest.mark.parametrize("name,job,description,expected_error", [
    ("", "Software Engineer", "empty name", "name"),
    ("John Doe", "", "empty job", "job"),
    ("", "", "empty name and job", "name"),
])
def test_create_user_invalid(client, name, job, description, expected_error):
    response = client.create_user(name, job)
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert expected_error.lower() in data["error"].lower()
