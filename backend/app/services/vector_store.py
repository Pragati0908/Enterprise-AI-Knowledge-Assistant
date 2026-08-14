"""
==========================================================
Enterprise AI Knowledge Assistant

FAISS Vector Store

Responsibilities
----------------
• Store embeddings
• Persist FAISS index
• Load existing FAISS index
• Append embeddings from multiple documents
• Perform similarity search
• Report total stored vectors
• Reset index when explicitly requested

Default embedding dimension = 384
SentenceTransformer:
sentence-transformers/all-MiniLM-L6-v2

IMPORTANT
---------
The FAISS index is persistent.

When a VectorStore object is created:

    If faiss.index exists
        -> load existing index

    If faiss.index does not exist
        -> create new index

Therefore, adding embeddings for a new document
does NOT replace embeddings from previous documents.
==========================================================
"""

from pathlib import Path

import faiss
import numpy as np


class VectorStore:
    """
    Persistent FAISS vector store.

    Multiple documents share the same FAISS index.

    Example:

        Document A
             ↓
          12 vectors
             ↓
        FAISS index
             ↓
        Document B
             ↓
          15 vectors
             ↓
        SAME FAISS index
             ↓
          27 vectors
    """

    # ======================================================
    # Constructor
    # ======================================================

    def __init__(
        self,
        dimension: int = 384
    ):
        """
        Initialize the VectorStore.

        If a saved FAISS index already exists,
        it is loaded automatically.

        Otherwise, a new empty FAISS index
        is created.
        """

        self.dimension = dimension

        # ==================================================
        # Project Paths
        # ==================================================

        self.project_root = (
            Path(__file__).resolve().parents[3]
        )

        self.vector_db = (
            self.project_root
            / "backend"
            / "vector_db"
        )

        self.vector_db.mkdir(
            parents=True,
            exist_ok=True
        )

        self.default_index_path = (
            self.vector_db
            / "faiss.index"
        )

        # ==================================================
        # Initialize / Load Index
        # ==================================================

        if self.default_index_path.exists():

            try:

                self.index = faiss.read_index(
                    str(self.default_index_path)
                )

                # ------------------------------------------
                # Validate dimension
                # ------------------------------------------

                if self.index.d != self.dimension:

                    raise ValueError(
                        "FAISS index dimension mismatch. "
                        f"Expected {self.dimension}, "
                        f"but existing index has "
                        f"dimension {self.index.d}."
                    )

                print(
                    "\nExisting FAISS index loaded."
                )

                print(
                    f"Location : "
                    f"{self.default_index_path.resolve()}"
                )

                print(
                    f"Vectors  : "
                    f"{self.index.ntotal}\n"
                )

            except Exception as error:

                raise RuntimeError(
                    "Failed to load existing FAISS "
                    f"index: {error}"
                ) from error

        else:

            self.index = faiss.IndexFlatL2(
                self.dimension
            )

            print(
                "\nNew FAISS index created."
            )

            print(
                f"Dimension : {self.dimension}"
            )

            print(
                f"Location  : "
                f"{self.default_index_path.resolve()}"
            )

            print(
                "Vectors   : 0\n"
            )

    # ======================================================
    # Add Embeddings
    # ======================================================

    def add_embeddings(
        self,
        embeddings
    ):
        """
        Add embeddings to the EXISTING FAISS index.

        IMPORTANT:
        This method does not recreate the index.

        Therefore:

            Existing vectors
                    +
            New vectors
                    =
            Combined index
        """

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32
        )

        # --------------------------------------------------
        # Validate input
        # --------------------------------------------------

        if embeddings.size == 0:

            print(
                "No embeddings provided. "
                "Nothing was added."
            )

            return

        # --------------------------------------------------
        # Ensure 2-dimensional shape
        # --------------------------------------------------

        if embeddings.ndim == 1:

            embeddings = embeddings.reshape(
                1,
                -1
            )

        # --------------------------------------------------
        # Validate embedding dimension
        # --------------------------------------------------

        if embeddings.shape[1] != self.dimension:

            raise ValueError(
                "Embedding dimension mismatch. "
                f"Expected {self.dimension}, "
                f"received {embeddings.shape[1]}."
            )

        # --------------------------------------------------
        # Vector count before adding
        # --------------------------------------------------

        vectors_before = self.index.ntotal

        # --------------------------------------------------
        # Add vectors
        # --------------------------------------------------

        self.index.add(
            embeddings
        )

        # --------------------------------------------------
        # Vector count after adding
        # --------------------------------------------------

        vectors_after = self.index.ntotal

        vectors_added = (
            vectors_after
            - vectors_before
        )

        print(
            "\nFAISS embeddings added."
        )

        print(
            f"Vectors before : {vectors_before}"
        )

        print(
            f"Vectors added  : {vectors_added}"
        )

        print(
            f"Vectors after  : {vectors_after}\n"
        )

    # ======================================================
    # Save FAISS Index
    # ======================================================

    def save(
        self,
        file_path=None
    ):
        """
        Persist the current FAISS index to disk.

        If no path is supplied, the default
        persistent index is used.
        """

        if file_path is None:

            file_path = (
                self.default_index_path
            )

        else:

            file_path = Path(
                file_path
            )

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(file_path)
        )

        print(
            "\nFAISS index saved successfully."
        )

        print(
            f"Location : "
            f"{file_path.resolve()}"
        )

        print(
            f"Vectors  : "
            f"{self.total_vectors()}\n"
        )

    # ======================================================
    # Load FAISS Index
    # ======================================================

    def load(
        self,
        file_path=None
    ):
        """
        Explicitly load a FAISS index from disk.

        This method is useful when you want to
        manually load a specific index.
        """

        if file_path is None:

            file_path = (
                self.default_index_path
            )

        else:

            file_path = Path(
                file_path
            )

        if not file_path.exists():

            raise FileNotFoundError(
                "FAISS index not found: "
                f"{file_path}"
            )

        loaded_index = faiss.read_index(
            str(file_path)
        )

        # --------------------------------------------------
        # Validate dimension
        # --------------------------------------------------

        if loaded_index.d != self.dimension:

            raise ValueError(
                "FAISS index dimension mismatch. "
                f"Expected {self.dimension}, "
                f"but loaded index has "
                f"dimension {loaded_index.d}."
            )

        self.index = loaded_index

        print(
            "\nFAISS index loaded successfully."
        )

        print(
            f"Location : "
            f"{file_path.resolve()}"
        )

        print(
            f"Vectors  : "
            f"{self.total_vectors()}\n"
        )

    # ======================================================
    # Total Stored Vectors
    # ======================================================

    def total_vectors(
        self
    ):
        """
        Return total number of vectors currently
        stored in the FAISS index.
        """

        return self.index.ntotal

    # ======================================================
    # Similarity Search
    # ======================================================

    def search(
        self,
        query_embedding,
        k: int = 5
    ):
        """
        Search the FAISS index.

        Returns vector IDs and distances.
        """

        if self.index.ntotal == 0:

            return []

        # --------------------------------------------------
        # Prevent requesting more vectors than available
        # --------------------------------------------------

        k = min(
            k,
            self.index.ntotal
        )

        query_embedding = np.asarray(
            [query_embedding],
            dtype=np.float32
        )

        # --------------------------------------------------
        # Validate query dimension
        # --------------------------------------------------

        if query_embedding.shape[1] != self.dimension:

            raise ValueError(
                "Query embedding dimension mismatch. "
                f"Expected {self.dimension}, "
                f"received {query_embedding.shape[1]}."
            )

        # --------------------------------------------------
        # FAISS Search
        # --------------------------------------------------

        distances, indices = (
            self.index.search(
                query_embedding,
                k
            )
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index == -1:

                continue

            results.append(
                {
                    "vector_id": int(index),
                    "distance": float(distance)
                }
            )

        return results

    # ======================================================
    # Check if Index Exists
    # ======================================================

    def exists(
        self
    ) -> bool:
        """
        Return True if the persistent FAISS
        index exists.
        """

        return (
            self.default_index_path.exists()
        )

    # ======================================================
    # Reset Index
    # ======================================================

    def reset(
        self
    ):
        """
        Explicitly delete all vectors from the
        current in-memory index.

        IMPORTANT:
        This does NOT automatically save the empty
        index to disk.
        """

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        print(
            "FAISS index reset successfully."
        )

        print(
            "Current vectors : 0"
        )