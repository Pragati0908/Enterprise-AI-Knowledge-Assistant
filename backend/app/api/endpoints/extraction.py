"""
===============================================================
Enterprise AI Knowledge Assistant

Information Extraction API

Endpoint
--------
POST /extraction

Supported extraction types
--------------------------
1. all
2. dates
3. entities
4. invoice
===============================================================
"""

from fastapi import APIRouter

from app.schemas.extraction import (
    ExtractionRequest
)

from app.services.extraction_service import (
    ExtractionService
)


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="",
    tags=[
        "Information Extraction"
    ]
)


# ==========================================================
# POST /extraction
# ==========================================================

@router.post(
    "/extraction"
)
def extract_information(
    request: ExtractionRequest
):

    # ======================================================
    # Read request data
    # ======================================================

    text = request.text.strip()

    extraction_type = (
        request.extraction_type
        .strip()
        .lower()
    )

    # ======================================================
    # ALL
    # ======================================================

    if extraction_type == "all":

        return (
            ExtractionService.extract(
                text
            )
        )

    # ======================================================
    # DATES
    # ======================================================

    if extraction_type == "dates":

        return {

            "success": True,

            "dates":
                ExtractionService.extract_dates(
                    text
                ),

            "message":
                "Date extraction completed."
        }

    # ======================================================
    # ENTITIES
    # ======================================================

    if extraction_type == "entities":

        entities = (
            ExtractionService.extract_entities(
                text
            )
        )

        return {

            "success": True,

            "names":
                entities["names"],

            "organizations":
                entities["organizations"],

            "message":
                "Entity extraction completed."
        }

    # ======================================================
    # INVOICE
    # ======================================================

    if extraction_type == "invoice":

        return {

            "success": True,

            "invoice":
                ExtractionService.extract_invoice(
                    text
                ),

            "message":
                "Invoice extraction completed."
        }

    # ======================================================
    # INVALID EXTRACTION TYPE
    # ======================================================

    return {

        "success": False,

        "error":
            "Unsupported extraction type.",

        "supported_types": [
            "all",
            "dates",
            "entities",
            "invoice"
        ]
    }