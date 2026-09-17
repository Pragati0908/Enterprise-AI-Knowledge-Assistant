"""
===============================================================
Enterprise AI Knowledge Assistant

Protected Authentication Test
===============================================================
"""

import uuid

from fastapi.testclient import (
    TestClient
)

from app.main import app


client = TestClient(
    app
)


def test_protected_route():

    print()

    print("=" * 70)

    print(
        "PROTECTED ROUTE TEST"
    )

    print("=" * 70)


    # ==========================================================
    # Create a unique test user
    # ==========================================================

    username = (
        f"protected_test_{uuid.uuid4().hex[:8]}"
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


    assert (
        register_response.status_code
        in (200, 201)
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


if __name__ == "__main__":

    test_protected_route()