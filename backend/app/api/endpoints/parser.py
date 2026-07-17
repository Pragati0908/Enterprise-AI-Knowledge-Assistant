from fastapi import APIRouter

from app.services.document_processor import DocumentProcessor


router = APIRouter(
    prefix="/parser",
    tags=["Parser"]
)


@router.get("/status")
def status():

    return {
        "message": "Parser service running"
    }


@router.get("/test")
def test_parser():

    files = [
        "tests/sample.pdf",
        "tests/sample.docx",
        "tests/sample.pptx",
        "tests/sample.xlsx"
    ]

    result = {}

    for file in files:

        try:

            text = DocumentProcessor.extract_text(file)

            result[file] = {
                "status": "success",
                "preview": text[:200]
            }

        except Exception as e:

            result[file] = {
                "status": "failed",
                "error": str(e)
            }

    return result