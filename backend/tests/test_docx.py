from app.services.parsers.docx_parser import DOCXParser

text = DOCXParser.extract_text(
    "tests/sample.docx"
)

print(text)