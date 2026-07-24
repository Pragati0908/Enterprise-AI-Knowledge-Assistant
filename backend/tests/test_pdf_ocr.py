from app.services.ocr.pdf_ocr import PDFOCR


text = PDFOCR.extract_text(

    "tests/scanned.pdf"

)

print(text)