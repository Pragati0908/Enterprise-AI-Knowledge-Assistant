"""
===============================================================
Enterprise AI Knowledge Assistant

Authentication API Test
===============================================================
"""

from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


# ==========================================================
# Test Client
# ==========================================================

client = TestClient(
    app
)


# ==========================================================
# Authentication API Test
# ==========================================================

def test_authentication():

    print()

    print(
        "=" * 70
    )

    print(
        "AUTHENTICATION API TEST"
    )

    print(
        "=" * 70
    )


    # ------------------------------------------------------
    # Generate Unique User
    # ------------------------------------------------------

    unique_id = uuid4().hex[:8]

    username = (
        f"testuser_{unique_id}"
    )

    email = (
        f"testuser_{unique_id}@example.com"
    )

    password = (
        "Password123"
    )


    # ======================================================
    # Register User
    # ======================================================

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )


    print()

    print(
        "Registration Status:"
    )

    print(
        register_response.status_code
    )


    print()

    print(
        "Registration Response:"
    )

    print(
        register_response.json()
    )


    assert (
        register_response.status_code
        == 201
    )


    # ======================================================
    # Login User
    # ======================================================

    login_response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": password
        }
    )


    print()

    print(
        "Login Status:"
    )

    print(
        login_response.status_code
    )


    print()

    print(
        "Login Response:"
    )

    print(
        login_response.json()
    )


    # ======================================================
    # Validate Login
    # ======================================================

    assert (
        login_response.status_code
        == 200
    )


    data = login_response.json()


    assert (
        "access_token"
        in data
    )


    assert (
        data["token_type"]
        == "bearer"
    )


    print()

    print(
        "=" * 70
    )

    print(
        "TEST PASSED"
    )

    print(
        "=" * 70
    )


# ==========================================================
# Run Test
# ==========================================================

if __name__ == "__main__":

    test_authentication()