import pytest


@pytest.mark.xfail(reason="reqres.in API does not persist deletions, user still fetchable after delete")
def test_delete_user(client):
    users_response = client.get_users()
    users_data = users_response.json()
    first_user_id = users_data["data"][0]["id"]
    
    response = client.delete_user(first_user_id)
    
    assert response.status_code == 204

    get_response = client.get_user(first_user_id)
    assert get_response.status_code == 404, "Fetching deleted user should return 404 Not Found"
    get_data = get_response.json()
    assert get_data["data"] is None, "Deleted user data should be null"


@pytest.mark.xfail(reason="reqres.in API does not validate input, returns 204 for any user_id")
@pytest.mark.parametrize("user_id,description", [
    (999, "non-existent id"),
    ("", "blank"),
    (0, "zero"),
    ("_", "non-numeric"),
])
def test_delete_user_invalid(client, user_id, description):
    response = client.delete_user(user_id)

    assert response.status_code == 404, "Deleting invalid user should return 404 Not Found"
