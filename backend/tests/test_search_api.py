"""
===============================================================
Enterprise AI Knowledge Assistant

Search API Test
===============================================================
"""


# ============================================================
# Test Search API
# ============================================================

def test_search_api(client, auth_headers):

    response = client.post(
        "/search",
        headers=auth_headers,
        json={
            "query": "OCR",
            "top_k": 5
        }
    )

    print("\n" + "=" * 70)
    print("SEARCH API TEST")
    print("=" * 70)

    print("\nStatus Code:")
    print(response.status_code)

    print("\nResponse:")
    print(response.json())

    # ========================================================
    # Validate HTTP Response
    # ========================================================

    assert response.status_code == 200, (
        f"Expected status code 200, "
        f"but received {response.status_code}. "
        f"Response: {response.text}"
    )

    # ========================================================
    # Validate Response JSON
    # ========================================================

    data = response.json()

    assert "success" in data, (
        "Response does not contain the 'success' field."
    )

    assert "results" in data, (
        "Response does not contain the 'results' field."
    )

    # ========================================================
    # Display Successful Test
    # ========================================================

    print("\nTEST PASSED")


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("SEARCH API TEST")
    print("=" * 70)

    print("\nRun this test using pytest:")
    print(
        "python -m pytest "
        "tests/test_search_api.py -v -s"
    )

    print("\n" + "=" * 70)