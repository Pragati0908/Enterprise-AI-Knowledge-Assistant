"""
===============================================================
Enterprise AI Knowledge Assistant

Extraction Service Tests
===============================================================

Responsibilities
----------------
1. Validate date extraction
2. Validate duplicate date removal
3. Validate complete extraction response
===============================================================
"""

from app.services.extraction_service import (
    ExtractionService
)


# ============================================================
# Test 1 — Date Extraction
# ============================================================

def test_date_extraction():

    text = """
    Invoice Date: 12/08/2026
    Due Date: 25/08/2026
    Agreement Date: 2026-08-30
    Meeting Date: 15 August 2026
    Approval Date: August 20, 2026
    """

    result = ExtractionService.extract_dates(
        text
    )

    print("\n" + "=" * 70)
    print("DATE EXTRACTION TEST")
    print("=" * 70)

    print("\nInput Text:")
    print(text)

    print("\nExtracted Dates:")

    for date in result:

        print(
            f"  - {date}"
        )

    # --------------------------------------------------------
    # Validate Result Type
    # --------------------------------------------------------

    assert isinstance(result, list), (
        "extract_dates() must return a list."
    )

    # --------------------------------------------------------
    # Validate Required Dates
    # --------------------------------------------------------

    expected_dates = [
        "12/08/2026",
        "25/08/2026",
        "2026-08-30",
        "15 August 2026",
        "August 20, 2026",
    ]

    for expected_date in expected_dates:

        assert expected_date in result, (
            f"Expected date '{expected_date}' "
            f"was not found in extracted results.\n"
            f"Actual results: {result}"
        )

    print("\nAll supported date formats detected.")
    print("\nDATE EXTRACTION TEST PASSED")


# ============================================================
# Test 2 — Duplicate Date Removal
# ============================================================

def test_duplicate_date_removal():

    text = """
    Invoice Date: 12/08/2026
    The invoice was generated on 12/08/2026.
    Payment due on 25/08/2026.
    """

    result = ExtractionService.extract_dates(
        text
    )

    print("\n" + "=" * 70)
    print("DUPLICATE DATE REMOVAL TEST")
    print("=" * 70)

    print("\nExtracted Dates:")
    print(result)

    # --------------------------------------------------------
    # Validate Result Type
    # --------------------------------------------------------

    assert isinstance(result, list), (
        "extract_dates() must return a list."
    )

    # --------------------------------------------------------
    # Validate Duplicate Removal
    # --------------------------------------------------------

    assert result.count("12/08/2026") == 1, (
        "Duplicate date '12/08/2026' "
        "was not removed.\n"
        f"Actual results: {result}"
    )

    assert result.count("25/08/2026") == 1, (
        "Date '25/08/2026' should appear exactly once.\n"
        f"Actual results: {result}"
    )

    print("\nDuplicate dates removed successfully.")
    print("\nDUPLICATE DATE TEST PASSED")


# ============================================================
# Test 3 — Complete Extraction
# ============================================================

def test_complete_extraction():

    text = """
    Invoice Date: 12/08/2026
    Due Date: 25/08/2026
    """

    result = ExtractionService.extract(
        text
    )

    print("\n" + "=" * 70)
    print("COMPLETE EXTRACTION TEST")
    print("=" * 70)

    print("\nExtraction Response:")
    print(result)

    # --------------------------------------------------------
    # Validate Response Type
    # --------------------------------------------------------

    assert isinstance(result, dict), (
        "ExtractionService.extract() "
        "must return a dictionary."
    )

    # --------------------------------------------------------
    # Validate Success
    # --------------------------------------------------------

    assert result.get("success") is True, (
        "Complete extraction did not return success=True.\n"
        f"Actual response: {result}"
    )

    # --------------------------------------------------------
    # Validate Required Keys
    # --------------------------------------------------------

    required_keys = [
        "dates",
        "names",
        "organizations",
    ]

    for key in required_keys:

        assert key in result, (
            f"Required key '{key}' "
            f"is missing from extraction response.\n"
            f"Actual response: {result}"
        )

    # --------------------------------------------------------
    # Validate Dates
    # --------------------------------------------------------

    dates = result.get("dates", [])

    assert "12/08/2026" in dates, (
        "Invoice date '12/08/2026' "
        "was not found in complete extraction.\n"
        f"Extracted dates: {dates}"
    )

    assert "25/08/2026" in dates, (
        "Due date '25/08/2026' "
        "was not found in complete extraction.\n"
        f"Extracted dates: {dates}"
    )

    print("\nRequired extraction fields are available.")
    print("\nCOMPLETE EXTRACTION TEST PASSED")


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("EXTRACTION SERVICE TESTS")
    print("=" * 70)

    test_date_extraction()

    test_duplicate_date_removal()

    test_complete_extraction()

    print("\n" + "=" * 70)
    print("ALL EXTRACTION SERVICE TESTS PASSED")
    print("=" * 70)