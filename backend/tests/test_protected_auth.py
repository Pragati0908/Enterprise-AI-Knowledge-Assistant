"""
===============================================================
Enterprise AI Knowledge Assistant

Protected Authentication Test
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
# Protected Route Test
# ==========================================================

def test_protected_route():

    print()

    print("=" * 70)

    print(
        "PROTECTED ROUTE TEST"
    )

    print("=" * 70)


    # ==========================================================
    # Generate Unique Test User
    # ==========================================================

    unique_id = uuid4().hex[:8]

    username = (
        f"protected_test_{unique_id}"
    )

    email = (
        f"protected_test_{unique_id}@example.com"
    )

    password = (
        "Password123"
    )


    # ==========================================================
    # Register Test User
    # ==========================================================

    register_response = client.post(

        "/auth/register",

        json={

            "username":
                username,

            "email":
                email,

            "password":
                password

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


    # ==========================================================
    # Login
    # ==========================================================

    login_response = client.post(

        "/auth/login",

        json={

            "username":
                username,

            "password":
                password

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


    assert (
        login_response.status_code
        == 200
    )


    # ==========================================================
    # Extract JWT Token
    # ==========================================================

    login_data = (
        login_response.json()
    )

    token = (
        login_data[
            "access_token"
        ]
    )


    print()

    print(
        "JWT Token Generated:"
    )

    print(
        token[:30] + "..."
    )


    # ==========================================================
    # Authorization Header
    # ==========================================================

    headers = {

        "Authorization":
            f"Bearer {token}"

    }


    # ==========================================================
    # Protected Extraction Request
    # ==========================================================

    response = client.post(

        "/extraction",

        json={

            "text":
                "Invoice Number: INV-5001. "
                "Total: ₹7000.",

            "extraction_type":
                "invoice"

        },

        headers=headers

    )


    # ==========================================================
    # Display Result
    # ==========================================================

    print()

    print(
        "Protected Route Status Code:"
    )

    print(
        response.status_code
    )

    print()

    print(
        "Protected Route Response:"
    )

    print(
        response.json()
    )


    # ==========================================================
    # Assertions
    # ==========================================================

    assert (
        response.status_code
        == 200
    )

    response_data = (
        response.json()
    )

    assert (
        response_data[
            "success"
        ]
        is True
    )


    print()

    print("=" * 70)

    print(
        "TEST PASSED"
    )

    print("=" * 70)


# ==========================================================
# Run Test Directly
# ==========================================================

if __name__ == "__main__":

    test_protected_route()