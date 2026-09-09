"""
===============================================================
Enterprise AI Knowledge Assistant

Pytest Configuration
===============================================================
"""

import sys
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient


# ============================================================
# Add Backend Directory to Python Path
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parents[1]

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


# ============================================================
# Import FastAPI Application
# ============================================================

from app.main import app


# ============================================================
# Test Client Fixture
# ============================================================

@pytest.fixture(scope="session")
def client():
    """
    Create ONE TestClient for the complete pytest session.

    IMPORTANT:
    Keeping this fixture session-scoped prevents FastAPI startup
    and shutdown events from being executed repeatedly for every
    individual test.

    This is especially important for the Enterprise AI Knowledge
    Assistant because application startup may initialize services
    such as:

        - Database
        - FAISS
        - Metadata
        - Embedding model
        - Search services
        - Other application services
    """

    with TestClient(app) as test_client:
        yield test_client


# ============================================================
# Test User Fixture
# ============================================================

@pytest.fixture(scope="session")
def test_user():
    """
    Generate one unique test user for the complete pytest session.

    A UUID is used so that the username/email does not conflict
    with users created during previous pytest executions.
    """

    unique_id = uuid4().hex[:8]

    return {
        "username": f"testuser_{unique_id}",
        "email": f"testuser_{unique_id}@example.com",
        "password": "Password123",
    }


# ============================================================
# Authentication Fixture
# ============================================================

@pytest.fixture(scope="session")
def auth_headers(client, test_user):
    """
    Register and authenticate one unique test user.

    The resulting Authorization header is reused by all tests
    requiring authentication.

    Example:

        response = client.post(
            "/search",
            headers=auth_headers,
            json=payload,
        )

    Returns:

        {
            "Authorization": "Bearer <access_token>"
        }
    """

    # --------------------------------------------------------
    # Register User
    # --------------------------------------------------------

    register_response = client.post(
        "/auth/register",
        json={
            "username": test_user["username"],
            "email": test_user["email"],
            "password": test_user["password"],
        },
    )

    assert register_response.status_code == 201, (
        "\n"
        "============================================================\n"
        "TEST USER REGISTRATION FAILED\n"
        "============================================================\n"
        f"Status Code : {register_response.status_code}\n"
        f"Response    : {register_response.text}\n"
        f"Username    : {test_user['username']}\n"
        f"Email       : {test_user['email']}\n"
        "============================================================\n"
    )

    # --------------------------------------------------------
    # Login User
    # --------------------------------------------------------

    login_response = client.post(
        "/auth/login",
        json={
            "username": test_user["username"],
            "password": test_user["password"],
        },
    )

    assert login_response.status_code == 200, (
        "\n"
        "============================================================\n"
        "TEST USER LOGIN FAILED\n"
        "============================================================\n"
        f"Status Code : {login_response.status_code}\n"
        f"Response    : {login_response.text}\n"
        f"Username    : {test_user['username']}\n"
        "============================================================\n"
    )

    # --------------------------------------------------------
    # Parse Login Response
    # --------------------------------------------------------

    try:
        login_data = login_response.json()

    except ValueError:
        pytest.fail(
            "\n"
            "============================================================\n"
            "INVALID LOGIN RESPONSE\n"
            "============================================================\n"
            "Login endpoint did not return valid JSON.\n"
            f"Response: {login_response.text}\n"
            "============================================================\n"
        )

    # --------------------------------------------------------
    # Extract Access Token
    # --------------------------------------------------------

    access_token = login_data.get("access_token")

    assert access_token, (
        "\n"
        "============================================================\n"
        "ACCESS TOKEN MISSING\n"
        "============================================================\n"
        "Login response does not contain 'access_token'.\n"
        f"Response JSON: {login_data}\n"
        "============================================================\n"
    )

    # --------------------------------------------------------
    # Validate Token Type
    # --------------------------------------------------------

    token_type = login_data.get("token_type")

    assert token_type == "bearer", (
        "\n"
        "============================================================\n"
        "INVALID TOKEN TYPE\n"
        "============================================================\n"
        "Expected : bearer\n"
        f"Received : {token_type}\n"
        f"Response : {login_data}\n"
        "============================================================\n"
    )

    # --------------------------------------------------------
    # Return Authentication Headers
    # --------------------------------------------------------

    return {
        "Authorization": f"Bearer {access_token}"
    }