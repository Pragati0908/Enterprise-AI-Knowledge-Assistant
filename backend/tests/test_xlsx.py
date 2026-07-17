from app.services.parsers.xlsx_parser import XLSXParser

text = XLSXParser.extract_text(
    "tests/sample.xlsx"
)

print(text)