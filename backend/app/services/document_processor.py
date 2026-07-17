from pathlib import Path

from app.services.parsers.pdf_parser import PDFParser
from app.services.parsers.docx_parser import DOCXParser
from app.services.parsers.pptx_parser import PPTXParser
from app.services.parsers.xlsx_parser import XLSXParser


class DocumentProcessor:

    @staticmethod
    def extract_text(file_path: str):

        extension = Path(file_path).suffix.lower()

        parsers = {

            ".pdf": PDFParser,

            ".docx": DOCXParser,

            ".pptx": PPTXParser,

            ".xlsx": XLSXParser
        }

        parser = parsers.get(extension)

        if parser is None:

            raise ValueError(

                f"Unsupported file type: {extension}"
            )

        return parser.extract_text(file_path)