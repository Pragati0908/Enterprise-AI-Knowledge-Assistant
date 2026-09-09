"""
===============================================================
Enterprise AI Knowledge Assistant

Document Upload API

Endpoint
--------
POST /upload/

Responsibilities
----------------
1. Receive uploaded document
2. Validate file type
3. Save document inside extension-specific folder
4. Automatically extract text
5. Automatically clean text
6. Automatically generate chunks
7. Count generated chunks
8. Update document analytics
9. Return upload and processing information
===============================================================
"""

from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile
)

from sqlalchemy.orm import Session

from werkzeug.utils import secure_filename

from app.db.database import get_db

from app.services.document_processing_service import (
    process_document_file
)


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/upload",
    tags=["Document Upload"]
)


# ==========================================================
# Project Paths
# ==========================================================

# File location:
# backend/app/api/endpoints/upload.py
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
# Allowed File Types
# ==========================================================

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "pptx",
    "xlsx"
}


# ==========================================================
# Upload Endpoint
# ==========================================================

@router.post("/")
async def upload_document(

    file: UploadFile = File(...),

    db: Session = Depends(
        get_db
    )

):

    # ======================================================
    # Validate Filename
    # ======================================================

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename received."
        )

    # ======================================================
    # Secure Filename
    # ======================================================

    filename = secure_filename(
        Path(
            file.filename
        ).name
    )

    # ======================================================
    # Validate Filename After Sanitization
    # ======================================================

    if not filename:

        raise HTTPException(
            status_code=400,
            detail="Invalid filename."
        )

    # ======================================================
    # Determine Extension
    # ======================================================

    extension = (
        Path(
            filename
        ).suffix
        .lower()
        .replace(
            ".",
            ""
        )
    )

    # ======================================================
    # Validate File Type
    # ======================================================

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: "
                f"{extension}"
            )
        )

    # ======================================================
    # Create Type-specific Folder
    # ======================================================

    folder_path = (
        UPLOAD_DIR
        / extension
    )

    folder_path.mkdir(
        parents=True,
        exist_ok=True
    )

    # ======================================================
    # Final File Path
    # ======================================================

    file_path = (
        folder_path
        / filename
    )

    # ======================================================
    # Read Uploaded File
    # ======================================================

    contents = await file.read()

    if not contents:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # ======================================================
    # Save File
    # ======================================================

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(contents)

    # ======================================================
    # Automatically Process Document
    # ======================================================

    processing_result = None

    processing_error = None

    try:

        processing_result = process_document_file(

            file_path=file_path,

            filename=filename,

            db=db

        )

    except Exception as error:

        processing_error = str(error)

        print(
            "Document processing failed: "
            f"{processing_error}"
        )

    # ======================================================
    # Prepare Final Response
    # ======================================================

    response = {

        "message":
            "File uploaded successfully.",

        "filename":
            filename,

        "extension":
            extension,

        "file_size_bytes":
            len(contents),

        "saved_to":
            str(
                file_path.resolve()
            ),

        "processing_completed":
            processing_result is not None,

        "total_chunks":
            (
                processing_result["total_chunks"]
                if processing_result is not None
                else 0
            )

    }

    # ======================================================
    # Include Processing Error If Any
    # ======================================================

    if processing_error is not None:

        response["processing_error"] = (
            processing_error
        )

    return response