"""
===============================================================
Enterprise AI Knowledge Assistant

Extraction API Tests
===============================================================

Responsibilities
----------------
1. Validate invoice extraction API
2. Validate date extraction API
3. Validate name extraction through entity extraction API
4. Validate organization extraction through entity extraction API
5. Validate authentication for protected extraction routes
===============================================================
"""


# ============================================================
# Test 1 — Invoice Extraction API
# ============================================================

def test_extraction_api(client, auth_headers):

    response = client.post(
        "/extraction",
        headers=auth_headers,
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
            "extraction_type": "invoice"
        }
    )

    print("\n")
    print("=" * 70)
    print("INFORMATION EXTRACTION API TEST")
    print("=" * 70)

    print("\nStatus Code:")
    print(response.status_code)

    print("\nResponse:")
    print(response.json())

    # --------------------------------------------------------
    # Validate HTTP Status
    # --------------------------------------------------------

    assert response.status_code == 200, (
        f"Expected status code 200, "
        f"but received {response.status_code}.\n"
        f"Response: {response.text}"
    )

    # --------------------------------------------------------
    # Validate Response
    # --------------------------------------------------------

    data = response.json()

    assert isinstance(data, dict), (
        "Extraction API response must be a dictionary."
    )

    assert data.get("success") is True, (
        "Extraction API did not return success=True.\n"
        f"Response: {data}"
    )

    print("\nInvoice extraction completed successfully.")
    print("\nINVOICE EXTRACTION TEST PASSED")


# ============================================================
# Test 2 — Extraction Types
# ============================================================

def test_extraction_types(client, auth_headers):

    print("\n")
    print("=" * 70)
    print("EXTRACTION TYPES TEST")
    print("=" * 70)

    # ========================================================
    # Test 2.1 — Dates Extraction
    # ========================================================

    response = client.post(
        "/extraction",
        headers=auth_headers,
        json={
            "text": (
                "Invoice Date: 12/08/2026. "
                "Due Date: 25/08/2026."
            ),
            "extraction_type": "dates"
        }
    )

    print("\nDates Extraction Response:")
    print(response.json())

    # --------------------------------------------------------
    # Validate HTTP Status
    # --------------------------------------------------------

    assert response.status_code == 200, (
        f"Dates extraction failed.\n"
        f"Status code: {response.status_code}\n"
        f"Response: {response.text}"
    )

    # --------------------------------------------------------
    # Validate Response
    # --------------------------------------------------------

    dates_data = response.json()

    assert isinstance(dates_data, dict), (
        "Dates extraction response must be a dictionary."
    )

    assert dates_data.get("success") is True, (
        f"Dates extraction did not return success=True.\n"
        f"Response: {dates_data}"
    )

    # --------------------------------------------------------
    # Validate extracted dates
    # --------------------------------------------------------

    assert "dates" in dates_data, (
        "Dates extraction response does not contain "
        "'dates' field."
    )

    assert isinstance(dates_data["dates"], list), (
        "Extracted dates must be returned as a list."
    )

    assert "12/08/2026" in dates_data["dates"], (
        "Invoice date 12/08/2026 was not extracted."
    )

    assert "25/08/2026" in dates_data["dates"], (
        "Due date 25/08/2026 was not extracted."
    )

    print("\nDate extraction completed successfully.")

    # ========================================================
    # Test 2.2 — Entity Extraction
    #
    # The API uses:
    #     extraction_type = "entities"
    #
    # But the response contains:
    #     names
    #     organizations
    #
    # Therefore, we validate those exact response fields.
    # ========================================================

    response = client.post(
        "/extraction",
        headers=auth_headers,
        json={
            "text": (
                "The agreement was prepared by Rahul Sharma. "
                "ABC Technologies Pvt Ltd signed an agreement "
                "with XYZ Corporation."
            ),
            "extraction_type": "entities"
        }
    )

    print("\nEntity Extraction Response:")
    print(response.json())

    # --------------------------------------------------------
    # Validate HTTP Status
    # --------------------------------------------------------

    assert response.status_code == 200, (
        f"Entity extraction failed.\n"
        f"Status code: {response.status_code}\n"
        f"Response: {response.text}"
    )

    # --------------------------------------------------------
    # Validate Response
    # --------------------------------------------------------

    entities_data = response.json()

    assert isinstance(entities_data, dict), (
        "Entity extraction response must be a dictionary."
    )

    assert entities_data.get("success") is True, (
        "Entity extraction did not return success=True.\n"
        f"Response: {entities_data}"
    )

    # ========================================================
    # Validate Names
    # ========================================================

    assert "names" in entities_data, (
        "Entity extraction response does not contain "
        "'names' field."
    )

    assert isinstance(entities_data["names"], list), (
        "Extracted names must be returned as a list."
    )

    assert "Rahul Sharma" in entities_data["names"], (
        "Expected name 'Rahul Sharma' was not extracted.\n"
        f"Extracted names: {entities_data['names']}"
    )

    # ========================================================
    # Validate Organizations
    # ========================================================

    assert "organizations" in entities_data, (
        "Entity extraction response does not contain "
        "'organizations' field."
    )

    assert isinstance(entities_data["organizations"], list), (
        "Extracted organizations must be returned as a list."
    )

    assert "ABC Technologies Pvt Ltd" in (
        entities_data["organizations"]
    ), (
        "Expected organization "
        "'ABC Technologies Pvt Ltd' was not extracted.\n"
        f"Extracted organizations: "
        f"{entities_data['organizations']}"
    )

    assert "XYZ Corporation" in (
        entities_data["organizations"]
    ), (
        "Expected organization "
        "'XYZ Corporation' was not extracted.\n"
        f"Extracted organizations: "
        f"{entities_data['organizations']}"
    )

    # --------------------------------------------------------
    # Display extracted entities
    # --------------------------------------------------------

    print("\nExtracted Names:")

    for name in entities_data["names"]:
        print(f"  - {name}")

    print("\nExtracted Organizations:")

    for organization in entities_data["organizations"]:
        print(f"  - {organization}")

    print("\nEntity extraction completed successfully.")

    # ========================================================
    # Final Result
    # ========================================================

    print("\nAll extraction types completed successfully.")
    print("\nEXTRACTION TYPES TEST PASSED")


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("EXTRACTION API TESTS")
    print("=" * 70)

    print(
        "\nRun this file using pytest:"
    )

    print(
        "pytest tests/test_extraction_api.py -v -s"
    )

    print("\n" + "=" * 70)
