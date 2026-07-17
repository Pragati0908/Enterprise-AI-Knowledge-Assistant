import pandas as pd


class XLSXParser:

    @staticmethod
    def extract_text(file_path: str):

        sheets = pd.read_excel(
            file_path,
            sheet_name=None
        )

        text = ""

        for sheet_name, dataframe in sheets.items():

            text += f"\n=== {sheet_name} ===\n"

            text += dataframe.to_string()

        return text