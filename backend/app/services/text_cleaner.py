import re


class TextCleaner:

    @staticmethod
    def remove_extra_spaces(text):

        lines = text.splitlines()

        cleaned_lines = [

        re.sub(

            r"[ \t]+",

            " ",

            line

        ).strip()

        for line in lines
  ]

        return "\n".join(cleaned_lines)

    @staticmethod
    def remove_blank_lines(text):

        return re.sub(

        r"\n{3,}",

        "\n\n",

        text

       )

    @staticmethod
    def remove_special_characters(text):

        return re.sub(

            r"[^\w\s.,!?-]",

            "",

            text

        )

    @staticmethod
    def clean_text(text):

        text = TextCleaner.remove_extra_spaces(
            text
        )

        text = TextCleaner.remove_blank_lines(
            text
        )

        text = TextCleaner.remove_special_characters(
            text
        )

        return text