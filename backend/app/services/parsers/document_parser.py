from pathlib import Path

from app.services.parsers.pdf_parser import PDFParser
from app.services.parsers.docx_parser import DOCXParser
from app.services.parsers.pptx_parser import PPTXParser
from app.services.parsers.xlsx_parser import XLSXParser


class DocumentParser:
    """
    Unified parser for all supported document types.

    Supported formats:
        • PDF
        • DOCX
        • PPTX
        • XLSX

    Usage:

        text = DocumentParser.extract_text(file_path)

    or

        text = DocumentParser.parse_document(file_path)
    """

    # ======================================================
    # Parse Document
    # ======================================================

    @staticmethod
    def parse_document(file_path: str) -> str:
        """
        Main parsing function used throughout the project.
        """

        return DocumentParser.extract_text(file_path)

    # ======================================================
    # Extract Text
    # ======================================================

    @staticmethod
    def extract_text(file_path: str) -> str:

        path = Path(file_path)

        if not path.exists():

            raise FileNotFoundError(
                f"Document not found: {path}"
            )

        extension = path.suffix.lower()

        # --------------------------------------------------
        # PDF
        # --------------------------------------------------

        if extension == ".pdf":

            return PDFParser.extract_text(
                str(path)
            )

        # --------------------------------------------------
        # DOCX
        # --------------------------------------------------

        elif extension == ".docx":

            return DOCXParser.extract_text(
                str(path)
            )

        # --------------------------------------------------
        # PPTX
        # --------------------------------------------------

        elif extension == ".pptx":

            return PPTXParser.extract_text(
                str(path)
            )

        # --------------------------------------------------
        # XLSX
        # --------------------------------------------------

        elif extension == ".xlsx":

            return XLSXParser.extract_text(
                str(path)
            )

        # --------------------------------------------------
        # Unsupported File
        # --------------------------------------------------

        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    # ======================================================
    # Supported Extensions
    # ======================================================

    @staticmethod
    def supported_extensions():

        return [
            ".pdf",
            ".docx",
            ".pptx",
            ".xlsx"
        ]

    # ======================================================
    # Check Supported File
    # ======================================================

    @staticmethod
    def is_supported(file_path: str):

        return (
            Path(file_path).suffix.lower()
            in DocumentParser.supported_extensions()
        )