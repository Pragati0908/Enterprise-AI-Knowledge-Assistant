from app.services.text_cleaner import TextCleaner


text = """

Hello!!!    AI Project



Week 4 @@@ OCR ###

"""

cleaned_text = TextCleaner.clean_text(
    text
)

print(cleaned_text)