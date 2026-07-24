from pdf2image import convert_from_path

import pytesseract


class PDFOCR:

    @staticmethod
    def extract_text(file_path):

        try:

            pages = convert_from_path(
                file_path
            )

            text = ""

            for page in pages:

                page_text = pytesseract.image_to_string(
                    page
                )

                text += page_text + "\n"

            return text

        except Exception as e:

            return f"Unable to process PDF: {str(e)}"