import streamlit as st

from api_client import (
    ask_question,
    get_chat_status
)


# ==========================================================
# Initialize Session State
# ==========================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# ==========================================================
# Render Chat Component
# ==========================================================

def render_chat_page():

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

                    st.session_state.chat_history.append(

                        result

                    )

                except Exception as error:

                    st.error(error)

    st.divider()

    # ======================================================
    # Conversation History
    # ======================================================

    st.subheader("Conversation")

    if len(st.session_state.chat_history) == 0:

        st.info(
            "No conversation yet."
        )

    for item in reversed(

        st.session_state.chat_history

    ):

        # --------------------------------------------------
        # User
        # --------------------------------------------------

        with st.chat_message(

            "user"

        ):

            st.markdown(

                item["question"]

            )

        # --------------------------------------------------
        # Assistant
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

            if len(item["sources"]) == 0:

                st.info(
                    "No relevant source documents found."
                )

            else:

                for source in item["sources"]:

                    with st.expander(

                        f"{source['document']} | "
                        f"Page {source['page']}"

                    ):

                        st.write(

                            f"Chunk ID : "
                            f"{source['chunk_id']}"

                        )

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