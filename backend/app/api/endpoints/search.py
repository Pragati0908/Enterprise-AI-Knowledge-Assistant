"""
===============================================================
Enterprise AI Knowledge Assistant

Search API

Endpoint
--------
POST /search

Responsibilities
----------------
1. Receive search query
2. Call SearchService
3. Generate citations
4. Return search results
===============================================================
"""

from fastapi import APIRouter

from app.schemas.search import SearchRequest
from app.services.retriever import Retriever
from app.services.search_service import SearchService
from app.services.citation_service import CitationService


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/search",
    tags=["Multi-document Search"]
)


# ==========================================================
# Initialize Services
# ==========================================================

retriever = Retriever()

search_service = SearchService(
    retriever=retriever
)


# ==========================================================
# Search Endpoint
# ==========================================================

@router.post("")
def search_documents(
    request: SearchRequest
):

    result = search_service.search(

        query=request.query,

        top_k=request.top_k

    )

    # ------------------------------------------------------
    # Search failed
    # ------------------------------------------------------

    if not result["success"]:

        return result

    # ------------------------------------------------------
    # Generate citations
    # ------------------------------------------------------

    citations = CitationService.create_citations(

        result["results"]

    )

    # ------------------------------------------------------
    # Attach citation to each result
    # ------------------------------------------------------

    for result_item, citation in zip(
        result["results"],
        citations
    ):

        result_item["citation"] = (
            citation["citation"]
        )

    # ------------------------------------------------------
    # Final response
    # ------------------------------------------------------

    return result