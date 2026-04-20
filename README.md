# API Test Framework

A lightweight test framework for testing the ReqRes.in API endpoints using pytest.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get a free API key from [ReqRes.in](https://app.reqres.in/api-keys)

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API key
```

4. Run tests:
```bash
pytest tests/ -v
```

## Test Coverage

- **Authentication**: Login success and failure scenarios
- **Users**: Get user list, get specific user (valid/invalid)
- **User Creation**: Create new users with validation
- **User Deletion**: Delete users and verify response

## Project Structure

```
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures and configuration
│   ├── client.py            # API client wrapper
│   ├── test_auth.py         # Authentication tests
│   ├── test_users.py        # User endpoint tests
│   ├── test_user_creation.py # User creation tests
│   └── test_user_deletion.py # User deletion tests
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```
