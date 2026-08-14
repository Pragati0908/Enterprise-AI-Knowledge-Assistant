import streamlit as st


def render_sidebar():

    st.sidebar.title(
        "Navigation"
    )

    page = st.sidebar.radio(

        "Select Page",

        [

            "Home",

            "Upload Documents",

            "OCR",

            "Chunk Viewer",

            "Documents",

            "Embedding Status",

            "Create Embedding",

            "Similarity Search",

            "Chat",

            # ==================================================
            # DAY 39 — MULTI-DOCUMENT SEARCH
            # ==================================================

            "Search",

            "Settings"

        ]

    )

    return page