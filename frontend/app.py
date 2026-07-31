import streamlit as st

from components.sidebar import render_sidebar

from api_client import (
    get_health,
    upload_file,
    get_documents,
    extract_ocr,
    generate_chunks,
    get_embedding_status,
    create_document_embeddings,
    search_embeddings
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
# EMBEDDING STATUS
# ======================================================
elif page == "Embedding Status":
    st.header("🧠 Embedding Service Status")
    if st.button("Check Status"):
        st.json(get_embedding_status())

# ======================================================
# CREATE EMBEDDING
# ======================================================
# ======================================================
# INDEX DOCUMENT
# ======================================================

elif page == "Create Embedding":

    st.header("🧠 Index Uploaded Document")

    st.info(
        "Index a document that has already been uploaded using the Upload Documents page."
    )

    filename = st.text_input(

        "Document Name",

        placeholder="sample_chunk_testing.pdf"

    )

    if st.button(

        "Create Embeddings"

    ):

        if filename.strip() == "":

            st.warning(

                "Please enter the uploaded document name."

            )

        else:

            with st.spinner(

                "Creating embeddings..."

            ):

                result = create_document_embeddings(

                    filename

                )

            if "detail" in result:

                st.error(

                    result["detail"]

                )

            else:

                st.success(

                    result["message"]

                )

                st.write(

                    f"Document : {result['document']}"

                )

                st.write(

                    f"Chunks : {result['total_chunks']}"

                )

                st.write(

                    f"Embedding Dimension : {result['embedding_dimension']}"

                )

                st.write(

                    f"Total Stored Vectors : {result['total_vectors']}"

                )

# ======================================================
# SIMILARITY SEARCH
# ======================================================

elif page == "Similarity Search":

    st.header("🔎 Similarity Search")

    st.info(

        "Search semantically similar chunks from indexed documents."

    )

    query = st.text_input(

        "Enter Search Query",

        placeholder="Machine Learning"

    )

    top_k = st.slider(

        "Top K Results",

        min_value=1,

        max_value=10,

        value=5

    )

    if st.button(

        "Search"

    ):

        if query.strip() == "":

            st.warning(

                "Please enter a query."

            )

        else:

            with st.spinner(

                "Searching FAISS Vector Database..."

            ):

                results = search_embeddings(

                    query,

                    top_k

                )

            if "detail" in results:

                st.error(

                    results["detail"]

                )

            elif results["total_results"] == 0:

                st.warning(

                    "No matching chunks found."

                )

            else:

                st.success(

                    f"Found {results['total_results']} matching chunks."

                )

                st.subheader(

                    "Search Results"

                )

                for item in results["results"]:

                    with st.expander(

                        f"📄 Chunk {item['chunk_id']}"

                    ):

                        col1, col2 = st.columns(2)

                        with col1:

                            st.write(

                                f"**Document:** {item['document']}"

                            )

                            st.write(

                                f"**Page:** {item['page']}"

                            )

                            st.write(

                                f"**Source:** {item['source']}"

                            )

                            st.write(

                                f"**Chunk ID:** {item['chunk_id']}"

                            )

                        with col2:

                            st.write(

                                f"**Characters:** {item['chunk_length']}"

                            )

                            st.write(

                                f"**Start Index:** {item['start_index']}"

                            )

                            st.write(

                                f"**End Index:** {item['end_index']}"

                            )

                            st.write(

                                f"**Distance:** {item['distance']:.4f}"

                            )

                        st.text_area(

                            "Chunk Text",

                            item["text"],

                            height=220,

                            key=f"search_chunk_{item['chunk_id']}"

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

        "System configuration will be added now."

    )