"""
===============================================================
Enterprise AI Knowledge Assistant

Database Models
===============================================================
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Text
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
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


# ==============================================================
# Document Analytics Model
# ==============================================================

class DocumentAnalytics(Base):

    __tablename__ = "document_analytics"

    # ==========================================================
    # Analytics Record ID
    # ==========================================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ==========================================================
    # Document Filename
    # ==========================================================

    filename = Column(
        String,
        nullable=False
    )

    # ==========================================================
    # File Type
    # ==========================================================

    file_type = Column(
        String,
        nullable=True
    )

    # ==========================================================
    # File Size
    # ==========================================================

    file_size = Column(
        Integer,
        nullable=True
    )

    # ==========================================================
    # Total Chunks
    # ==========================================================

    total_chunks = Column(
        Integer,
        default=0
    )

    # ==========================================================
    # Document Creation Time
    # ==========================================================

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


# ==============================================================
# Extraction Analytics Model
# ==============================================================

class ExtractionAnalytics(Base):

    __tablename__ = "extraction_analytics"

    # ==========================================================
    # Analytics Record ID
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
        String,
        nullable=True
    )

    # ==========================================================
    # Extraction Type
    # ==========================================================

    extraction_type = Column(
        String,
        nullable=False
    )

    # ==========================================================
    # Invoice Number
    # ==========================================================

    invoice_number = Column(
        String,
        nullable=True
    )

    # ==========================================================
    # Vendor
    # ==========================================================

    vendor = Column(
        String,
        nullable=True
    )

    # ==========================================================
    # Total Invoice Amount
    # ==========================================================

    total_amount = Column(
        Float,
        nullable=True
    )

    # ==========================================================
    # Extraction Time
    # ==========================================================

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


# ==============================================================
# Search Analytics Model
# ==============================================================

class SearchAnalytics(Base):

    __tablename__ = "search_analytics"

    # ==========================================================
    # Analytics Record ID
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
        String,
        nullable=True
    )

    # ==========================================================
    # Search Query
    # ==========================================================

    query = Column(
        Text,
        nullable=False
    )

    # ==========================================================
    # Search Type
    # ==========================================================

    search_type = Column(
        String,
        nullable=True
    )

    # ==========================================================
    # Top K
    # ==========================================================

    top_k = Column(
        Integer,
        nullable=True
    )

    # ==========================================================
    # Number of Results
    # ==========================================================

    results_count = Column(
        Integer,
        default=0
    )

    # ==========================================================
    # Search Time
    # ==========================================================

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )