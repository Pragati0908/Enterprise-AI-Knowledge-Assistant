"""
===============================================================
Search API Test
===============================================================
"""

from fastapi.testclient import TestClient

from app.main import app


# ============================================================
# Test Client
# ============================================================

client = TestClient(app)


# ============================================================
# Test Search API
# ============================================================

def test_search_api():

    response = client.post(
        "/search",
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

    assert response.status_code == 200

    # ========================================================
    # Validate Response JSON
    # ========================================================

    data = response.json()

    assert "success" in data
    assert "results" in data

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

    test_search_api()

    print("\n" + "=" * 70)
    print("ALL SEARCH API TESTS PASSED")
    print("=" * 70)