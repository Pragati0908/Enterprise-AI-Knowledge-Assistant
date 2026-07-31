import os

import faiss

import numpy as np


class VectorStore:

    def __init__(

        self,

        dimension

    ):

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(

            dimension

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

            dtype="float32"

        )

        self.index.add(

            embeddings

        )

    # ==========================================================
    # Save FAISS Index
    # ==========================================================

    def save(

        self,

        file_path

    ):

        os.makedirs(

            os.path.dirname(file_path),

            exist_ok=True

        )

        faiss.write_index(

            self.index,

            file_path

        )

    # ==========================================================
    # Load FAISS Index
    # ==========================================================

    def load(

        self,

        file_path

    ):

        self.index = faiss.read_index(

            file_path

        )

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

        k=5

    ):

        query_embedding = np.asarray(

            [query_embedding],

            dtype="float32"

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

            # Skip invalid indices (can occur if k > total vectors)
            if index == -1:

                continue

            results.append(

                {

                    "vector_id": int(index),

                    "distance": float(distance)

                }

            )

        return results