import streamlit as st

from components.sidebar import render_sidebar

from api_client import (
    get_health,
    upload_file,
    get_documents,
    extract_ocr,
    generate_chunks
)


st.set_page_config(
    page_title="Enterprise AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)


def load_css():

    try:

        with open(

            "assets/styles.css"

        ) as f:

            st.markdown(

                f"<style>{f.read()}</style>",

                unsafe_allow_html=True

            )

    except FileNotFoundError:

        pass


load_css()


page = render_sidebar()


st.title("🤖 Enterprise AI Knowledge Assistant")

st.subheader(page)


# ======================================================
# HOME
# ======================================================

if page == "Home":

    st.write("Dashboard")

    try:

        health = get_health()

        st.success(

            "Backend connected successfully."

        )

        st.json(

            health

        )

    except Exception:

        st.error(

            "Cannot connect to FastAPI backend."

        )


# ======================================================
# UPLOAD DOCUMENTS
# ======================================================

elif page == "Upload Documents":

    st.header("📂 Upload Documents")

    uploaded_file = st.file_uploader(

        "Choose a document",

        type=[

            "pdf",

            "docx",

            "pptx",

            "xlsx"

        ],

        key="upload"

    )

    if uploaded_file:

        st.write(

            f"Selected File : {uploaded_file.name}"

        )

        if st.button(

            "Upload File"

        ):

            result = upload_file(

                uploaded_file

            )

            st.success(

                "File uploaded successfully."

            )

            st.json(

                result

            )


# ======================================================
# OCR
# ======================================================

elif page == "OCR":

    st.header("📝 OCR Text Extraction")

    uploaded_file = st.file_uploader(

        "Upload scanned PDF or Image",

        type=[

            "pdf",

            "png",

            "jpg",

            "jpeg"

        ],

        key="ocr"

    )

    if uploaded_file:

        st.write(

            f"Selected File : {uploaded_file.name}"

        )

        if st.button(

            "Extract Text"

        ):

            with st.spinner(

                "Running OCR..."

            ):

                result = extract_ocr(

                    uploaded_file

                )

            st.success(

                "OCR Completed Successfully"

            )

            st.text_area(

                "Extracted Text",

                result["text"],

                height=350

            )


# ======================================================
# CHUNK VIEWER
# ======================================================

elif page == "Chunk Viewer":

    st.header("📑 Chunk Viewer")

    uploaded_file = st.file_uploader(

        "Upload document",

        type=[

            "pdf",

            "png",

            "jpg",

            "jpeg"

        ],

        key="chunk"

    )

    if uploaded_file:

        st.write(

            f"Selected File : {uploaded_file.name}"

        )

        if st.button(

            "Generate Chunks"

        ):

            with st.spinner(

                "Generating Chunks..."

            ):

                result = generate_chunks(

                    uploaded_file

                )

            st.success(

                f"Generated {result['total_chunks']} chunks"

            )

            for chunk in result["chunks"]:

                with st.expander(

                    f"Chunk {chunk['chunk_id']}"

                ):

                    st.write(

                        f"Source : {chunk['source']}"

                    )

                    st.write(

                        f"Start : {chunk['start_index']}"

                    )

                    st.write(

                        f"End : {chunk['end_index']}"

                    )

                    st.write(

                        f"Length : {chunk['chunk_length']}"

                    )

                    st.text_area(

                        "Text",

                        chunk["text"],

                        height=180,

                        key=f"chunk_{chunk['chunk_id']}"

                    )


# ======================================================
# DOCUMENTS
# ======================================================

elif page == "Documents":

    st.header("📚 Uploaded Documents")

    try:

        documents = get_documents()

        st.json(

            documents

        )

    except Exception:

        st.error(

            "Unable to fetch document list."

        )


# ======================================================
# CHAT
# ======================================================

elif page == "Chat":

    st.header("💬 AI Chat")

    st.info(

        "RAG Chat Interface will be implemented here."

    )


# ======================================================
# SETTINGS
# ======================================================

elif page == "Settings":

    st.header("⚙ Settings")

    st.write(

        "System configuration will be added in Week 7."

    )