import pytest
import os
from dotenv import load_dotenv
from reqres import ReqResClient

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("BASE_URL")
    if not url:
        pytest.fail("BASE_URL not found in environment variables")
    return url


@pytest.fixture(scope="session")
def client(base_url):
    api_key = os.getenv("API_KEY")
    return ReqResClient(base_url, api_key)


@pytest.fixture(scope="session")
def test_email():
    email = os.getenv("TEST_EMAIL")
    if not email:
        pytest.fail("TEST_EMAIL not found in environment variables")
    return email


@pytest.fixture(scope="session")
def test_password():
    password = os.getenv("TEST_PASSWORD")
    if not password:
        pytest.fail("TEST_PASSWORD not found in environment variables")
    return password
