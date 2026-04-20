import pytest
from tests.utils import META_KEYS, USERS_RESPONSE_KEYS, USER_KEYS, USER_WITHOUT_ID_KEYS


def validate_total_pages(data):
    per_page = data["per_page"]
    total = data["total"]
    total_pages = data["total_pages"]
    expected_total_pages = (total + per_page - 1) // per_page
    assert total_pages == expected_total_pages, f"total_pages should be {expected_total_pages} based on total={total} and per_page={per_page}"


def validate_data_length(data):

    per_page = data["per_page"]
    total = data["total"]
    if total < per_page:
        assert len(data["data"]) == total, f"data length {len(data['data'])} should equal total {total} when total < per_page"
    else:
        assert len(data["data"]) == per_page, f"data length {len(data['data'])} should equal per_page {per_page} when total >= per_page"


def test_get_users_list(client):
    response = client.get_users()
    
    assert response.status_code == 200
    data = response.json()
    assert USERS_RESPONSE_KEYS.issubset(data.keys())
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    
    validate_total_pages(data)
    validate_data_length(data)

    for user in data["data"]:
        assert USER_KEYS.issubset(user.keys())

    assert META_KEYS.issubset(data["_meta"].keys())


def test_get_users_by_page(client):
    response = client.get_users(page=2)
    
    assert response.status_code == 200
    data = response.json()
    assert USERS_RESPONSE_KEYS.issubset(data.keys())
    assert data["total_pages"] >= 2, "Need at least 2 total pages to test page 2"
    assert data["page"] == 2
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    
    validate_total_pages(data)
    validate_data_length(data)
    
    for user in data["data"]:
        assert USER_KEYS.issubset(user.keys())
    
    assert META_KEYS.issubset(data["_meta"].keys())


@pytest.mark.parametrize("page,description", [
    (0, "zero page"),
    (-1, "negative page"),
    (999, "very high page"),
    ('a', "non-numerical page"),
])
def test_get_users_invalid_page(client, page, description):
    response = client.get_users(page=page)
    
    assert response.status_code == 200
    data = response.json()
    assert USERS_RESPONSE_KEYS.issubset(data.keys())
    assert data["page"] == 1
    assert isinstance(data["data"], list)


def test_get_users_with_custom_per_page(client):
    response = client.get_users(per_page=3)
    
    assert response.status_code == 200
    data = response.json()
    assert USERS_RESPONSE_KEYS.issubset(data.keys())
    assert data["per_page"] == 3
    assert data["page"] == 1
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    
    validate_total_pages(data)
    validate_data_length(data)
    
    for user in data["data"]:
        assert USER_KEYS.issubset(user.keys())
    
    if "_meta" in data:
        assert META_KEYS.issubset(data["_meta"].keys())


@pytest.mark.parametrize("per_page,description", [
    (0, "zero per_page"),
    (-1, "negative per_page"),
    (999, "very high per_page"),
    ('a', "non-numerical per_page"),
])
def test_get_users_invalid_per_page(client, per_page, description):
    response = client.get_users(per_page=per_page)
    
    assert response.status_code == 200
    data = response.json()
    assert USERS_RESPONSE_KEYS.issubset(data.keys())
    assert isinstance(data["data"], list)


def test_get_users_with_page_and_per_page(client):
    response = client.get_users(page=4, per_page=1)
    
    assert response.status_code == 200
    data = response.json()
    assert USERS_RESPONSE_KEYS.issubset(data.keys())
    assert data["page"] == 4
    assert data["per_page"] == 1
    assert data["total_pages"] >= 4, "Need at least 4 total pages to test page 4"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    
    validate_total_pages(data)
    validate_data_length(data)
    
    for user in data["data"]:
        assert USER_KEYS.issubset(user.keys())
    
    if "_meta" in data:
        assert META_KEYS.issubset(data["_meta"].keys())


def test_get_specific_user_valid(client):
    response = client.get_user(2)
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    user = data["data"]
    assert user["id"] == 2
    assert USER_WITHOUT_ID_KEYS.issubset(user.keys())


@pytest.mark.parametrize("user_id,description", [
    (999, "non-existent id"),
    (0, "zero"),
    ("_", "non-numeric"),
])
def test_get_specific_user_invalid(client, user_id, description):
    response = client.get_user(user_id)
    
    assert response.status_code == 404
    data = response.json()
    assert "data" in data
    assert data["data"] is None
