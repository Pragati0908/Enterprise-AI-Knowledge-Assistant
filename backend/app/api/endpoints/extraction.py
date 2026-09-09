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

Authentication
--------------
JWT Bearer Token Required

Analytics
---------
Extraction activity is recorded in the
extraction_analytics database table.
===============================================================
"""

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session


# ==========================================================
# Authentication
# ==========================================================

from app.auth.dependencies import (
    get_current_user
)


# ==========================================================
# Database
# ==========================================================

from app.db.database import (
    get_db
)

from app.db.models import (
    User
)


# ==========================================================
# Schemas
# ==========================================================

from app.schemas.extraction import (
    ExtractionRequest
)


# ==========================================================
# Services
# ==========================================================

from app.services.extraction_service import (
    ExtractionService
)

from app.services.analytics_service import (
    AnalyticsService
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

    request: ExtractionRequest,

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
    # Read Request Data
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

        result = ExtractionService.extract(
            text
        )


        # ==================================================
        # Record Analytics
        # ==================================================

        invoice = result.get(
            "invoice",
            {}
        )


        AnalyticsService.record_extraction(

            db=db,

            username=current_user.username,

            extraction_type="all",

            invoice_number=invoice.get(
                "invoice_number"
            ),

            vendor=invoice.get(
                "vendor"
            ),

            total_amount=invoice.get(
                "total_amount"
            )

        )


        return result


    # ======================================================
    # DATES
    # ======================================================

    if extraction_type == "dates":

        dates = (
            ExtractionService.extract_dates(
                text
            )
        )


        # ==================================================
        # Record Analytics
        # ==================================================

        AnalyticsService.record_extraction(

            db=db,

            username=current_user.username,

            extraction_type="dates"

        )


        return {

            "success": True,

            "dates": dates,

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


        # ==================================================
        # Record Analytics
        # ==================================================

        AnalyticsService.record_extraction(

            db=db,

            username=current_user.username,

            extraction_type="entities"

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

        invoice = (
            ExtractionService.extract_invoice(
                text
            )
        )


        # ==================================================
        # Record Analytics
        # ==================================================

        AnalyticsService.record_extraction(

            db=db,

            username=current_user.username,

            extraction_type="invoice",

            invoice_number=invoice.get(
                "invoice_number"
            ),

            vendor=invoice.get(
                "vendor"
            ),

            total_amount=invoice.get(
                "total_amount"
            )

        )


        return {

            "success": True,

            "invoice": invoice,

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