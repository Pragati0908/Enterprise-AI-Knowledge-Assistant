"""
===============================================================
Enterprise AI Knowledge Assistant

Negative and Boundary Tests
===============================================================
"""

from typing import Any


def print_response(test_name: str, response: Any) -> None:
    print("\n" + "=" * 70)
    print(test_name)
    print("=" * 70)

    print("\nStatus Code:")
    print(response.status_code)

    print("\nResponse:")
    print(response.json())

    print("\n" + "-" * 70)


# ============================================================
# Authentication Tests
# ============================================================

def test_search_without_authentication(client):
    response = client.post(
        "/search",
        json={
            "query": "What is OCR?",
            "top_k": 5
        }
    )

    print_response(
        "NEGATIVE TEST 1 — SEARCH WITHOUT AUTHENTICATION",
        response
    )

    assert response.status_code == 401


def test_extraction_without_authentication(client):
    response = client.post(
        "/extraction",
        json={
            "text": "Invoice Date: 12/08/2026",
            "extraction_type": "dates"
        }
    )

    print_response(
        "NEGATIVE TEST 2 — EXTRACTION WITHOUT AUTHENTICATION",
        response
    )

    assert response.status_code == 401


def test_invalid_authorization_token(client):
    response = client.post(
        "/search",
        headers={
            "Authorization": "Bearer invalid_token"
        },
        json={
            "query": "OCR",
            "top_k": 5
        }
    )

    print_response(
        "NEGATIVE TEST 3 — INVALID AUTHORIZATION TOKEN",
        response
    )

    assert response.status_code == 401


# ============================================================
# Search Validation Tests
# ============================================================

def test_empty_search_query(client, auth_headers):
    response = client.post(
        "/search",
        headers=auth_headers,
        json={
            "query": "",
            "top_k": 5
        }
    )

    print_response(
        "NEGATIVE TEST 4 — EMPTY SEARCH QUERY",
        response
    )

    assert response.status_code in (400, 422)


def test_missing_search_query(client, auth_headers):
    response = client.post(
        "/search",
        headers=auth_headers,
        json={
            "top_k": 5
        }
    )

    print_response(
        "NEGATIVE TEST 5 — MISSING SEARCH QUERY",
        response
    )

    assert response.status_code in (400, 422)


def test_invalid_top_k(client, auth_headers):
    response = client.post(
        "/search",
        headers=auth_headers,
        json={
            "query": "OCR",
            "top_k": -1
        }
    )

    print_response(
        "NEGATIVE TEST 6 — INVALID TOP_K",
        response
    )

    assert response.status_code in (400, 422)


def test_zero_top_k(client, auth_headers):
    response = client.post(
        "/search",
        headers=auth_headers,
        json={
            "query": "OCR",
            "top_k": 0
        }
    )

    print_response(
        "NEGATIVE TEST 7 — ZERO TOP_K",
        response
    )

    assert response.status_code in (400, 422)


def test_top_k_as_string(client, auth_headers):
    response = client.post(
        "/search",
        headers=auth_headers,
        json={
            "query": "OCR",
            "top_k": "five"
        }
    )

    print_response(
        "NEGATIVE TEST 8 — TOP_K AS STRING",
        response
    )

    assert response.status_code in (400, 422)


# ==========================================================
# NEGATIVE TEST 9 — WHITESPACE-ONLY SEARCH QUERY
# ==========================================================

def test_whitespace_only_search_query(client, auth_headers):
    response = client.post(
        "/search",
        headers=auth_headers,
        json={
            "query": "   ",
            "top_k": 5
        }
    )

    print_response(
        "NEGATIVE TEST 9 — WHITESPACE-ONLY SEARCH QUERY",
        response
    )

    data = response.json()

    # The API returns HTTP 200 but reports application-level failure.
    assert response.status_code == 200

    assert data["success"] is False
    assert data["query"] == "   "
    assert data["total_results"] == 0
    assert data["results"] == []
    assert data["error"] == "Search query cannot be empty."

def test_malformed_json_request(client, auth_headers):
    response = client.post(
        "/search",
        headers={
            **auth_headers,
            "Content-Type": "application/json"
        },
        content='{"query": "OCR", "top_k": }'
    )

    print_response(
        "NEGATIVE TEST 10 — MALFORMED JSON",
        response
    )

    assert response.status_code in (400, 422)


def test_search_with_no_matching_results(client, auth_headers):
    response = client.post(
        "/search",
        headers=auth_headers,
        json={
            "query": "This phrase should not exist in the indexed documents",
            "top_k": 5
        }
    )

    print_response(
        "NEGATIVE TEST 11 — EMPTY SEARCH RESULTS",
        response
    )

    assert response.status_code == 200


# ============================================================
# Extraction Validation Tests
# ============================================================

def test_missing_extraction_text(client, auth_headers):
    response = client.post(
        "/extraction",
        headers=auth_headers,
        json={
            "extraction_type": "dates"
        }
    )

    print_response(
        "NEGATIVE TEST 12 — MISSING EXTRACTION TEXT",
        response
    )

    assert response.status_code in (400, 422)


def test_empty_extraction_text(client, auth_headers):
    response = client.post(
        "/extraction",
        headers=auth_headers,
        json={
            "text": "",
            "extraction_type": "dates"
        }
    )

    print_response(
        "NEGATIVE TEST 13 — EMPTY EXTRACTION TEXT",
        response
    )

    assert response.status_code in (200, 400, 422)


# ==========================================================
# NEGATIVE TEST 14 — UNSUPPORTED EXTRACTION TYPE
# ==========================================================

def test_unsupported_extraction_type(client, auth_headers):
    response = client.post(
        "/extraction",
        headers=auth_headers,
        json={
            "text": "Invoice Date: 12/08/2026",
            "extraction_type": "unsupported_type"
        }
    )

    print_response(
        "NEGATIVE TEST 14 — UNSUPPORTED EXTRACTION TYPE",
        response
    )

    data = response.json()

    # The API returns HTTP 200 but reports application-level failure.
    assert response.status_code == 200

    assert data["success"] is False
    assert data["error"] == "Unsupported extraction type."

    assert data["supported_types"] == [
        "all",
        "dates",
        "entities",
        "invoice"
    ]


def test_extraction_text_as_number(client, auth_headers):
    response = client.post(
        "/extraction",
        headers=auth_headers,
        json={
            "text": 12345,
            "extraction_type": "dates"
        }
    )

    print_response(
        "NEGATIVE TEST 15 — EXTRACTION TEXT AS NUMBER",
        response
    )

    assert response.status_code in (400, 422)


def test_large_extraction_text(client, auth_headers):
    large_text = (
        "Invoice Date: 12/08/2026. "
        "Due Date: 25/08/2026. "
    ) * 1000

    response = client.post(
        "/extraction",
        headers=auth_headers,
        json={
            "text": large_text,
            "extraction_type": "dates"
        }
    )

    print_response(
        "NEGATIVE TEST 16 — LARGE EXTRACTION TEXT",
        response
    )

    assert response.status_code in (200, 400, 413, 422)