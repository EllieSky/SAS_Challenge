# API Test Framework

A lightweight test framework for testing the ReqRes.in API endpoints using pytest.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your credentials
```

Required environment variables:
- `BASE_URL` - API base URL (default: https://reqres.in/api)
- `TEST_EMAIL` - Test email for login
- `TEST_PASSWORD` - Test password for login
- `API_KEY` - API key

3. Run tests:
```bash
pytest tests/ -v
```

For HTML test report:
```bash
pytest tests/ -v --html=test-report.html --self-contained-html
```

## Test Coverage

- **Authentication**: Login success and failure scenarios with parameterized invalid inputs
- **Users**: 
  - Get user list with pagination (page, per_page parameters)
  - Pagination validation logic
  - Get specific user (valid/invalid IDs)
  - Negative tests for invalid page and per_page values
- **User Creation**: 
  - Create new users with validation
  - Negative tests for invalid inputs (empty name/job)
  - User persistence validation
- **User Deletion**: 
  - Delete users by ID
  - Negative tests for invalid user IDs

## Known Failures

The following tests are marked as `xfail` (expected to fail) due to limitations of the reqres.in demo API:

- **test_create_user_invalid**: The reqres.in API does not validate input and returns 201 for invalid data (empty name/job)
- **test_create_user_persistence**: The reqres.in API does not persist created users, so fetching a created user by ID returns 404
- **test_delete_user**: The reqres.in API does not persist deletions, so fetching a deleted user returns 200 instead of 404
- **test_delete_user_invalid**: The reqres.in API returns 204 for any user_id instead of validating input
- **test_get_users_invalid_page**: The reqres.in API does not handle negative or very high page numbers correctly
- **test_get_users_invalid_per_page**: The reqres.in API does not handle negative or very high per_page numbers correctly

## CI/CD

Tests run automatically on GitHub Actions for:
- Push to main/master branches
- Pull requests from any branch

The workflow:
- Uses Python 3.14
- Installs dependencies from requirements.txt
- Creates .env file from GitHub Secrets and Repository Variables
- Runs pytest with HTML report generation
- Uploads test report as an artifact

Required GitHub Secrets:
- `TEST_EMAIL`
- `TEST_PASSWORD`
- `API_KEY`

Required GitHub Repository Variables:
- `BASE_URL`

## Project Structure

```
├── conftest.py              # Test fixtures and configuration (project root)
├── reqres/
│   ├── __init__.py
│   └── client.py            # API client wrapper
├── tests/
│   ├── __init__.py
│   ├── utils.py             # Helper functions and constants
│   ├── test_auth.py         # Authentication tests
│   ├── test_users.py        # User endpoint tests
│   ├── test_user_creation.py # User creation tests
│   └── test_user_deletion.py # User deletion tests
├── .github/
│   └── workflows/
│       └── tests.yml        # GitHub Actions CI workflow
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```
