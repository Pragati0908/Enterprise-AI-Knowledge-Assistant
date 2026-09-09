"""
===============================================================
Enterprise AI Knowledge Assistant

Document Processing Service

Responsibilities
----------------
1. Extract document text
2. Clean extracted text
3. Generate text chunks
4. Count generated chunks
5. Update or create document analytics
===============================================================
"""

from pathlib import Path

from sqlalchemy.orm import Session

from app.services.document_processor import DocumentProcessor
from app.services.ocr_service import OCRService
from app.services.text_cleaner import TextCleaner
from app.services.chunker import TextChunker
from app.services.analytics_service import AnalyticsService


# ==========================================================
# Supported File Types
# ==========================================================

SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
}


# ==========================================================
# Extract and Clean Text
# ==========================================================

def extract_and_clean_text(
    file_path: Path,
) -> str:
    """
    Extract and clean text using the appropriate method.

    Images -> OCR
    PDF    -> Document Parser; if almost empty, use OCR
    DOCX   -> Document Parser
    PPTX   -> Document Parser
    XLSX   -> Document Parser
    """

    extension = file_path.suffix.lower()

    extracted_text = ""

    # ------------------------------------------------------
    # Validate file extension
    # ------------------------------------------------------

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    # ------------------------------------------------------
    # Images
    # ------------------------------------------------------

    if extension in {
        ".png",
        ".jpg",
        ".jpeg",
    }:
        extracted_text = OCRService.extract_text(
            str(file_path)
        )

    # ------------------------------------------------------
    # PDF
    # ------------------------------------------------------

    elif extension == ".pdf":

        try:
            extracted_text = (
                DocumentProcessor.extract_text(
                    str(file_path)
                )
            )

        except Exception:
            extracted_text = ""

        # --------------------------------------------------
        # OCR fallback for scanned PDFs
        # --------------------------------------------------

        if len(extracted_text.strip()) < 20:
            extracted_text = OCRService.extract_text(
                str(file_path)
            )

    # ------------------------------------------------------
    # Office Documents
    # ------------------------------------------------------

    elif extension in {
        ".docx",
        ".pptx",
        ".xlsx",
    }:
        extracted_text = (
            DocumentProcessor.extract_text(
                str(file_path)
            )
        )

    # ------------------------------------------------------
    # Clean Extracted Text
    # ------------------------------------------------------

    cleaned_text = TextCleaner.clean_text(
        extracted_text
    )

    return cleaned_text


# ==========================================================
# Record or Update Analytics
# ==========================================================

def record_document_analytics(
    db: Session,
    file_path: Path,
    filename: str,
    total_chunks: int,
):
    """
    Create or update document analytics.

    If an analytics record already exists for the filename,
    the latest record is updated.

    If no matching record exists, a new record is created.
    """

    # ------------------------------------------------------
    # Determine file type
    # ------------------------------------------------------

    file_type = (
        file_path.suffix
        .lower()
        .replace(
            ".",
            "",
        )
    )

    # ------------------------------------------------------
    # Create or update analytics
    # ------------------------------------------------------

    analytics_record = (
        AnalyticsService.create_or_update_document(
            db=db,
            filename=filename,
            file_type=file_type,
            file_size=file_path.stat().st_size,
            total_chunks=total_chunks,
        )
    )

    return {
        "analytics_id": analytics_record.id,
        "filename": analytics_record.filename,
        "file_type": analytics_record.file_type,
        "file_size": analytics_record.file_size,
        "total_chunks": analytics_record.total_chunks,
    }


# ==========================================================
# Process Saved Document
# ==========================================================

def process_document_file(
    file_path: Path,
    filename: str,
    db: Session,
):
    """
    Complete document-processing pipeline.

    Extract text
        ↓
    Clean text
        ↓
    Generate chunks
        ↓
    Count chunks
        ↓
    Create or update document analytics
        ↓
    Return processing result
    """

    # ------------------------------------------------------
    # Validate file existence
    # ------------------------------------------------------

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"Provided path is not a file: {file_path}"
        )

    # ------------------------------------------------------
    # Validate file extension
    # ------------------------------------------------------

    extension = file_path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    # ------------------------------------------------------
    # Extract and clean text
    # ------------------------------------------------------

    cleaned_text = extract_and_clean_text(
        file_path=file_path
    )

    if not cleaned_text:
        raise ValueError(
            "No text could be extracted "
            "from the document."
        )

    if not cleaned_text.strip():
        raise ValueError(
            "Extracted text is empty after cleaning."
        )

    # ------------------------------------------------------
    # Generate text chunks
    # ------------------------------------------------------

    chunks = TextChunker.chunk_text(
        text=cleaned_text,
        source=filename,
        chunk_size=500,
        overlap=100,
    )

    # ------------------------------------------------------
    # Calculate actual chunk count
    # ------------------------------------------------------

    total_chunks = len(chunks)

    # ------------------------------------------------------
    # Create or update document analytics
    # ------------------------------------------------------

    analytics_result = record_document_analytics(
        db=db,
        file_path=file_path,
        filename=filename,
        total_chunks=total_chunks,
    )

    # ------------------------------------------------------
    # Return complete processing result
    # ------------------------------------------------------

    return {
        "filename": filename,
        "characters": len(cleaned_text),
        "total_chunks": total_chunks,
        "chunks": chunks,
        "analytics_id": analytics_result["analytics_id"],
        "analytics": analytics_result,
    }