from pathlib import Path

import faiss
import numpy as np


class VectorStore:
    """
    ==========================================================
    FAISS Vector Store

    Responsibilities
    ----------------
    • Store embeddings
    • Save FAISS index
    • Load FAISS index
    • Perform similarity search

    Default embedding dimension = 384
    (SentenceTransformer: all-MiniLM-L6-v2)
    ==========================================================
    """

    def __init__(
        self,
        dimension: int = 384
    ):

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        # ======================================================
        # Project Paths
        # ======================================================

        self.project_root = Path(__file__).resolve().parents[3]

        self.vector_db = (
            self.project_root /
            "backend" /
            "vector_db"
        )

        self.vector_db.mkdir(
            parents=True,
            exist_ok=True
        )

        self.default_index_path = (
            self.vector_db /
            "faiss.index"
        )

    # ==========================================================
    # Add Embeddings
    # ==========================================================

    def add_embeddings(
        self,
        embeddings
    ):

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32
        )

        self.index.add(
            embeddings
        )

    # ==========================================================
    # Save FAISS Index
    # ==========================================================

    def save(
        self,
        file_path=None
    ):

        if file_path is None:

            file_path = self.default_index_path

        else:

            file_path = Path(file_path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(file_path)
        )

        print("\nFAISS index saved successfully.")
        print(f"Location : {file_path.resolve()}")
        print(f"Vectors  : {self.total_vectors()}\n")

    # ==========================================================
    # Load FAISS Index
    # ==========================================================

    def load(
        self,
        file_path=None
    ):

        if file_path is None:

            file_path = self.default_index_path

        else:

            file_path = Path(file_path)

        if not file_path.exists():

            raise FileNotFoundError(
                f"FAISS index not found : {file_path}"
            )

        self.index = faiss.read_index(
            str(file_path)
        )

        print("\nFAISS index loaded successfully.")
        print(f"Location : {file_path.resolve()}")
        print(f"Vectors  : {self.total_vectors()}\n")

    # ==========================================================
    # Total Stored Vectors
    # ==========================================================

    def total_vectors(
        self
    ):

        return self.index.ntotal

    # ==========================================================
    # Similarity Search
    # ==========================================================

    def search(
        self,
        query_embedding,
        k: int = 5
    ):

        query_embedding = np.asarray(
            [query_embedding],
            dtype=np.float32
        )

        distances, indices = self.index.search(
            query_embedding,
            k
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

    # ==========================================================
    # Check if Index Exists
    # ==========================================================

    def exists(
        self
    ) -> bool:

        return self.default_index_path.exists()

    # ==========================================================
    # Reset Index
    # ==========================================================

    def reset(
        self
    ):

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        print("FAISS index reset successfully.")