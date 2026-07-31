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

            "Settings"

        ]

    )

    return page