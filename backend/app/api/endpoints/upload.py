from pathlib import Path

from fastapi import APIRouter, UploadFile, File


router = APIRouter(
    prefix="/upload",
    tags=["Document Upload"]
)


UPLOAD_DIR = Path("uploads")


@router.post("/")
async def upload_document(
    file: UploadFile = File(...)
):

    extension = file.filename.split(".")[-1].lower()

    allowed_extensions = [
        "pdf",
        "docx",
        "pptx",
        "xlsx"
    ]

    if extension not in allowed_extensions:

        return {
            "error": "Unsupported file type"
        }

    folder_path = UPLOAD_DIR / extension

    folder_path.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = folder_path / file.filename

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    return {

        "filename": file.filename,

        "extension": extension,

        "saved_to": str(file_path),

        "message": "File uploaded successfully"
    }