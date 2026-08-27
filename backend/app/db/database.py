"""
===============================================================
Enterprise AI Knowledge Assistant

Database Configuration
===============================================================
"""

from sqlalchemy import create_engine

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)


# ==============================================================
# Database URL
# ==============================================================

DATABASE_URL = (
    "sqlite:///./enterprise_ai.db"
)


# ==============================================================
# Database Engine
# ==============================================================

engine = create_engine(

    DATABASE_URL,

    connect_args={
        "check_same_thread": False
    }

)


# ==============================================================
# Database Session
# ==============================================================

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)


# ==============================================================
# Base Model
# ==============================================================

Base = declarative_base()


# ==============================================================
# Database Dependency
# ==============================================================

def get_db():

    database = SessionLocal()

    try:

        yield database

    finally:

        database.close()