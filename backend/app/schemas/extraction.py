"""
===============================================================
Enterprise AI Knowledge Assistant

Information Extraction Schemas
===============================================================
"""

from pydantic import BaseModel, Field


# ==============================================================
# General Extraction Request
# ==============================================================

class ExtractionRequest(BaseModel):

    text: str = Field(
        min_length=1,
        description="Text from which information will be extracted."
    )

    extraction_type: str = Field(
        default="all",
        description=(
            "Type of information extraction to perform. "
            "Supported values: all, dates, entities, invoice."
        )
    )


# ==============================================================
# General Extraction Response
# ==============================================================

class ExtractionResponse(BaseModel):

    success: bool

    dates: list[str] = []

    names: list[str] = []

    organizations: list[str] = []

    message: str = ""


# ==============================================================
# Invoice Data
# ==============================================================

class InvoiceData(BaseModel):

    invoice_number: str | None = None

    invoice_date: str | None = None

    due_date: str | None = None

    vendor: str | None = None

    customer: str | None = None

    subtotal: float | None = None

    tax: float | None = None

    total_amount: float | None = None

    currency: str | None = None