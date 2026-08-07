from pathlib import Path

from fastapi import APIRouter
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile

from werkzeug.utils import secure_filename


router = APIRouter(
    prefix="/upload",
    tags=["Document Upload"]
)

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[4]

UPLOAD_DIR = PROJECT_ROOT / "backend" / "uploads"

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
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename received."
        )

    filename = secure_filename(file.filename)

    extension = filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}"
        )

    folder_path = UPLOAD_DIR / extension

    folder_path.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = folder_path / filename

    contents = await file.read()

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(contents)

    return {

        "message": "File uploaded successfully.",

        "filename": filename,

        "extension": extension,

        "file_size_bytes": len(contents),

        "saved_to": str(file_path.resolve())

    }