"""
===============================================================
Enterprise AI Knowledge Assistant

Information Extraction Service

Responsibilities
----------------
1. Extract dates
2. Extract person names
3. Extract organizations
4. Extract invoice fields
5. Remove known false-positive organizations
6. Return structured information
===============================================================
"""

import re

import spacy


class ExtractionService:

    # ==========================================================
    # Load NLP Model
    # ==========================================================

    nlp = spacy.load(
        "en_core_web_sm"
    )

    # ==========================================================
    # Date Patterns
    # ==========================================================

    DATE_PATTERNS = [

        # DD/MM/YYYY
        r"\b\d{1,2}/\d{1,2}/\d{4}\b",

        # DD-MM-YYYY
        r"\b\d{1,2}-\d{1,2}-\d{4}\b",

        # YYYY-MM-DD
        r"\b\d{4}-\d{1,2}-\d{2}\b",

        # DD Month YYYY
        r"\b\d{1,2}\s+"
        r"(?:January|February|March|April|May|June|"
        r"July|August|September|October|November|December)"
        r"\s+\d{4}\b",

        # Month DD, YYYY
        r"\b"
        r"(?:January|February|March|April|May|June|"
        r"July|August|September|October|November|December)"
        r"\s+\d{1,2},\s+\d{4}\b"
    ]

    # ==========================================================
    # False-Positive Organizations
    # ==========================================================

    INVALID_ORGANIZATIONS = {

        "invoice date",
        "due date",
        "invoice number",
        "invoice no",
        "invoice #",
        "date",
        "total",
        "total amount",
        "amount",
        "subtotal",
        "tax",
        "tax amount",
        "balance",
        "payment terms",
        "billing address",
        "shipping address",
        "customer",
        "vendor",
        "description",
        "quantity",
        "unit price",
        "price"
    }

    # ==========================================================
    # Extract Dates
    # ==========================================================

    @classmethod
    def extract_dates(cls, text):

        dates = []

        for pattern in cls.DATE_PATTERNS:

            matches = re.findall(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            dates.extend(
                matches
            )

        # Remove duplicates while preserving order
        return list(
            dict.fromkeys(
                dates
            )
        )

    # ==========================================================
    # Extract Named Entities
    # ==========================================================

    @classmethod
    def extract_entities(cls, text):

        document = cls.nlp(
            text
        )

        names = []

        organizations = []

        for entity in document.ents:

            # --------------------------------------------------
            # PERSON
            # --------------------------------------------------

            if entity.label_ == "PERSON":

                name = entity.text.strip()

                if name:

                    names.append(
                        name
                    )

            # --------------------------------------------------
            # ORGANIZATION
            # --------------------------------------------------

            elif entity.label_ == "ORG":

                organization = (
                    entity.text.strip()
                )

                # Remove known false positives

                if (
                    organization.lower()
                    in cls.INVALID_ORGANIZATIONS
                ):

                    continue

                if organization:

                    organizations.append(
                        organization
                    )

        return {

            "names": list(
                dict.fromkeys(
                    names
                )
            ),

            "organizations": list(
                dict.fromkeys(
                    organizations
                )
            )
        }

    # ==========================================================
    # Extract Invoice Number
    # ==========================================================

    @classmethod
    def extract_invoice_number(cls, text):

        pattern = (
            r"(?:Invoice\s*(?:Number|No\.?|#))"
            r"\s*[:\-]?\s*"
            r"([A-Z0-9][A-Z0-9\-/]*)"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            return match.group(
                1
            ).strip()

        return None

    # ==========================================================
    # Extract Invoice Date
    # ==========================================================

    @classmethod
    def extract_invoice_date(cls, text):

        pattern = (
            r"Invoice\s+Date"
            r"\s*[:\-]?\s*"
            r"("
            r"\d{1,2}/\d{1,2}/\d{4}"
            r"|"
            r"\d{1,2}-\d{1,2}-\d{4}"
            r"|"
            r"\d{4}-\d{1,2}-\d{1,2}"
            r"|"
            r"\d{1,2}\s+"
            r"(?:January|February|March|April|May|June|"
            r"July|August|September|October|November|December)"
            r"\s+\d{4}"
            r"|"
            r"(?:January|February|March|April|May|June|"
            r"July|August|September|October|November|December)"
            r"\s+\d{1,2},\s+\d{4}"
            r")"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            return match.group(
                1
            ).strip()

        return None

    # ==========================================================
    # Extract Due Date
    # ==========================================================

    @classmethod
    def extract_due_date(cls, text):

        pattern = (
            r"Due\s+Date"
            r"\s*[:\-]?\s*"
            r"("
            r"\d{1,2}/\d{1,2}/\d{4}"
            r"|"
            r"\d{1,2}-\d{1,2}-\d{4}"
            r"|"
            r"\d{4}-\d{1,2}-\d{1,2}"
            r"|"
            r"\d{1,2}\s+"
            r"(?:January|February|March|April|May|June|"
            r"July|August|September|October|November|December)"
            r"\s+\d{4}"
            r"|"
            r"(?:January|February|March|April|May|June|"
            r"July|August|September|October|November|December)"
            r"\s+\d{1,2},\s+\d{4}"
            r")"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            return match.group(
                1
            ).strip()

        return None

    # ==========================================================
    # Extract Vendor
    # ==========================================================

    @classmethod
    def extract_vendor(cls, text):

        pattern = (
            r"^\s*Vendor"
            r"\s*[:\-]\s*"
            r"([^\n\r]+)"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.MULTILINE
        )

        if match:

            return match.group(
                1
            ).strip()

        return None

    # ==========================================================
    # Extract Customer
    # ==========================================================

    @classmethod
    def extract_customer(cls, text):

        pattern = (
            r"^\s*Customer"
            r"\s*[:\-]\s*"
            r"([^\n\r]+)"
        )

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE | re.MULTILINE
        )

        if match:

            return match.group(
                1
            ).strip()

        return None

    # ==========================================================
    # Extract Amount
    # ==========================================================

    @classmethod
    def extract_amount(
        cls,
        text,
        label_pattern
    ):

        """
        Extract an amount associated with a field label.

        Examples:

        Total: ₹5000

        Grand Total: ₹11,800.00

        Invoice Date: 12/08/2026. Total: ₹5000.
        """

        pattern = (
            r"(?:^|[\n\r\.])"
            r"\s*"
            r"(?:"
            + label_pattern
            + r")"
            r"\s*[:\-]?\s*"
            r"(?:₹|Rs\.?|INR|\$|USD|€|EUR|£|GBP)?"
            r"\s*"
            r"([\d,]+(?:\.\d{1,2})?)"
        )

        matches = re.findall(
            pattern,
            text,
            flags=(
                re.IGNORECASE
                | re.MULTILINE
            )
        )

        if not matches:

            return None

        amount_text = matches[-1]

        amount_text = amount_text.replace(
            ",",
            ""
        )

        return float(
            amount_text
        )

    # ==========================================================
    # Extract Currency
    # ==========================================================

    @classmethod
    def extract_currency(cls, text):

        # ------------------------------------------------------
        # Indian Rupee
        # ------------------------------------------------------

        if (
            "₹" in text
            or re.search(
                r"\bINR\b",
                text,
                flags=re.IGNORECASE
            )
        ):

            return "INR"

        # ------------------------------------------------------
        # US Dollar
        # ------------------------------------------------------

        if (
            "$" in text
            or re.search(
                r"\bUSD\b",
                text,
                flags=re.IGNORECASE
            )
        ):

            return "USD"

        # ------------------------------------------------------
        # Euro
        # ------------------------------------------------------

        if (
            "€" in text
            or re.search(
                r"\bEUR\b",
                text,
                flags=re.IGNORECASE
            )
        ):

            return "EUR"

        # ------------------------------------------------------
        # British Pound
        # ------------------------------------------------------

        if (
            "£" in text
            or re.search(
                r"\bGBP\b",
                text,
                flags=re.IGNORECASE
            )
        ):

            return "GBP"

        return None

        # ==========================================================
    # Complete Invoice Extraction
    # ==========================================================

    @classmethod
    def extract_invoice(cls, text):

        # ------------------------------------------------------
        # Invoice Number
        # ------------------------------------------------------

        invoice_number = (
            cls.extract_invoice_number(
                text
            )
        )

        # ------------------------------------------------------
        # Invoice Date
        # ------------------------------------------------------

        invoice_date = (
            cls.extract_invoice_date(
                text
            )
        )

        # ------------------------------------------------------
        # Due Date
        # ------------------------------------------------------

        due_date = (
            cls.extract_due_date(
                text
            )
        )

        # ------------------------------------------------------
        # Vendor
        # ------------------------------------------------------

        vendor = (
            cls.extract_vendor(
                text
            )
        )

        # ------------------------------------------------------
        # Customer
        # ------------------------------------------------------

        customer = (
            cls.extract_customer(
                text
            )
        )

        # ------------------------------------------------------
        # Subtotal
        # ------------------------------------------------------

        subtotal = (
            cls.extract_amount(
                text,
                r"\bSubtotal\b"
            )
        )

        # ------------------------------------------------------
        # Tax / GST
        # ------------------------------------------------------

        tax = (
            cls.extract_amount(
                text,
                r"\b(?:Tax|GST)\b"
            )
        )

        # ------------------------------------------------------
        # Grand Total
        # ------------------------------------------------------

        total = (
            cls.extract_amount(
                text,
                r"\bGrand\s+Total\b"
            )
        )

        # ------------------------------------------------------
        # Normal Total
        #
        # Used only if Grand Total does not exist.
        # ------------------------------------------------------

        if total is None:

            total = (
                cls.extract_amount(
                    text,
                    r"\bTotal\b"
                )
            )

        # ------------------------------------------------------
        # Currency
        # ------------------------------------------------------

        currency = (
            cls.extract_currency(
                text
            )
        )

        # ------------------------------------------------------
        # Return Invoice Data
        # ------------------------------------------------------

        return {

            "invoice_number":
                invoice_number,

            "invoice_date":
                invoice_date,

            "due_date":
                due_date,

            "vendor":
                vendor,

            "customer":
                customer,

            "subtotal":
                subtotal,

            "tax":
                tax,

            "total_amount":
                total,

            "currency":
                currency
        }

    # ==========================================================
    # Complete Information Extraction
    # ==========================================================

    @classmethod
    def extract(cls, text):

        entities = (
            cls.extract_entities(
                text
            )
        )

        return {

            "success": True,

            "dates": cls.extract_dates(
                text
            ),

            "names": entities[
                "names"
            ],

            "organizations": entities[
                "organizations"
            ],

            "message": (
                "Information extraction completed."
            )
        }