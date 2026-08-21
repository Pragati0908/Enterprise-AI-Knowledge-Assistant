from app.services.extraction_service import (
    ExtractionService
)


def test_invoice_extraction():

    text = """

    TAX INVOICE

    Invoice Number: INV-2026-001

    Invoice Date: 12/08/2026

    Due Date: 25/08/2026

    Vendor: ABC Technologies Pvt Ltd

    Customer: XYZ Corporation

    Subtotal: ₹10,000.00

    GST: ₹1,800.00

    Grand Total: ₹11,800.00

    """

    result = (
        ExtractionService.extract_invoice(
            text
        )
    )

    print("\n")
    print("=" * 70)
    print("INVOICE EXTRACTION TEST")
    print("=" * 70)

    print("\nResult:")
    print(result)

    # ==========================================================
    # Invoice Number
    # ==========================================================

    assert (
        result["invoice_number"]
        == "INV-2026-001"
    )

    # ==========================================================
    # Invoice Date
    # ==========================================================

    assert (
        result["invoice_date"]
        == "12/08/2026"
    )

    # ==========================================================
    # Due Date
    # ==========================================================

    assert (
        result["due_date"]
        == "25/08/2026"
    )

    # ==========================================================
    # Vendor
    # ==========================================================

    assert (
        result["vendor"]
        == "ABC Technologies Pvt Ltd"
    )

    # ==========================================================
    # Customer
    # ==========================================================

    assert (
        result["customer"]
        == "XYZ Corporation"
    )

    # ==========================================================
    # Subtotal
    # ==========================================================

    assert (
        result["subtotal"]
        == 10000.00
    )

    # ==========================================================
    # Tax
    # ==========================================================

    assert (
        result["tax"]
        == 1800.00
    )

    # ==========================================================
    # Total
    # ==========================================================

    assert (
        result["total_amount"]
        == 11800.00
    )

    # ==========================================================
    # Currency
    # ==========================================================

    assert (
        result["currency"]
        == "INR"
    )

    print("\nTEST PASSED")


if __name__ == "__main__":

    test_invoice_extraction()