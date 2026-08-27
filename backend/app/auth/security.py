"""
===============================================================
Enterprise AI Knowledge Assistant

Authentication Security
===============================================================
"""

from passlib.context import CryptContext


# ==============================================================
# Password Hashing Configuration
# ==============================================================

password_context = CryptContext(

    schemes=[
        "bcrypt"
    ],

    deprecated="auto"

)


# ==============================================================
# Hash Password
# ==============================================================

def hash_password(
    password: str
):

    return password_context.hash(
        password
    )


# ==============================================================
# Verify Password
# ==============================================================

def verify_password(

    plain_password: str,

    hashed_password: str

):

    return password_context.verify(

        plain_password,

        hashed_password

    )