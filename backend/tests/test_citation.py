from app.services.citation_service import CitationService


# =============================================================
# Test 1 - Single Citation
# =============================================================

def test_single_citation():

    result = {

        "document": "OCR_Guide.pdf",

        "page": 4,

        "chunk_id": "chunk_12",

        "distance": 0.2381

    }

    citation = CitationService.create_citation(
        result
    )

    print("\n" + "=" * 70)
    print("TEST 1 : SINGLE CITATION")
    print("=" * 70)

    print("\nOriginal Result:")
    print(result)

    print("\nGenerated Citation:")
    print(citation)

    assert citation["document"] == "OCR_Guide.pdf"
    assert citation["page"] == 4
    assert citation["chunk_id"] == "chunk_12"

    print("\nTEST 1 PASSED")


# =============================================================
# Test 2 - Multiple Citations
# =============================================================

def test_multiple_citations():

    results = [

        {
            "document": "OCR_Guide.pdf",
            "page": 4,
            "chunk_id": "chunk_12",
            "distance": 0.2381
        },

        {
            "document": "enterprise_ai.docx",
            "page": 2,
            "chunk_id": "chunk_2",
            "distance": 0.3412
        },

        {
            "document": "sample_chunk_testing.pdf",
            "page": 1,
            "chunk_id": "chunk_5",
            "distance": 0.4521
        }

    ]

    citations = CitationService.create_citations(
        results
    )

    print("\n" + "=" * 70)
    print("TEST 2 : MULTIPLE CITATIONS")
    print("=" * 70)

    print(
        f"\nTotal Citations : "
        f"{len(citations)}"
    )

    for citation in citations:

        print(
            f"\n{citation['citation']}"
        )

        print(
            f"Distance : "
            f"{citation['distance']}"
        )

    assert len(citations) == 3

    print("\nTEST 2 PASSED")


# =============================================================
# Test 3 - Missing Metadata / Fallback
# =============================================================

def test_citation_fallback():

    result = {

        "document": "test.pdf"

    }

    citation = CitationService.create_citation(
        result
    )

    print("\n" + "=" * 70)
    print("TEST 3 : CITATION FALLBACK")
    print("=" * 70)

    print("\nOriginal Result:")
    print(result)

    print("\nGenerated Citation:")
    print(citation)

    # ---------------------------------------------------------
    # Verify document is preserved
    # ---------------------------------------------------------

    assert (
        citation["document"]
        == "test.pdf"
    )

    # ---------------------------------------------------------
    # Page should use default value
    # ---------------------------------------------------------

    assert (
        citation["page"]
        == 1
    )

    # ---------------------------------------------------------
    # Chunk ID should use fallback value
    # ---------------------------------------------------------

    assert (
        citation["chunk_id"]
        == "Unknown"
    )

    # ---------------------------------------------------------
    # Distance should use default value
    # ---------------------------------------------------------

    assert (
        citation["distance"]
        == 0
    )

    # ---------------------------------------------------------
    # Citation text should also contain
    # the fallback values
    # ---------------------------------------------------------

    assert (
        citation["citation"]
        == "[test.pdf | Page 1 | Chunk Unknown]"
    )

    print("\nTEST 3 PASSED")


# =============================================================
# Main
# =============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("CITATION SERVICE TEST")
    print("=" * 70)

    test_single_citation()

    test_multiple_citations()

    test_citation_fallback()

    print("\n" + "=" * 70)
    print("ALL CITATION TESTS PASSED")
    print("=" * 70)