from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_processor import DocumentProcessor
from app.services.ocr_service import OCRService
from app.services.text_cleaner import TextCleaner
from app.services.chunker import TextChunker


router = APIRouter(
    prefix="/ocr",
    tags=["OCR"]
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def process_uploaded_file(file_path: str, filename: str):
    """
    Extract text using the most appropriate method.

    Images  -> OCR
    PDF     -> Document Parser
               if empty -> OCR
    DOCX    -> Document Parser
    PPTX    -> Document Parser
    XLSX    -> Document Parser
    """

    extension = Path(file_path).suffix.lower()

    # -------------------------
    # Image OCR
    # -------------------------

    if extension in [".png", ".jpg", ".jpeg"]:

        extracted_text = OCRService.extract_text(
            file_path
        )

    # -------------------------
    # PDF
    # -------------------------

    elif extension == ".pdf":

        try:

            extracted_text = DocumentProcessor.extract_text(
                file_path
            )

        except Exception:

            extracted_text = ""

        # If PDF parser extracted almost nothing,
        # assume scanned PDF.

        if len(extracted_text.strip()) < 20:

            extracted_text = OCRService.extract_text(
                file_path
            )

    # -------------------------
    # Office Documents
    # -------------------------

    elif extension in [

        ".docx",

        ".pptx",

        ".xlsx"

    ]:

        extracted_text = DocumentProcessor.extract_text(
            file_path
        )

    else:

        raise HTTPException(

            status_code=400,

            detail="Unsupported file format."

        )

    # -------------------------
    # Clean Text
    # -------------------------

    cleaned_text = TextCleaner.clean_text(

        extracted_text

    )

    return cleaned_text


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

        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:

            buffer.write(

                await file.read()

            )

        cleaned_text = process_uploaded_file(

            str(file_path),

            file.filename

        )

        return {

            "filename": file.filename,

            "characters": len(cleaned_text),

            "text": cleaned_text

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# ==========================================================
# OCR CHUNK
# ==========================================================

@router.post("/chunk")
async def generate_chunks(

    file: UploadFile = File(...)

):

    try:

        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:

            buffer.write(

                await file.read()

            )

        cleaned_text = process_uploaded_file(

            str(file_path),

            file.filename

        )

        chunks = TextChunker.chunk_text(

            text=cleaned_text,

            source=file.filename,

            chunk_size=500,

            overlap=100

        )

        return {

            "filename": file.filename,

            "total_chunks": len(chunks),

            "chunks": chunks

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )