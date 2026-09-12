"""
===============================================================
Enterprise AI Knowledge Assistant

Authentication Schemas
===============================================================
"""

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


# ==========================================================
# User Registration
# ==========================================================

class UserCreate(
    BaseModel
):

    username: str = Field(
        min_length=3,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=6
    )


# ==========================================================
# User Login
# ==========================================================

class UserLogin(
    BaseModel
):

    username: str

    password: str


# ==========================================================
# User Response
# ==========================================================

class UserResponse(
    BaseModel
):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    username: str

    email: EmailStr


# ==========================================================
# Authentication Token Response
# ==========================================================

class TokenResponse(
    BaseModel
):

    access_token: str

    token_type: str = "bearer"