"""
===============================================================
Enterprise AI Knowledge Assistant

Database Models
===============================================================
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime
)

from app.db.database import Base


# ==============================================================
# User Model
# ==============================================================

class User(Base):

    __tablename__ = "users"


    # ==========================================================
    # User ID
    # ==========================================================

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    # ==========================================================
    # Username
    # ==========================================================

    username = Column(

        String(100),

        unique=True,

        nullable=False,

        index=True

    )


    # ==========================================================
    # Email
    # ==========================================================

    email = Column(

        String(255),

        unique=True,

        nullable=False,

        index=True

    )


    # ==========================================================
    # Hashed Password
    # ==========================================================

    hashed_password = Column(

        String(255),

        nullable=False

    )


    # ==========================================================
    # Account Creation Time
    # ==========================================================

    created_at = Column(

        DateTime,

        default=datetime.utcnow,

        nullable=False

    ) 

    