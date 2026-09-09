"""
===============================================================
Enterprise AI Knowledge Assistant

OCR and Document Processing API

Endpoints
---------
GET  /ocr/status
POST /ocr/extract
POST /ocr/chunk
POST /ocr/process-all

Responsibilities
----------------
1. Extract text from supported documents
2. Use OCR for images and scanned PDFs
3. Clean extracted text
4. Generate text chunks
5. Record the actual number of generated chunks
6. Update document analytics
7. Process all previously uploaded documents
===============================================================
"""

from pathlib import Path
from typing import Tuple

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.services.document_processing_service import (
    process_document_file
)


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/ocr",
    tags=["OCR"]
)


# ==========================================================
# Project Paths
# ==========================================================

# File location:
# backend/app/api/endpoints/ocr.py
#
# parents[0] -> backend/app/api/endpoints
# parents[1] -> backend/app/api
# parents[2] -> backend/app
# parents[3] -> backend
# parents[4] -> project root

PROJECT_ROOT = Path(
    __file__
).resolve().parents[4]

UPLOAD_DIR = (
    PROJECT_ROOT
    / "backend"
    / "uploads"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


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
    ".xlsx"
}


# ==========================================================
# Helper: Get Extension Folder
# ==========================================================

def get_extension_folder(
    filename: str
) -> Path:
    """
    Return the extension-specific upload folder.

    Examples:
        document.pdf -> backend/uploads/pdf
        report.docx  -> backend/uploads/docx
    """

    extension = Path(
        filename
    ).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file format: "
                f"{extension}"
            )
        )

    folder_path = (
        UPLOAD_DIR
        / extension.replace(
            ".",
            ""
        )
    )

    folder_path.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder_path


# ==========================================================
# Helper: Save Uploaded File
# ==========================================================

async def save_uploaded_file(
    file: UploadFile
) -> Tuple[Path, str]:

    # ------------------------------------------------------
    # Validate filename
    # ------------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename received."
        )

    filename = Path(
        file.filename
    ).name

    if not filename:

        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )

    # ------------------------------------------------------
    # Get extension-specific folder
    # ------------------------------------------------------

    folder_path = get_extension_folder(
        filename
    )

    # ------------------------------------------------------
    # Create final file path
    # ------------------------------------------------------

    file_path = (
        folder_path
        / filename
    )

    # ------------------------------------------------------
    # Read uploaded file
    # ------------------------------------------------------

    contents = await file.read()

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # ------------------------------------------------------
    # Save file
    # ------------------------------------------------------

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(contents)

    return file_path, filename


# ==========================================================
# STATUS
# ==========================================================

@router.get("/status")
def ocr_status():

    return {
        "service": "OCR",
        "status": "Running",
        "message": "OCR Service is active."
    }


# ==========================================================
# OCR EXTRACT
# ==========================================================

@router.post("/extract")
async def extract_text(
    file: UploadFile = File(...)
):

    try:

        # --------------------------------------------------
        # Save uploaded file
        # --------------------------------------------------

        file_path, filename = (
            await save_uploaded_file(file)
        )

        # --------------------------------------------------
        # Extract and clean text
        # --------------------------------------------------

        from app.services.document_processing_service import (
            extract_and_clean_text
        )

        cleaned_text = extract_and_clean_text(
            file_path
        )

        # --------------------------------------------------
        # Return extracted text
        # --------------------------------------------------

        return {
            "filename": filename,
            "characters": len(cleaned_text),
            "text": cleaned_text
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ==========================================================
# OCR CHUNK
# ==========================================================

@router.post("/chunk")
async def generate_chunks(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:

        # --------------------------------------------------
        # Save uploaded file
        # --------------------------------------------------

        file_path, filename = (
            await save_uploaded_file(file)
        )

        # --------------------------------------------------
        # Extract, clean, chunk, and update analytics
        # --------------------------------------------------

        result = process_document_file(
            file_path=file_path,
            filename=filename,
            db=db
        )

        # --------------------------------------------------
        # Return response
        # --------------------------------------------------

        return {
            "filename": result["filename"],
            "characters": result["characters"],
            "total_chunks": result["total_chunks"],
            "analytics_recorded": True,
            "chunks": result["chunks"]
        }

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ==========================================================
# PROCESS ALL PREVIOUSLY UPLOADED DOCUMENTS
# ==========================================================

@router.post("/process-all")
def process_all_documents(
    db: Session = Depends(get_db)
):

    processed_documents = []

    failed_documents = []

    # ------------------------------------------------------
    # Process every supported extension folder
    # ------------------------------------------------------

    for extension in SUPPORTED_EXTENSIONS:

        extension_folder = (
            UPLOAD_DIR
            / extension.replace(
                ".",
                ""
            )
        )

        if not extension_folder.exists():

            continue

        # --------------------------------------------------
        # Process files in the extension folder
        # --------------------------------------------------

        for file_path in extension_folder.iterdir():

            if not file_path.is_file():

                continue

            if (
                file_path.suffix.lower()
                not in SUPPORTED_EXTENSIONS
            ):

                continue

            filename = file_path.name

            try:

                result = process_document_file(
                    file_path=file_path,
                    filename=filename,
                    db=db
                )

                processed_documents.append({

                    "filename":
                        result["filename"],

                    "file_type":
                        file_path.suffix
                        .lower()
                        .replace(
                            ".",
                            ""
                        ),

                    "total_chunks":
                        result["total_chunks"],

                    "characters":
                        result["characters"]

                })

            except Exception as error:

                failed_documents.append({

                    "filename":
                        filename,

                    "error":
                        str(error)

                })

    # ------------------------------------------------------
    # Return batch-processing summary
    # ------------------------------------------------------

    return {

        "message":
            "Document processing completed.",

        "upload_directory":
            str(
                UPLOAD_DIR.resolve()
            ),

        "total_files":
            (
                len(processed_documents)
                + len(failed_documents)
            ),

        "processed_files":
            len(processed_documents),

        "failed_files":
            len(failed_documents),

        "processed_documents":
            processed_documents,

        "failed_documents":
            failed_documents

    }