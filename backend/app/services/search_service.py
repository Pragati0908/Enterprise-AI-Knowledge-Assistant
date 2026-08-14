"""
===============================================================
Enterprise AI Knowledge Assistant

Search Service

Responsibilities
----------------
1. Accept a search query
2. Call the existing Retriever
3. Search across all indexed documents
4. Organize retrieved results
5. Return document and chunk information

Important
---------
SearchService does NOT implement FAISS search.

It uses the existing Retriever service.
===============================================================
"""

import logging

from app.services.retriever import Retriever


# ============================================================
# Logging
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# Search Service
# ============================================================

class SearchService:
    """
    Application-level search service.

    Search flow:

        User Query
             |
             v
        SearchService
             |
             v
          Retriever
             |
             v
       EmbeddingService
             |
             v
          FAISS
             |
             v
       MetadataStore
             |
             v
      Multiple Documents
    """

    # ========================================================
    # Constructor
    # ========================================================

    def __init__(
        self,
        retriever: Retriever
    ):

        self.retriever = retriever

    # ========================================================
    # Search
    # ========================================================

    def search(
        self,
        query: str,
        top_k: int = 10
    ) -> dict:
        """
        Search across all indexed documents.

        Parameters
        ----------
        query:
            User's semantic search query.

        top_k:
            Maximum number of chunks to retrieve.

        Returns
        -------
        dict
            Search results containing chunks from
            all indexed documents.
        """

        # ----------------------------------------------------
        # Validate query
        # ----------------------------------------------------

        if not query or not query.strip():

            return {
                "success": False,
                "query": query,
                "total_results": 0,
                "results": [],
                "error": "Search query cannot be empty."
            }

        # ----------------------------------------------------
        # Normalize query
        # ----------------------------------------------------

        query = query.strip()

        logger.info("=" * 70)
        logger.info("MULTI-DOCUMENT SEARCH")
        logger.info("=" * 70)

        logger.info(
            "Query : %s",
            query
        )

        logger.info(
            "Top K : %d",
            top_k
        )

        # ----------------------------------------------------
        # Call EXISTING Retriever
        # ----------------------------------------------------

        try:

            retrieved_chunks = self.retriever.retrieve(
                query=query,
                top_k=top_k
            )

        except Exception as error:

            logger.exception(
                "Multi-document retrieval failed."
            )

            return {
                "success": False,
                "query": query,
                "total_results": 0,
                "results": [],
                "error": str(error)
            }

        # ----------------------------------------------------
        # No results
        # ----------------------------------------------------

        if not retrieved_chunks:

            logger.info(
                "No matching chunks found."
            )

            return {
                "success": True,
                "query": query,
                "total_results": 0,
                "results": []
            }

        # ----------------------------------------------------
        # Organize results
        # ----------------------------------------------------

        results = []

        for chunk in retrieved_chunks:

            results.append(
                {
                    "chunk_id": chunk.get("chunk_id"),
                    "document": chunk.get("document"),
                    "page": chunk.get("page"),
                    "distance": chunk.get("distance"),
                    "text": chunk.get("text", "")
                }
            )

        # ----------------------------------------------------
        # Log document distribution
        # ----------------------------------------------------

        documents = set()

        for result in results:

            document = result.get("document")

            if document:

                documents.add(document)

        logger.info(
            "Total chunks retrieved : %d",
            len(results)
        )

        logger.info(
            "Documents represented : %d",
            len(documents)
        )

        for document in sorted(documents):

            logger.info(
                "Document found : %s",
                document
            )

        logger.info("=" * 70)

        # ----------------------------------------------------
        # Return
        # ----------------------------------------------------

        return {
            "success": True,
            "query": query,
            "total_results": len(results),
            "documents_found": len(documents),
            "documents": sorted(documents),
            "results": results
        }