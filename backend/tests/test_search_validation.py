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


# ============================================================
# Test 1 — Search API Response
# ============================================================

def test_search_response(client, auth_headers):

    response = client.post(
        "/search",
        headers=auth_headers,
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

    assert response.status_code == 200, (
        f"Expected status code 200, "
        f"but received {response.status_code}. "
        f"Response: {response.text}"
    )

    data = response.json()

    print("\nResponse:")
    print(data)

    assert data["success"] is True

    assert "query" in data

    assert "total_results" in data

    assert "results" in data

    print("\nTEST 1 PASSED")


# ============================================================
# Test 2 — Validate Result Fields
# ============================================================

def test_result_fields(client, auth_headers):

    response = client.post(
        "/search",
        headers=auth_headers,
        json={
            "query": "What is OCR?",
            "top_k": 5
        }
    )

    assert response.status_code == 200, (
        f"Expected status code 200, "
        f"but received {response.status_code}. "
        f"Response: {response.text}"
    )

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

            assert field in item, (
                f"Required field '{field}' "
                f"is missing from result #{index}."
            )

    print("\nTEST 2 PASSED")


# ============================================================
# Test 3 — Citation Validation
# ============================================================

def test_citations(client, auth_headers):

    response = client.post(
        "/search",
        headers=auth_headers,
        json={
            "query": "What is OCR?",
            "top_k": 5
        }
    )

    assert response.status_code == 200, (
        f"Expected status code 200, "
        f"but received {response.status_code}. "
        f"Response: {response.text}"
    )

    data = response.json()

    results = data.get(
        "results",
        []
    )

    print("\n" + "=" * 70)
    print("TEST 3 — CITATION VALIDATION")
    print("=" * 70)

    for index, item in enumerate(
        results,
        start=1
    ):

        citation = item.get(
            "citation"
        )

        assert citation is not None, (
            f"Citation is missing from result #{index}."
        )

        assert citation != "", (
            f"Citation is empty in result #{index}."
        )

        document = item["document"]

        page = item["page"]

        chunk_id = item["chunk_id"]

        assert str(document) in citation, (
            f"Document '{document}' "
            f"is not present in citation: {citation}"
        )

        assert str(page) in citation, (
            f"Page '{page}' "
            f"is not present in citation: {citation}"
        )

        assert str(chunk_id) in citation, (
            f"Chunk ID '{chunk_id}' "
            f"is not present in citation: {citation}"
        )

        print(
            f"\n{citation}"
        )

    print("\nTEST 3 PASSED")


# ============================================================
# Test 4 — Ranking Validation
# ============================================================

def test_ranking(client, auth_headers):

    response = client.post(
        "/search",
        headers=auth_headers,
        json={
            "query": "What is OCR?",
            "top_k": 5
        }
    )

    assert response.status_code == 200, (
        f"Expected status code 200, "
        f"but received {response.status_code}. "
        f"Response: {response.text}"
    )

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

    print("\nDistances:")

    for distance in distances:

        print(distance)

    assert distances == sorted(
        distances
    ), (
        "Search results are not ordered "
        "by ascending distance."
    )

    print(
        "\nRanking is in ascending "
        "distance order."
    )

    print("\nTEST 4 PASSED")


# ============================================================
# Test 5 — Duplicate Validation
# ============================================================

def test_duplicate_results(client, auth_headers):

    response = client.post(
        "/search",
        headers=auth_headers,
        json={
            "query": "What is OCR?",
            "top_k": 10
        }
    )

    assert response.status_code == 200, (
        f"Expected status code 200, "
        f"but received {response.status_code}. "
        f"Response: {response.text}"
    )

    data = response.json()

    results = data.get(
        "results",
        []
    )

    print("\n" + "=" * 70)
    print("TEST 5 — DUPLICATE VALIDATION")
    print("=" * 70)

    seen = set()

    for index, item in enumerate(
        results,
        start=1
    ):

        unique_key = (
            item.get("document"),
            item.get("chunk_id")
        )

        print(
            f"\nChecking Result #{index}: "
            f"{unique_key}"
        )

        assert unique_key not in seen, (
            f"Duplicate result detected: {unique_key}"
        )

        seen.add(
            unique_key
        )

    print(
        f"\nUnique Results: {len(seen)}"
    )

    print("\nTEST 5 PASSED")


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print(
        "DAY 40 — SEARCH, RANKING AND "
        "CITATION VALIDATION"
    )
    print("=" * 70)

    print("\nRun this file using pytest:")
    print(
        "python -m pytest "
        "tests/test_search_validation.py -v -s"
    )

    print("\n" + "=" * 70)