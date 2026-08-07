from pathlib import Path

from fastapi import APIRouter

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[4]

UPLOAD_DIR = PROJECT_ROOT / "backend" / "uploads"

SUPPORTED_EXTENSIONS = [
    "pdf",
    "docx",
    "pptx",
    "xlsx"
]


# ==========================================================
# GET Uploaded Documents
# ==========================================================

@router.get("/")
def get_documents():

    documents = []

    document_id = 1

    for extension in SUPPORTED_EXTENSIONS:

        folder = UPLOAD_DIR / extension

        if not folder.exists():

            continue

        for file in sorted(folder.iterdir()):

            if not file.is_file():

                continue

            documents.append(

                {
                    "id": document_id,
                    "filename": file.name,
                    "extension": extension,
                    "size_kb": round(file.stat().st_size / 1024, 2),
                    "location": str(file)
                }

            )

            document_id += 1

    return {

        "total_documents": len(documents),

        "documents": documents

    }