import pytesseract

from PIL import Image


class ImageOCR:

    @staticmethod
    def extract_text(file_path):

        image = Image.open(
            file_path
        )

        text = pytesseract.image_to_string(
            image
        )

        return text