"""
===============================================================
Enterprise AI Knowledge Assistant

Authentication API
===============================================================
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.auth.jwt import (
    create_access_token
)

from app.auth.security import (
    hash_password,
    verify_password
)

from app.auth.dependencies import (
    get_current_user
)

from app.db.database import (
    get_db
)

from app.db.models import (
    User
)

from app.schemas.auth import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse
)


# ==========================================================
# Authentication Router
# ==========================================================

router = APIRouter(
    prefix="/auth",
    tags=[
        "Authentication"
    ]
)


# ==========================================================
# User Registration
# ==========================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(

    user: UserCreate,

    db: Session = Depends(
        get_db
    )

):

    # ------------------------------------------------------
    # Check Existing Username
    # ------------------------------------------------------

    existing_username = (
        db.query(
            User
        )
        .filter(
            User.username == user.username
        )
        .first()
    )

    if existing_username:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists."
        )


    # ------------------------------------------------------
    # Check Existing Email
    # ------------------------------------------------------

    existing_email = (
        db.query(
            User
        )
        .filter(
            User.email == user.email
        )
        .first()
    )

    if existing_email:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )


    # ------------------------------------------------------
    # Hash Password
    # ------------------------------------------------------

    hashed_password = hash_password(
        user.password
    )


    # ------------------------------------------------------
    # Create User Object
    # ------------------------------------------------------

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )


    # ------------------------------------------------------
    # Add User to Database
    # ------------------------------------------------------

    db.add(
        new_user
    )


    # ------------------------------------------------------
    # Commit Transaction
    # ------------------------------------------------------

    db.commit()


    # ------------------------------------------------------
    # Refresh User Object
    # ------------------------------------------------------

    db.refresh(
        new_user
    )


    # ------------------------------------------------------
    # Return Safe User Information
    # ------------------------------------------------------

    return new_user


# ==========================================================
# User Login
# ==========================================================

@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(

    user: UserLogin,

    db: Session = Depends(
        get_db
    )

):

    # ------------------------------------------------------
    # Find User
    # ------------------------------------------------------

    database_user = (
        db.query(
            User
        )
        .filter(
            User.username == user.username
        )
        .first()
    )


    # ------------------------------------------------------
    # Invalid Username
    # ------------------------------------------------------

    if not database_user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )


    # ------------------------------------------------------
    # Verify Password
    # ------------------------------------------------------

    password_valid = verify_password(
        user.password,
        database_user.hashed_password
    )


    if not password_valid:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )


    # ------------------------------------------------------
    # Generate JWT Token
    # ------------------------------------------------------

    access_token = create_access_token(
        {
            "sub": str(
                database_user.id
            )
        }
    )


    # ------------------------------------------------------
    # Return Token
    # ------------------------------------------------------

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==========================================================
# Get Current User
# ==========================================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_logged_in_user(

    current_user: User = Depends(
        get_current_user
    )

):

    return current_user