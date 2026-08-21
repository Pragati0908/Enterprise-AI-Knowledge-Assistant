from app.services.extraction_service import (
    ExtractionService
)


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

    print("\n" + "=" * 60)
    print("DATE EXTRACTION TEST")
    print("=" * 60)

    print("\nExtracted Dates:")

    for date in result:

        print(
            f"  - {date}"
        )

    assert "12/08/2026" in result
    assert "25/08/2026" in result
    assert "2026-08-30" in result
    assert "15 August 2026" in result
    assert "August 20, 2026" in result

    print("\nAll supported date formats detected.")

    print("\nTEST PASSED")


def test_duplicate_date_removal():

    text = """
    Invoice Date: 12/08/2026
    The invoice was generated on 12/08/2026.
    Payment due on 25/08/2026.
    """

    result = ExtractionService.extract_dates(
        text
    )

    print("\nDuplicate Removal Test:")
    print(result)

    assert result.count(
        "12/08/2026"
    ) == 1

    assert result.count(
        "25/08/2026"
    ) == 1

    print("\nDUPLICATE TEST PASSED")


def test_complete_extraction():

    text = """
    Invoice Date: 12/08/2026
    Due Date: 25/08/2026
    """

    result = ExtractionService.extract(
        text
    )

    print("\nComplete Extraction:")
    print(result)

    assert result["success"] is True

    assert "dates" in result

    assert "names" in result

    assert "organizations" in result

    assert "12/08/2026" in result["dates"]

    assert "25/08/2026" in result["dates"]

    print("\nCOMPLETE EXTRACTION TEST PASSED")


if __name__ == "__main__":

    test_date_extraction()

    test_duplicate_date_removal()

    test_complete_extraction()

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED")
    print("=" * 60)