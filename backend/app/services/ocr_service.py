from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image


class OCRService:
    """
    OCR Service

    Supports:
        - Scanned PDF
        - PNG
        - JPG
        - JPEG
    """

    @staticmethod
    def extract_text(file_path: str) -> str:

        file_path = Path(file_path)

        if not file_path.exists():

            raise FileNotFoundError(

                f"File not found: {file_path}"

            )

        extension = file_path.suffix.lower()

        if extension == ".pdf":

            return OCRService.extract_pdf_text(

                file_path

            )

        elif extension in [

            ".png",

            ".jpg",

            ".jpeg"

        ]:

            return OCRService.extract_image_text(

                file_path

            )

        else:

            raise ValueError(

                f"OCR does not support '{extension}' files."

            )

    @staticmethod
    def extract_image_text(image_path: Path) -> str:

        image = Image.open(

            image_path

        )

        text = pytesseract.image_to_string(

            image,

            lang="eng"

        )

        return text

    @staticmethod
    def extract_pdf_text(pdf_path: Path) -> str:

        pages = convert_from_path(

            pdf_path

        )

        extracted_text = ""

        for page_number, page in enumerate(

            pages,

            start=1

        ):

            page_text = pytesseract.image_to_string(

                page,

                lang="eng"

            )

            extracted_text += (

                f"\n----- Page {page_number} -----\n"

            )

            extracted_text += page_text

            extracted_text += "\n"

        return extracted_text