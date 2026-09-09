"""
===============================================================
Enterprise AI Knowledge Assistant

Search API

Endpoint
--------
POST /search

Responsibilities
----------------
1. Authenticate user using JWT
2. Receive search query
3. Call SearchService
4. Generate citations
5. Record search analytics
6. Return search results
===============================================================
"""

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.schemas.search import (
    SearchRequest
)

from app.services.retriever import (
    Retriever
)

from app.services.search_service import (
    SearchService
)

from app.services.citation_service import (
    CitationService
)

from app.services.analytics_service import (
    AnalyticsService
)

from app.auth.dependencies import (
    get_current_user
)

from app.db.database import (
    get_db
)

from app.db.models import (
    User
)


# ==========================================================
# Router
# ==========================================================

router = APIRouter(

    prefix="/search",

    tags=[
        "Multi-document Search"
    ]

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

    request: SearchRequest,

    # ======================================================
    # JWT Authentication
    # ======================================================

    current_user: User = Depends(

        get_current_user

    ),

    # ======================================================
    # Database Session
    # ======================================================

    db: Session = Depends(

        get_db

    )

):

    # ======================================================
    # Perform Search
    # ======================================================

    result = search_service.search(

        query=request.query,

        top_k=request.top_k

    )


    # ======================================================
    # Search Failed
    # ======================================================

    if not result["success"]:

        return result


    # ======================================================
    # Generate Citations
    # ======================================================

    citations = CitationService.create_citations(

        result["results"]

    )


    # ======================================================
    # Attach Citation to Each Result
    # ======================================================

    for result_item, citation in zip(

        result["results"],

        citations

    ):

        result_item["citation"] = (

            citation["citation"]

        )


    # ======================================================
    # Determine Result Count
    # ======================================================

    results_count = len(

        result["results"]

    )


    # ======================================================
    # Record Search Analytics
    # ======================================================

    try:

        AnalyticsService.record_search(

            db=db,

            username=current_user.username,

            query=request.query,

            search_type="multi-document",

            top_k=request.top_k,

            results_count=results_count

        )

    except Exception as error:

        # --------------------------------------------------
        # Search itself succeeded.
        # Analytics failure should not break the search.
        # --------------------------------------------------

        print(

            "Search analytics recording failed: "

            f"{error}"

        )


    # ======================================================
    # Final Response
    # ======================================================

    return result
