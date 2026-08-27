"""
===============================================================
Enterprise AI Knowledge Assistant

Authentication Dependencies
===============================================================
"""

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from jose import (
    JWTError,
    jwt
)

from sqlalchemy.orm import Session

from app.auth.jwt import (
    ALGORITHM,
    SECRET_KEY
)

from app.db.database import (
    get_db
)

from app.db.models import (
    User
)


# ==============================================================
# Bearer Authentication
# ==============================================================

security = HTTPBearer()


# ==============================================================
# Get Current User
# ==============================================================

def get_current_user(

    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),

    db: Session = Depends(
        get_db
    )

):

    # ----------------------------------------------------------
    # Extract Token
    # ----------------------------------------------------------

    token = credentials.credentials


    # ----------------------------------------------------------
    # Decode Token
    # ----------------------------------------------------------

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[
                ALGORITHM
            ]

        )

        user_id = payload.get(
            "sub"
        )

    except JWTError:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid authentication token."

        )


    # ----------------------------------------------------------
    # Missing User ID
    # ----------------------------------------------------------

    if not user_id:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid authentication token."

        )


    # ----------------------------------------------------------
    # Find User
    # ----------------------------------------------------------

    try:

        user_id = int(
            user_id
        )

    except (
        TypeError,
        ValueError
    ):

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid authentication token."

        )


    user = db.query(
        User
    ).filter(

        User.id == user_id

    ).first()


    # ----------------------------------------------------------
    # User Not Found
    # ----------------------------------------------------------

    if not user:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="User not found."

        )


    # ----------------------------------------------------------
    # Return Current User
    # ----------------------------------------------------------

    return user