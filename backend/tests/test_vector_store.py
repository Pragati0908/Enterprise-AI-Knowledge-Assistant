"""
===============================================================
Enterprise AI Knowledge Assistant

Vector Store Test

Purpose
-------
Test FAISS vector creation, insertion, saving and loading
without modifying the application's persistent FAISS index.

IMPORTANT
---------
This test uses a temporary FAISS file.

It DOES NOT modify:

    backend/vector_db/faiss.index
===============================================================
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore


# ==========================================================
# TEST DATA
# ==========================================================

texts = [

    "Artificial Intelligence",

    "Machine Learning",

    "Natural Language Processing",

    "Deep Learning"

]


# ==========================================================
# TEST
# ==========================================================

def test_vector_store():

    print("\n")
    print("=" * 70)
    print("VECTOR STORE TEST")
    print("=" * 70)

    # ------------------------------------------------------
    # Generate embeddings
    # ------------------------------------------------------

    embeddings = EmbeddingService.generate_embeddings(
        texts
    )

    dimension = len(
        embeddings[0]
    )

    print(
        f"\nEmbedding Dimension : {dimension}"
    )

    print(
        f"Total Texts         : {len(texts)}"
    )

    # ------------------------------------------------------
    # Temporary directory
    # ------------------------------------------------------

    with TemporaryDirectory() as temp_dir:

        temp_path = Path(
            temp_dir
        )

        test_index_path = (
            temp_path
            / "faiss_test.index"
        )

        print(
            f"\nTemporary Index     : "
            f"{test_index_path}"
        )

        # --------------------------------------------------
        # Create isolated VectorStore
        # --------------------------------------------------

        store = VectorStore(
            dimension
        )

        # --------------------------------------------------
        # IMPORTANT
        # --------------------------------------------------
        # VectorStore() may automatically load the
        # application's persistent FAISS index.
        #
        # Therefore explicitly reset the in-memory index
        # before using it for this isolated test.
        # --------------------------------------------------

        store.reset()

        vectors_before = (
            store.total_vectors()
        )

        print(
            f"\nVectors Before      : "
            f"{vectors_before}"
        )

        # --------------------------------------------------
        # Add embeddings
        # --------------------------------------------------

        store.add_embeddings(
            embeddings
        )

        vectors_after = (
            store.total_vectors()
        )

        print(
            f"Vectors After       : "
            f"{vectors_after}"
        )

        # --------------------------------------------------
        # Validate vector count
        # --------------------------------------------------

        assert vectors_before == 0, (
            "Temporary test VectorStore "
            "was not empty."
        )

        assert vectors_after == len(
            embeddings
        ), (
            "Unexpected number of vectors "
            "stored in test VectorStore."
        )

        # --------------------------------------------------
        # Save to temporary location
        # --------------------------------------------------

        store.save(
            test_index_path
        )

        assert test_index_path.exists(), (
            "Temporary FAISS index was not created."
        )

        print(
            "\nIndex Saved Successfully"
        )

        # --------------------------------------------------
        # Load into a new VectorStore
        # --------------------------------------------------

        new_store = VectorStore(
            dimension
        )

        # The constructor may load the application's
        # persistent index, so reset first.

        new_store.reset()

        new_store.load(
            test_index_path
        )

        loaded_vectors = (
            new_store.total_vectors()
        )

        print(
            "Index Loaded Successfully"
        )

        print(
            f"\nLoaded Vectors      : "
            f"{loaded_vectors}"
        )

        # --------------------------------------------------
        # Validate loaded count
        # --------------------------------------------------

        assert loaded_vectors == len(
            embeddings
        ), (
            "Loaded FAISS vector count "
            "does not match expected count."
        )

        print("\nTEST PASSED")

    # ------------------------------------------------------
    # TemporaryDirectory is automatically deleted here.
    # ------------------------------------------------------

    print(
        "\nTemporary FAISS index removed."
    )

    print(
        "Production FAISS index was NOT modified."
    )

    print("\n" + "=" * 70)