from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.metadata_store import MetadataStore


class Retriever:
    """
    =========================================================
    Retriever Service

    Responsibilities
    ----------------
    1. Convert user query into embedding
    2. Search FAISS index
    3. Retrieve metadata
    4. Return ranked document chunks
    =========================================================
    """

    def __init__(
        self,
        vector_store: VectorStore | None = None,
        metadata_store: MetadataStore | None = None
   ):

        if vector_store is None:

           vector_store = VectorStore()

           vector_store.load()

        if metadata_store is None:

           metadata_store = MetadataStore()

           metadata_store.load()

        self.vector_store = vector_store

        self.metadata_store = metadata_store

    # ======================================================
    # Retrieve Similar Chunks
    # ======================================================

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        # --------------------------------------------------
        # Generate query embedding
        # --------------------------------------------------

        query_embedding = EmbeddingService.generate_embedding(
            query
        )

        # --------------------------------------------------
        # Search FAISS
        # --------------------------------------------------

        results = self.vector_store.search(
            query_embedding,
            top_k
        )

        retrieved_chunks = []

        # --------------------------------------------------
        # Match metadata
        # --------------------------------------------------

        for result in results:

            metadata = self.metadata_store.get(
                result["vector_id"]
            )

            if metadata is None:
                continue

            retrieved_chunks.append(

                {
                    "chunk_id": metadata.get("chunk_id"),
                    "document": metadata.get("document"),
                    "page": metadata.get("page", 1),
                    "distance": result["distance"],
                    "text": metadata.get("text", "")
                }

            )

        return retrieved_chunks