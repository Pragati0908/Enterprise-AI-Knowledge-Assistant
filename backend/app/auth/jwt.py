"""
===============================================================
Enterprise AI Knowledge Assistant

JWT Authentication
===============================================================
"""

from datetime import (
    datetime,
    timedelta,
    timezone
)

from jose import jwt


# ==========================================================
# JWT Configuration
# ==========================================================

SECRET_KEY = (
    "CHANGE_THIS_TO_A_LONG_RANDOM_SECRET_KEY"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ==========================================================
# Create Access Token
# ==========================================================

def create_access_token(
    data: dict
) -> str:

    payload = data.copy()

    expire = (
        datetime.now(
            timezone.utc
        )
        +
        timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload.update(
        {
            "exp": expire
        }
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )