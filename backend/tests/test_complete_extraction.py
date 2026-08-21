from app.services.extraction_service import (
    ExtractionService
)


def test_complete_extraction():

    text = """
    Invoice prepared by Rahul Sharma
    for Microsoft Corporation.

    Invoice Date: 12/08/2026

    Due Date: 25/08/2026

    The document was reviewed by
    Priya Agrawal.

    Agreement Date: 2026-08-30

    The contract was issued by
    Infosys Limited.
    """

    result = ExtractionService.extract(
        text
    )

    print("\n")
    print("=" * 70)
    print("COMPLETE INFORMATION EXTRACTION")
    print("=" * 70)

    print("\nDates:")
    for date in result["dates"]:
        print(
            f"  - {date}"
        )

    print("\nNames:")
    for name in result["names"]:
        print(
            f"  - {name}"
        )

    print("\nOrganizations:")
    for organization in result["organizations"]:
        print(
            f"  - {organization}"
        )

    print("\nComplete Result:")
    print(result)

    # ==========================================================
    # Date Assertions
    # ==========================================================

    assert "12/08/2026" in result["dates"]

    assert "25/08/2026" in result["dates"]

    assert "2026-08-30" in result["dates"]

    # ==========================================================
    # Name Assertions
    # ==========================================================

    assert "Rahul Sharma" in result["names"]

    assert "Priya Agrawal" in result["names"]

    # ==========================================================
    # Organization Assertions
    # ==========================================================

    assert any(
        "Microsoft" in organization
        for organization
        in result["organizations"]
    )

    assert any(
        "Infosys" in organization
        for organization
        in result["organizations"]
    )

    print("\nCOMPLETE EXTRACTION TEST PASSED")


if __name__ == "__main__":

    test_complete_extraction()