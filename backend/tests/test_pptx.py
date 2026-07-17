from app.services.parsers.pptx_parser import PPTXParser

text = PPTXParser.extract_text(
    "tests/sample.pptx"
)

print(text)