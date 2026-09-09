"""
===============================================================
Enterprise AI Knowledge Assistant

Power BI Analytics Data Exporter
===============================================================

Purpose
-------
Export SQLite analytics tables into CSV files that can be
imported into Microsoft Power BI.

Tables exported
---------------
1. users
2. document_analytics
3. extraction_analytics
4. search_analytics
===============================================================
"""

from pathlib import Path
import sqlite3
import csv


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

DATABASE_PATH = (
    PROJECT_ROOT / "enterprise_ai.db"
)

EXPORT_DIR = (
    PROJECT_ROOT / "powerbi_data"
)


# ==========================================================
# Create Export Directory
# ==========================================================

EXPORT_DIR.mkdir(

    parents=True,

    exist_ok=True

)


# ==========================================================
# Tables to Export
# ==========================================================

TABLES = [

    "users",

    "document_analytics",

    "extraction_analytics",

    "search_analytics"

]


# ==========================================================
# Export Table
# ==========================================================

def export_table(

    connection,

    table_name

):

    print(
        f"Exporting table: {table_name}"
    )


    cursor = connection.cursor()


    # ------------------------------------------------------
    # Read table data
    # ------------------------------------------------------

    cursor.execute(

        f"""
        SELECT *
        FROM {table_name}
        """

    )


    rows = cursor.fetchall()


    # ------------------------------------------------------
    # Read column names
    # ------------------------------------------------------

    column_names = [

        description[0]

        for description
        in cursor.description

    ]


    # ------------------------------------------------------
    # Output CSV
    # ------------------------------------------------------

    output_file = (

        EXPORT_DIR
        / f"{table_name}.csv"

    )


    # ------------------------------------------------------
    # Write CSV
    # ------------------------------------------------------

    with open(

        output_file,

        "w",

        newline="",

        encoding="utf-8-sig"

    ) as csv_file:

        writer = csv.writer(
            csv_file
        )


        # Header

        writer.writerow(
            column_names
        )


        # Data

        writer.writerows(
            rows
        )


    print(

        f"  Rows exported : {len(rows)}"

    )

    print(

        f"  File          : {output_file}"

    )

    print()


# ==========================================================
# Main
# ==========================================================

def main():

    print(
        "======================================================"
    )

    print(
        "Power BI Analytics Data Export"
    )

    print(
        "======================================================"
    )

    print()


    # ------------------------------------------------------
    # Check database
    # ------------------------------------------------------

    if not DATABASE_PATH.exists():

        print(
            "ERROR: SQLite database not found."
        )

        print(

            f"Expected location:"
            f" {DATABASE_PATH}"

        )

        return


    print(
        f"Database: {DATABASE_PATH}"
    )

    print()


    # ------------------------------------------------------
    # Connect SQLite
    # ------------------------------------------------------

    connection = sqlite3.connect(

        DATABASE_PATH

    )


    try:

        # --------------------------------------------------
        # Export tables
        # --------------------------------------------------

        for table_name in TABLES:

            export_table(

                connection,

                table_name

            )


    finally:

        connection.close()


    print(
        "======================================================"
    )

    print(
        "Export completed successfully."
    )

    print(
        "======================================================"
    )


# ==========================================================
# Program Entry
# ==========================================================

if __name__ == "__main__":

    main()