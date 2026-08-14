import streamlit as st

from api_client import search_documents


def render_search():

    st.header(
        "🔎 Multi-document Search"
    )

    st.write(
        "Search across all indexed documents."
    )

    # ======================================================
    # Search Input
    # ======================================================

    query = st.text_input(

        "Search Query",

        placeholder=(
            "Example: What is OCR?"
        )

    )

    # ======================================================
    # Top K
    # ======================================================

    top_k = st.slider(

        "Number of Results",

        min_value=1,

        max_value=20,

        value=5

    )

    # ======================================================
    # Search Button
    # ======================================================

    if st.button(
        "🔎 Search",
        use_container_width=True
    ):

        if not query.strip():

            st.warning(
                "Please enter a search query."
            )

            return

        with st.spinner(
            "Searching documents..."
        ):

            try:

                result = search_documents(

                    query=query,

                    top_k=top_k

                )

            except Exception as error:

                st.error(
                    f"Search failed: {error}"
                )

                return

        # ==================================================
        # Search Error
        # ==================================================

        if not result.get(
            "success",
            False
        ):

            st.error(
                result.get(
                    "error",
                    "Search failed."
                )
            )

            return

        # ==================================================
        # No Results
        # ==================================================

        total_results = result.get(
            "total_results",
            0
        )

        if total_results == 0:

            st.warning(
                "No matching documents found."
            )

            return

        # ==================================================
        # Results Summary
        # ==================================================

        st.success(

            f"Found {total_results} "
            f"matching chunks."

        )

        st.divider()

        # ==================================================
        # Display Results
        # ==================================================

        for result_index, item in enumerate(
            result.get(
                "results",
                []
            ),
            start=1
        ):

            # ----------------------------------------------
            # Result information
            # ----------------------------------------------

            rank = item.get(
                "rank",
                result_index
            )

            document = item.get(
                "document",
                "Unknown"
            )

            page = item.get(
                "page",
                1
            )

            distance = float(
                item.get(
                    "distance",
                    0
                )
            )

            citation = item.get(
                "citation",
                ""
            )

            # ----------------------------------------------
            # Result expander
            # ----------------------------------------------

            with st.expander(

                f"#{rank} | "
                f"{document} | "
                f"Page {page}"

            ):

                # ------------------------------------------
                # Citation
                # ------------------------------------------

                st.markdown(
                    "### 📌 Citation"
                )

                st.code(
                    citation
                )

                # ------------------------------------------
                # Metadata
                # ------------------------------------------

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"**Document:** {document}"
                    )

                with col2:

                    st.write(
                        f"**Page:** {page}"
                    )

                with col3:

                    st.write(
                        f"**Distance:** "
                        f"{distance:.4f}"
                    )

                # ------------------------------------------
                # Chunk
                # ------------------------------------------

                st.markdown(
                    "### 📄 Retrieved Chunk"
                )

                st.write(
                    item.get(
                        "text",
                        ""
                    )
                )