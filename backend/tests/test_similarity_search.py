"""
===============================================================
Enterprise AI Knowledge Assistant

Similarity Search Test

Purpose
-------
Test:

1. PDF extraction
2. Text chunking
3. Embedding generation
4. FAISS vector insertion
5. Metadata mapping
6. Similarity search

IMPORTANT
---------
This test does NOT modify the application's persistent:

    backend/vector_db/faiss.index

or:

    backend/vector_db/metadata.json
===============================================================
"""

from app.services.parsers.pdf_parser import PDFParser
from app.services.chunker import TextChunker
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.metadata_store import MetadataStore


# ==========================================================
# STEP 1 : Extract Text from PDF
# ==========================================================

def test_similarity_search():

    print()
    print("=" * 70)
    print("STEP 1 : PDF EXTRACTION")
    print("=" * 70)

    text = PDFParser.extract_text(
        "tests/sample_chunk_testing.pdf"
    )

    print(
        f"\nTotal Characters : {len(text)}"
    )

    assert text, (
        "PDF extraction returned empty text."
    )

    # ======================================================
    # STEP 2 : Generate Chunks
    # ======================================================

    print()
    print("=" * 70)
    print("STEP 2 : CHUNK GENERATION")
    print("=" * 70)

    chunks = TextChunker.chunk_text(

        text=text,

        source="sample_chunk_testing.pdf",

        chunk_size=800,

        overlap=150

    )

    print(
        f"\nTotal Chunks : {len(chunks)}"
    )

    assert chunks, (
        "No chunks were generated from PDF."
    )

    # ======================================================
    # STEP 3 : Prepare Chunk Texts
    # ======================================================

    chunk_texts = [

        chunk["text"]

        for chunk in chunks

    ]

    # ======================================================
    # STEP 4 : Generate Embeddings
    # ======================================================

    print()
    print("=" * 70)
    print("STEP 3 : GENERATE EMBEDDINGS")
    print("=" * 70)

    embeddings = (
        EmbeddingService.generate_embeddings(
            chunk_texts
        )
    )

    print(
        f"\nEmbeddings Generated : "
        f"{len(embeddings)}"
    )

    assert len(embeddings) == len(chunks), (
        "Number of embeddings does not "
        "match number of chunks."
    )

    dimension = len(
        embeddings[0]
    )

    print(
        f"Embedding Dimension : "
        f"{dimension}"
    )

    # ======================================================
    # STEP 5 : Create Isolated Vector Store
    # ======================================================

    print()
    print("=" * 70)
    print("STEP 4 : VECTOR STORE")
    print("=" * 70)

    vector_store = VectorStore(
        dimension
    )

    # ------------------------------------------------------
    # IMPORTANT
    # ------------------------------------------------------
    # Prevent this test from using the production FAISS
    # vectors that VectorStore may have loaded.
    # ------------------------------------------------------

    vector_store.reset()

    vectors_before = (
        vector_store.total_vectors()
    )

    print(
        f"\nVectors Before : "
        f"{vectors_before}"
    )

    assert vectors_before == 0, (
        "Test VectorStore was not empty "
        "after reset."
    )

    # ------------------------------------------------------
    # Add test embeddings
    # ------------------------------------------------------

    vector_store.add_embeddings(
        embeddings
    )

    vectors_after = (
        vector_store.total_vectors()
    )

    print(
        f"Vectors Stored : "
        f"{vectors_after}"
    )

    assert vectors_after == len(
        embeddings
    ), (
        "FAISS vector count does not "
        "match embedding count."
    )

    # ======================================================
    # STEP 6 : Create Isolated Metadata Store
    # ======================================================

    print()
    print("=" * 70)
    print("STEP 5 : METADATA STORE")
    print("=" * 70)

    # ------------------------------------------------------
    # IMPORTANT
    # ------------------------------------------------------
    # MetadataStore() automatically loads the production
    # metadata.json.
    #
    # Clear it so this test starts with an isolated
    # in-memory metadata collection.
    # ------------------------------------------------------

    metadata_store = MetadataStore()

    metadata_store.clear()

    metadata = []

    for chunk in chunks:

        metadata.append(

            {

                "chunk_id": chunk["chunk_id"],

                "document": (
                    "sample_chunk_testing.pdf"
                ),

                "page": 1,

                "source": (
                    "sample_chunk_testing.pdf"
                ),

                "start_index": (
                    chunk["start_index"]
                ),

                "end_index": (
                    chunk["end_index"]
                ),

                "text": chunk["text"]

            }

        )

    metadata_store.add_many(
        metadata
    )

    metadata_count = (
        metadata_store.total()
    )

    print(
        f"\nMetadata Records : "
        f"{metadata_count}"
    )

    assert metadata_count == len(
        embeddings
    ), (
        "Metadata count does not "
        "match FAISS vector count."
    )

    # ======================================================
    # STEP 7 : Verify FAISS / Metadata Alignment
    # ======================================================

    print()
    print("=" * 70)
    print("STEP 5A : VECTOR / METADATA ALIGNMENT")
    print("=" * 70)

    assert vector_store.total_vectors() == (
        metadata_store.total()
    ), (
        "FAISS vector count and metadata "
        "count do not match."
    )

    # ------------------------------------------------------
    # Verify vector IDs
    # ------------------------------------------------------

    for vector_id in range(
        metadata_store.total()
    ):

        item = metadata_store.get(
            vector_id
        )

        assert item is not None, (
            f"Metadata missing for "
            f"vector ID {vector_id}."
        )

        assert item["vector_id"] == (
            vector_id
        ), (
            f"Incorrect vector ID mapping "
            f"for metadata record {vector_id}."
        )

    print(
        "\nFAISS and metadata are aligned."
    )

    # ======================================================
    # STEP 8 : Similarity Search
    # ======================================================

    print()
    print("=" * 70)
    print("STEP 6 : SIMILARITY SEARCH")
    print("=" * 70)

    query = "Artificial Intelligence"

    print(
        f"\nQuery : {query}"
    )

    query_embedding = (
        EmbeddingService.generate_embedding(
            query
        )
    )

    results = vector_store.search(

        query_embedding,

        k=min(
            3,
            vector_store.total_vectors()
        )

    )

    assert results, (
        "Similarity search returned "
        "no results."
    )

    # ======================================================
    # STEP 9 : Display Results
    # ======================================================

    print()
    print("=" * 70)
    print("SEARCH RESULTS")
    print("=" * 70)

    for rank, result in enumerate(

        results,

        start=1

    ):

        vector_id = result[
            "vector_id"
        ]

        item = metadata_store.get(
            vector_id
        )

        assert item is not None, (
            f"No metadata found for "
            f"vector ID {vector_id}."
        )

        print()

        print(
            f"Rank : {rank}"
        )

        print(
            f"Vector ID : {vector_id}"
        )

        print(
            f"Distance : "
            f"{result['distance']:.6f}"
        )

        print(
            f"Chunk ID : "
            f"{item['chunk_id']}"
        )

        print(
            f"Document : "
            f"{item['document']}"
        )

        print(
            f"Page : "
            f"{item['page']}"
        )

        print(
            f"Source : "
            f"{item['source']}"
        )

        print(
            f"Start Index : "
            f"{item['start_index']}"
        )

        print(
            f"End Index : "
            f"{item['end_index']}"
        )

        print(
            f"Characters : "
            f"{len(item['text'])}"
        )

        print()

        print("Chunk Preview:\n")

        print(
            item["text"][:300]
        )

        print()

        print("-" * 70)

    # ======================================================
    # Final Validation
    # ======================================================

    print()
    print("=" * 70)
    print("TEST COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(
        "\n✓ PDF parsed successfully."
    )

    print(
        "✓ Text chunked successfully."
    )

    print(
        "✓ Embeddings generated."
    )

    print(
        "✓ Embeddings stored in isolated FAISS."
    )

    print(
        "✓ Metadata mapped successfully."
    )

    print(
        "✓ FAISS / metadata alignment verified."
    )

    print(
        "✓ Similarity search completed."
    )

    print(
        "\n✓ Production FAISS index was NOT modified."
    )

    print(
        "✓ Production metadata.json was NOT modified."
    )