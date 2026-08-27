"""
===============================================================
Enterprise AI Knowledge Assistant

Information Extraction Component
===============================================================
"""

import streamlit as st

from api_client import (
    extract_information
)


# ==========================================================
# Render Information Extraction
# ==========================================================

def render_extraction():

    # ------------------------------------------------------
    # Page Title
    # ------------------------------------------------------

    st.title(
        "🔎 Information Extraction"
    )

    st.write(
        """
        Extract structured information from text or documents.
        """
    )


    # ------------------------------------------------------
    # Extraction Type
    # ------------------------------------------------------

    extraction_type = st.selectbox(

        "Select Extraction Type",

        [

            "all",

            "dates",

            "entities",

            "invoice"

        ]

    )


    # ------------------------------------------------------
    # Text Input
    # ------------------------------------------------------

    text = st.text_area(

        "Enter Text",

        height=300,

        placeholder="""
Example:

TAX INVOICE

Invoice Number: INV-2026-001

Invoice Date: 12/08/2026

Due Date: 25/08/2026

Vendor: ABC Technologies Pvt Ltd

Customer: XYZ Corporation

Subtotal: ₹10,000.00

GST: ₹1,800.00

Grand Total: ₹11,800.00
        """

    )


    # ------------------------------------------------------
    # Extract Button
    # ------------------------------------------------------

    if st.button(

        "🔍 Extract Information",

        use_container_width=True

    ):

        # --------------------------------------------------
        # Validate Input
        # --------------------------------------------------

        if not text.strip():

            st.warning(
                "Please enter text for extraction."
            )

            return


        # --------------------------------------------------
        # Call Backend API
        # --------------------------------------------------

        try:

            with st.spinner(

                "Extracting information..."

            ):

                result = extract_information(

                    text=text,

                    extraction_type=(
                        extraction_type
                    )

                )


        except Exception as error:

            st.error(

                f"Extraction failed: {error}"

            )

            return


        # --------------------------------------------------
        # Validate API Response
        # --------------------------------------------------

        if not result.get(

            "success",

            False

        ):

            st.error(

                result.get(

                    "error",

                    "Information extraction failed."

                )

            )

            return


        # ==================================================
        # Display Backend Success Message
        # ==================================================

        message = result.get(

            "message"

        )


        if message:

            st.success(
                message
            )

        else:

            st.success(

                "Information extracted successfully."

            )


        # ==================================================
        # DATES
        # ==================================================

        if extraction_type in [

            "all",

            "dates"

        ]:

            st.subheader(

                "📅 Dates"

            )


            dates = result.get(

                "dates",

                []

            )


            if dates:

                for date in dates:

                    st.write(

                        f"• {date}"

                    )

            else:

                st.info(

                    "No dates found."

                )


        # ==================================================
        # ENTITIES
        # ==================================================

        if extraction_type in [

            "all",

            "entities"

        ]:

            # ----------------------------------------------
            # People
            # ----------------------------------------------

            st.subheader(

                "👤 People"

            )


            names = result.get(

                "names",

                []

            )


            if names:

                for name in names:

                    st.write(

                        f"• {name}"

                    )

            else:

                st.info(

                    "No people found."

                )


            # ----------------------------------------------
            # Organizations
            # ----------------------------------------------

            st.subheader(

                "🏢 Organizations"

            )


            organizations = result.get(

                "organizations",

                []

            )


            if organizations:

                for organization in organizations:

                    st.write(

                        f"• {organization}"

                    )

            else:

                st.info(

                    "No organizations found."

                )


        # ==================================================
        # INVOICE
        # ==================================================

        if extraction_type == "invoice":

            st.subheader(

                "🧾 Invoice Information"

            )


            invoice = result.get(

                "invoice",

                {}

            )


            if invoice:

                st.json(

                    invoice

                )

            else:

                st.info(

                    "No invoice information found."

                )