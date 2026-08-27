"""
===============================================================
Enterprise AI Knowledge Assistant

Sidebar Navigation Component
===============================================================
"""

import streamlit as st

from components.auth import (
    logout
)


# ==========================================================
# Render Sidebar
# ==========================================================

def render_sidebar():

    # ======================================================
    # Sidebar Title
    # ======================================================

    st.sidebar.title(
        "Navigation"
    )


    # ======================================================
    # Navigation Menu
    # ======================================================

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

            "Search",

            "Information Extraction",

            "Settings"

        ]

    )


    # ======================================================
    # Divider
    # ======================================================

    st.sidebar.divider()


    # ======================================================
    # User Information
    # ======================================================

    if st.session_state.get(

        "authenticated",

        False

    ):

        # ==================================================
        # Logged-in Status
        # ==================================================

        st.sidebar.success(

            "Logged in"

        )


        # ==================================================
        # Get Current User
        # ==================================================

        current_user = st.session_state.get(

            "current_user"

        )


        # ==================================================
        # Display User Information
        # ==================================================

        if current_user:

            username = current_user.get(

                "username",

                "User"

            )


            email = current_user.get(

                "email",

                ""

            )


            st.sidebar.write(

                f"👤 **{username}**"

            )


            if email:

                st.sidebar.caption(

                    email

                )


        # ==================================================
        # Logout Button
        # ==================================================

        if st.sidebar.button(

            "🚪 Logout",

            use_container_width=True

        ):

            logout()


    # ======================================================
    # Return Selected Page
    # ======================================================

    return page