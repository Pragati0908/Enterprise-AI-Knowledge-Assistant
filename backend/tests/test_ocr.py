from app.services.ocr.image_ocr import ImageOCR


text = ImageOCR.extract_text(

    "tests/sample.png"

)

print(text)