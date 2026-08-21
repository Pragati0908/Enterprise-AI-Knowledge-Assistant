from app.services.extraction_service import (
    ExtractionService
)


def test_entity_extraction():

    text = """
    Invoice prepared by Rahul Sharma
    for Microsoft Corporation.

    The document was reviewed by
    Priya Agrawal.
    """

    result = ExtractionService.extract(
        text
    )

    print("\nExtracted Information:")
    print(result)

    assert "Rahul Sharma" in result["names"]

    assert "Priya Agrawal" in result["names"]

    assert any(
        "Microsoft" in organization
        for organization in result["organizations"]
    )

    print("\nTEST PASSED")


if __name__ == "__main__":

    test_entity_extraction()