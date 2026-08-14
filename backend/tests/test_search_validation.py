"""
===============================================================
Enterprise AI Knowledge Assistant

Day 40
Search Ranking and Citation Validation

Responsibilities
----------------
1. Validate search response
2. Validate required fields
3. Validate citation
4. Validate ranking
5. Detect duplicate chunks
===============================================================
"""

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ==========================================================
# Test 1 — Search API Response
# ==========================================================

def test_search_response():

    response = client.post(
        "/search",
        json={
            "query": "What is OCR?",
            "top_k": 5
        }
    )

    print("\n" + "=" * 70)
    print("DAY 40 — SEARCH VALIDATION")
    print("=" * 70)

    print("\nStatus Code:")
    print(response.status_code)

    assert response.status_code == 200

    data = response.json()

    print("\nResponse:")
    print(data)

    assert data["success"] is True

    assert "query" in data

    assert "total_results" in data

    assert "results" in data

    print("\nTEST 1 PASSED")


# ==========================================================
# Test 2 — Validate Result Fields
# ==========================================================

def test_result_fields():

    response = client.post(
        "/search",
        json={
            "query": "What is OCR?",
            "top_k": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    results = data.get(
        "results",
        []
    )

    print("\n" + "=" * 70)
    print("TEST 2 — RESULT FIELD VALIDATION")
    print("=" * 70)

    if not results:

        print("\nNo results returned.")

        return

    required_fields = [
        "document",
        "page",
        "chunk_id",
        "distance",
        "text",
        "citation"
    ]

    for index, item in enumerate(
        results,
        start=1
    ):

        print(
            f"\nValidating Result #{index}"
        )

        for field in required_fields:

            print(
                f"  {field}: "
                f"{item.get(field)}"
            )

            assert field in item

    print("\nTEST 2 PASSED")


# ==========================================================
# Test 3 — Citation Validation
# ==========================================================

def test_citations():

    response = client.post(
        "/search",
        json={
            "query": "What is OCR?",
            "top_k": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    results = data.get(
        "results",
        []
    )

    print("\n" + "=" * 70)
    print("TEST 3 — CITATION VALIDATION")
    print("=" * 70)

    for item in results:

        citation = item.get(
            "citation"
        )

        assert citation is not None

        assert citation != ""

        document = item["document"]

        page = item["page"]

        chunk_id = item["chunk_id"]

        assert document in citation

        assert str(page) in citation

        assert str(chunk_id) in citation

        print(
            f"\n{citation}"
        )

    print("\nTEST 3 PASSED")


# ==========================================================
# Test 4 — Ranking Validation
# ==========================================================

def test_ranking():

    response = client.post(
        "/search",
        json={
            "query": "What is OCR?",
            "top_k": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    results = data.get(
        "results",
        []
    )

    print("\n" + "=" * 70)
    print("TEST 4 — RANKING VALIDATION")
    print("=" * 70)

    if len(results) < 2:

        print(
            "\nNot enough results to validate ranking."
        )

        return

    distances = [

        float(
            item.get(
                "distance",
                float("inf")
            )
        )

        for item in results

    ]

    print(
        "\nDistances:"
    )

    for distance in distances:

        print(
            distance
        )

    assert distances == sorted(
        distances
    )

    print(
        "\nRanking is in ascending "
        "distance order."
    )

    print("\nTEST 4 PASSED")


# ==========================================================
# Test 5 — Duplicate Validation
# ==========================================================

def test_duplicate_results():

    response = client.post(
        "/search",
        json={
            "query": "What is OCR?",
            "top_k": 10
        }
    )

    assert response.status_code == 200

    data = response.json()

    results = data.get(
        "results",
        []
    )

    print("\n" + "=" * 70)
    print("TEST 5 — DUPLICATE VALIDATION")
    print("=" * 70)

    seen = set()

    for item in results:

        unique_key = (

            item.get("document"),

            item.get("chunk_id")

        )

        print(
            f"\nChecking: {unique_key}"
        )

        assert unique_key not in seen

        seen.add(
            unique_key
        )

    print(
        f"\nUnique Results: {len(seen)}"
    )

    print("\nTEST 5 PASSED")


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    print("\n")

    print("=" * 70)
    print("DAY 40 — SEARCH, RANKING AND CITATION VALIDATION")
    print("=" * 70)

    test_search_response()

    test_result_fields()

    test_citations()

    test_ranking()

    test_duplicate_results()

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED")
    print("=" * 70)