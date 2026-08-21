import streamlit as st

from api_client import (
    ask_question,
    get_chat_status
)


# ==========================================================
# Render Chat Component
# ==========================================================

def render_chat_page():

    # ======================================================
    # Initialize Session State
    # ======================================================
    # This ensures chat_history always exists before
    # accessing, appending, clearing, or checking it.
    # ======================================================

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    # ======================================================
    # Chat Page Header
    # ======================================================

    st.header("🤖 AI Chat")

    st.markdown(
        "Ask questions about your uploaded documents."
    )

    # ------------------------------------------------------
    # Check Backend Status
    # ------------------------------------------------------

    try:

        status = get_chat_status()

        st.success(
            f"Chat Service : {status['status']} | "
            f"LLM : {status['llm_model']}"
        )

    except Exception as error:

        st.error(
            f"Unable to connect to backend.\n\n{error}"
        )

        return

    st.divider()

    # ------------------------------------------------------
    # Question Input
    # ------------------------------------------------------

    question = st.text_input(

        "Ask your question",

        placeholder="Example : What is OCR?"

    )

    top_k = st.slider(

        "Retrieved Chunks",

        min_value=1,

        max_value=10,

        value=3

    )

    # ------------------------------------------------------
    # Buttons
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        ask_button = st.button(

            "Ask Question",

            use_container_width=True

        )

    with col2:

        clear_button = st.button(

            "Clear Chat",

            use_container_width=True

        )

    # ------------------------------------------------------
    # Clear Chat
    # ------------------------------------------------------

    if clear_button:

        st.session_state.chat_history.clear()

        st.rerun()

    # ------------------------------------------------------
    # Ask Question
    # ------------------------------------------------------

    if ask_button:

        if question.strip() == "":

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(

                "Thinking..."

            ):

                try:

                    result = ask_question(

                        question=question,

                        top_k=top_k

                    )

                    # --------------------------------------
                    # Store conversation in session state
                    # --------------------------------------

                    st.session_state.chat_history.append(

                        result

                    )

                except Exception as error:

                    st.error(
                        f"Error while processing question: "
                        f"{error}"
                    )

    st.divider()

    # ======================================================
    # Conversation History
    # ======================================================

    st.subheader("Conversation")

    if len(st.session_state.chat_history) == 0:

        st.info(
            "No conversation yet."
        )

    else:

        for item in reversed(

            st.session_state.chat_history

        ):

            # --------------------------------------------------
            # User Message
            # --------------------------------------------------

            with st.chat_message(

                "user"

            ):

                st.markdown(

                    item["question"]

                )

            # --------------------------------------------------
            # Assistant Message
            # --------------------------------------------------

            with st.chat_message(

                "assistant"

            ):

                st.markdown(

                    item["answer"]

                )

                st.divider()

                # ----------------------------------------------
                # Sources
                # ----------------------------------------------

                st.markdown(
                    "### 📄 Source Documents"
                )

                sources = item.get(
                    "sources",
                    []
                )

                if len(sources) == 0:

                    st.info(
                        "No relevant source documents found."
                    )

                else:

                    for source in sources:

                        document_name = source.get(
                            "document",
                            "Unknown Document"
                        )

                        page_number = source.get(
                            "page",
                            "Unknown"
                        )

                        with st.expander(

                            f"{document_name} | "
                            f"Page {page_number}"

                        ):

                            st.write(

                                f"Chunk ID : "
                                f"{source.get('chunk_id', 'N/A')}"

                            )

                            # ----------------------------------
                            # Distance
                            # ----------------------------------

                            if (
                                source.get("distance")
                                is not None
                            ):

                                st.write(

                                    f"Distance : "
                                    f"{source['distance']:.4f}"

                                )

                            # ----------------------------------
                            # Optional Chunk Preview
                            # ----------------------------------

                            if "text" in source:

                                st.markdown(

                                    "#### Retrieved Chunk"

                                )

                                st.write(

                                    source["text"]

                                )