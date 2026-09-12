"""
===============================================================
Enterprise AI Knowledge Assistant

Week 13 — Tuesday Performance Tests
===============================================================

Responsibilities
----------------
1. Measure search API response time
2. Measure extraction API response time
3. Measure repeated search performance
4. Display performance statistics
5. Preserve existing functional behavior
===============================================================
"""

import time


# ============================================================
# Test 1 — Search Response Time
# ============================================================

def test_search_response_time(client, auth_headers):

    query = {
        "query": "What is OCR?",
        "top_k": 5
    }

    start_time = time.perf_counter()

    response = client.post(
        "/search",
        headers=auth_headers,
        json=query
    )

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    print("\n" + "=" * 70)
    print("PERFORMANCE TEST 1 — SEARCH RESPONSE TIME")
    print("=" * 70)

    print("\nStatus Code:")
    print(response.status_code)

    print("\nResponse Time:")
    print(f"{elapsed_time:.4f} seconds")

    assert response.status_code == 200, (
        f"Search request failed.\n"
        f"Response: {response.text}"
    )

    # --------------------------------------------------------
    # Development threshold
    # --------------------------------------------------------
    # This is NOT a production SLA.
    # Change it only after observing actual performance.

    assert elapsed_time < 5.0, (
        f"Search response exceeded the development threshold.\n"
        f"Response time: {elapsed_time:.4f} seconds"
    )

    print("\nSEARCH PERFORMANCE TEST PASSED")


# ============================================================
# Test 2 — Extraction Response Time
# ============================================================

def test_extraction_response_time(client, auth_headers):

    query = {
        "text": """
        Invoice Number: INV-1001
        Invoice Date: 12/08/2026
        Due Date: 25/08/2026
        Vendor: ABC Technologies Pvt Ltd
        Customer: XYZ Corporation
        """,
        "extraction_type": "invoice"
    }

    start_time = time.perf_counter()

    response = client.post(
        "/extraction",
        headers=auth_headers,
        json=query
    )

    end_time = time.perf_counter()

    elapsed_time = end_time - start_time

    print("\n" + "=" * 70)
    print("PERFORMANCE TEST 2 — EXTRACTION RESPONSE TIME")
    print("=" * 70)

    print("\nStatus Code:")
    print(response.status_code)

    print("\nResponse Time:")
    print(f"{elapsed_time:.4f} seconds")

    assert response.status_code == 200, (
        f"Extraction request failed.\n"
        f"Response: {response.text}"
    )

    assert elapsed_time < 5.0, (
        f"Extraction response exceeded the development threshold.\n"
        f"Response time: {elapsed_time:.4f} seconds"
    )

    print("\nEXTRACTION PERFORMANCE TEST PASSED")


# ============================================================
# Test 3 — Repeated Search Performance
# ============================================================

def test_repeated_search_performance(client, auth_headers):

    query = {
        "query": "What is OCR?",
        "top_k": 5
    }

    execution_times = []

    number_of_requests = 5

    print("\n" + "=" * 70)
    print("PERFORMANCE TEST 3 — REPEATED SEARCH")
    print("=" * 70)

    for request_number in range(1, number_of_requests + 1):

        start_time = time.perf_counter()

        response = client.post(
            "/search",
            headers=auth_headers,
            json=query
        )

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        execution_times.append(elapsed_time)

        assert response.status_code == 200, (
            f"Search request #{request_number} failed.\n"
            f"Response: {response.text}"
        )

        print(
            f"Request {request_number}: "
            f"{elapsed_time:.4f} seconds"
        )

    average_time = (
        sum(execution_times)
        / len(execution_times)
    )

    minimum_time = min(execution_times)
    maximum_time = max(execution_times)

    print("\nAverage Response Time:")
    print(f"{average_time:.4f} seconds")

    print("\nMinimum Response Time:")
    print(f"{minimum_time:.4f} seconds")

    print("\nMaximum Response Time:")
    print(f"{maximum_time:.4f} seconds")

    assert average_time < 5.0, (
        f"Average search response time exceeded threshold.\n"
        f"Average: {average_time:.4f} seconds"
    )

    print("\nREPEATED SEARCH PERFORMANCE TEST PASSED")


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("WEEK 13 — PERFORMANCE TESTS")
    print("=" * 70)

    print("\nRun this file using pytest:")
    print(
        "pytest tests/test_performance.py -v -s"
    )

    print("\n" + "=" * 70)