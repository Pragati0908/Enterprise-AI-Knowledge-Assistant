"""
===============================================================
Enterprise AI Knowledge Assistant

Analytics Service
===============================================================
"""

from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import (
    DocumentAnalytics,
    ExtractionAnalytics,
    SearchAnalytics,
)


# ==========================================================
# Analytics Service
# ==========================================================

class AnalyticsService:

    # ======================================================
    # Record Document
    # ======================================================

    @staticmethod
    def record_document(
        db: Session,
        filename: str,
        file_type: str,
        file_size: int,
        total_chunks: int = 0,
    ) -> DocumentAnalytics:
        """
        Create a new document analytics record.

        Parameters
        ----------
        db : Session
            SQLAlchemy database session.

        filename : str
            Name of the uploaded document.

        file_type : str
            File extension or document type.

        file_size : int
            File size in bytes.

        total_chunks : int
            Number of chunks generated from the document.
        """

        try:
            analytics_record = DocumentAnalytics(
                filename=filename,
                file_type=file_type,
                file_size=file_size,
                total_chunks=total_chunks,
            )

            db.add(analytics_record)
            db.commit()
            db.refresh(analytics_record)

            return analytics_record

        except SQLAlchemyError:
            db.rollback()
            raise

    # ======================================================
    # Update Document Chunks
    # ======================================================

    @staticmethod
    def update_document_chunks(
        db: Session,
        filename: str,
        total_chunks: int,
    ) -> Optional[DocumentAnalytics]:
        """
        Update the latest analytics record for a document.

        If a matching record does not exist, None is returned.
        The caller can then create a new analytics record.

        Parameters
        ----------
        db : Session
            SQLAlchemy database session.

        filename : str
            Name of the processed document.

        total_chunks : int
            Number of chunks generated from the document.
        """

        try:
            record = (
                db.query(DocumentAnalytics)
                .filter(
                    func.lower(DocumentAnalytics.filename)
                    == filename.strip().lower()
                )
                .order_by(
                    DocumentAnalytics.id.desc()
                )
                .first()
            )

            if record is None:
                return None

            record.total_chunks = max(0, int(total_chunks))

            db.commit()
            db.refresh(record)

            return record

        except SQLAlchemyError:
            db.rollback()
            raise

    # ======================================================
    # Create Or Update Document Analytics
    # ======================================================

    @staticmethod
    def create_or_update_document(
        db: Session,
        filename: str,
        file_type: str,
        file_size: int,
        total_chunks: int = 0,
    ) -> DocumentAnalytics:
        """
        Create a new document analytics record or update the
        latest existing record for the same filename.

        This method is useful when the same document is uploaded
        and processed more than once.
        """

        try:
            record = (
                db.query(DocumentAnalytics)
                .filter(
                    func.lower(DocumentAnalytics.filename)
                    == filename.strip().lower()
                )
                .order_by(
                    DocumentAnalytics.id.desc()
                )
                .first()
            )

            if record is None:
                record = DocumentAnalytics(
                    filename=filename,
                    file_type=file_type,
                    file_size=file_size,
                    total_chunks=max(0, int(total_chunks)),
                )

                db.add(record)

            else:
                record.file_type = file_type
                record.file_size = file_size
                record.total_chunks = max(0, int(total_chunks))

            db.commit()
            db.refresh(record)

            return record

        except SQLAlchemyError:
            db.rollback()
            raise

    # ======================================================
    # Record Extraction
    # ======================================================

    @staticmethod
    def record_extraction(
        db: Session,
        username: str,
        extraction_type: str,
        invoice_number: Optional[str] = None,
        vendor: Optional[str] = None,
        total_amount: Optional[float] = None,
    ) -> ExtractionAnalytics:
        """
        Record document or invoice extraction analytics.
        """

        try:
            analytics_record = ExtractionAnalytics(
                username=username,
                extraction_type=extraction_type,
                invoice_number=invoice_number,
                vendor=vendor,
                total_amount=total_amount,
            )

            db.add(analytics_record)
            db.commit()
            db.refresh(analytics_record)

            return analytics_record

        except SQLAlchemyError:
            db.rollback()
            raise

    # ======================================================
    # Record Search
    # ======================================================

    @staticmethod
    def record_search(
        db: Session,
        username: str,
        query: str,
        search_type: str,
        top_k: int,
        results_count: int,
    ) -> SearchAnalytics:
        """
        Record search analytics.
        """

        try:
            analytics_record = SearchAnalytics(
                username=username,
                query=query,
                search_type=search_type,
                top_k=top_k,
                results_count=results_count,
            )

            db.add(analytics_record)
            db.commit()
            db.refresh(analytics_record)

            return analytics_record

        except SQLAlchemyError:
            db.rollback()
            raise