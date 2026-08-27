"""
===============================================================

Enterprise AI Knowledge Assistant

Password Security Test

===============================================================
"""

from app.auth.security import (
    hash_password,
    verify_password
)


# ==========================================================
# Password Security Test
# ==========================================================

def test_password_security():

    print("=" * 70)

    print(
        "PASSWORD SECURITY TEST"
    )

    print("=" * 70)

    password = (
        "MySecurePassword123"
    )

    # ------------------------------------------------------
    # Hash Password
    # ------------------------------------------------------

    hashed_password = hash_password(
        password
    )

    print()

    print(
        "Original Password:"
    )

    print(
        password
    )

    print()

    print(
        "Hashed Password:"
    )

    print(
        hashed_password
    )

    # ------------------------------------------------------
    # Verify Correct Password
    # ------------------------------------------------------

    print()

    result = verify_password(
        password,
        hashed_password
    )

    print(
        "Password Verified:",
        result
    )

    assert result is True

    # ------------------------------------------------------
    # Verify Incorrect Password
    # ------------------------------------------------------

    incorrect_result = verify_password(
        "WrongPassword123",
        hashed_password
    )

    print(
        "Incorrect Password Rejected:",
        not incorrect_result
    )

    assert incorrect_result is False

    print()

    print("=" * 70)

    print(
        "TEST PASSED"
    )

    print("=" * 70)


# ==========================================================
# Run Test
# ==========================================================

if __name__ == "__main__":

    test_password_security()