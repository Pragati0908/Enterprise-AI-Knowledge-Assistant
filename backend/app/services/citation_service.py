"""
===============================================================
Enterprise AI Knowledge Assistant

Citation Service

Responsibilities
----------------
1. Generate citations for retrieved chunks
2. Preserve document information
3. Preserve page information
4. Preserve chunk information
5. Preserve similarity distance
6. Format citations for frontend display
===============================================================
"""

import logging


logger = logging.getLogger(__name__)


class CitationService:

    # ==========================================================
    # Create Citation
    # ==========================================================

    @staticmethod
    def create_citation(
        result: dict
    ) -> dict:

        document = result.get(
            "document",
            "Unknown document"
        )

        page = result.get(
            "page",
            1
        )

        chunk_id = result.get(
            "chunk_id",
            "Unknown"
        )

        distance = result.get(
            "distance",
            0
        )

        citation_text = (
            f"[{document} | "
            f"Page {page} | "
            f"Chunk {chunk_id}]"
        )

        return {
            "document": document,
            "page": page,
            "chunk_id": chunk_id,
            "distance": distance,
            "citation": citation_text
        }

    # ==========================================================
    # Create Multiple Citations
    # ==========================================================

    @classmethod
    def create_citations(
        cls,
        results: list
    ) -> list:

        citations = []

        for result in results:

            citations.append(
                cls.create_citation(
                    result
                )
            )

        return citations