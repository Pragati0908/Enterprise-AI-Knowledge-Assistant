from app.services.parsers.pdf_parser import PDFParser

text = PDFParser.extract_text(
    "tests/sample.pdf"
)

print(text[:1000])