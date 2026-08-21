"""
===============================================================
Enterprise AI Knowledge Assistant

Information Extraction API Test
===============================================================
"""

from fastapi.testclient import TestClient

from app.main import app


# ==========================================================
# Test Client
# ==========================================================

client = TestClient(
    app
)


# ==========================================================
# Invoice API Test
# ==========================================================

def test_extraction_api():

    response = client.post(

        "/extraction",

        json={

            "text": """

            Invoice Number: INV-1001

            Invoice Date: 12/08/2026

            Due Date: 25/08/2026

            Vendor: ABC Technologies Pvt Ltd

            Customer: XYZ Corporation

            Subtotal: ₹5000

            GST: ₹900

            Grand Total: ₹5900

            """,

            "extraction_type":
                "invoice"
        }
    )

    print("\n")

    print("=" * 70)

    print(
        "INFORMATION EXTRACTION API TEST"
    )

    print("=" * 70)

    print("\nStatus Code:")

    print(
        response.status_code
    )

    print("\nResponse:")

    print(
        response.json()
    )

    # ======================================================
    # Validate HTTP status
    # ======================================================

    assert (
        response.status_code
        == 200
    )

    # ======================================================
    # Response JSON
    # ======================================================

    data = response.json()

    # ======================================================
    # Validate success
    # ======================================================

    assert (
        data["success"]
        is True
    )

    # ======================================================
    # Validate invoice number
    # ======================================================

    assert (
        data["invoice"]["invoice_number"]
        == "INV-1001"
    )

    # ======================================================
    # Validate invoice date
    # ======================================================

    assert (
        data["invoice"]["invoice_date"]
        == "12/08/2026"
    )

    # ======================================================
    # Validate due date
    # ======================================================

    assert (
        data["invoice"]["due_date"]
        == "25/08/2026"
    )

    # ======================================================
    # Validate vendor
    # ======================================================

    assert (
        data["invoice"]["vendor"]
        == "ABC Technologies Pvt Ltd"
    )

    # ======================================================
    # Validate customer
    # ======================================================

    assert (
        data["invoice"]["customer"]
        == "XYZ Corporation"
    )

    # ======================================================
    # Validate subtotal
    # ======================================================

    assert (
        data["invoice"]["subtotal"]
        == 5000.0
    )

    # ======================================================
    # Validate GST
    # ======================================================

    assert (
        data["invoice"]["tax"]
        == 900.0
    )

    # ======================================================
    # Validate total
    # ======================================================

    assert (
        data["invoice"]["total_amount"]
        == 5900.0
    )

    # ======================================================
    # Validate currency
    # ======================================================

    assert (
        data["invoice"]["currency"]
        == "INR"
    )

    print(
        "\nTEST PASSED"
    )

def test_extraction_types():

    # ======================================================
    # DATES
    # ======================================================

    response = client.post(

        "/extraction",

        json={

            "text": (
                "Invoice Date: 12/08/2026. "
                "Due Date: 25/08/2026."
            ),

            "extraction_type":
                "dates"
        }
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert (
        "12/08/2026"
        in data["dates"]
    )

    assert (
        "25/08/2026"
        in data["dates"]
    )

    print(
        "\nDATES API TEST PASSED"
    )

    # ======================================================
    # ENTITIES
    # ======================================================

    response = client.post(

        "/extraction",

        json={

            "text": (
                "Rahul Sharma works for "
                "Microsoft Corporation."
            ),

            "extraction_type":
                "entities"
        }
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert (
        "Rahul Sharma"
        in data["names"]
    )

    assert any(
        "Microsoft"
        in organization
        for organization
        in data["organizations"]
    )

    print(
        "ENTITIES API TEST PASSED"
    )

    # ======================================================
    # INVALID TYPE
    # ======================================================

    response = client.post(

        "/extraction",

        json={

            "text":
                "Some document text",

            "extraction_type":
                "invalid"
        }
    )

    assert (
        response.status_code
        == 200
    )

    data = response.json()

    assert (
        data["success"]
        is False
    )

    assert (
        "Unsupported extraction type."
        == data["error"]
    )

    print(
        "INVALID TYPE TEST PASSED"
    )


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    test_extraction_api()

    test_extraction_types() 