import streamlit as st

from components.sidebar import render_sidebar
from components.chat import render_chat_page
from components.search import render_search
from components.extraction import render_extraction

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


# ==========================================================
# Streamlit Configuration
# ==========================================================

st.set_page_config(
    page_title="Enterprise AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)


# ==========================================================
# Load Custom CSS
# ==========================================================

def load_css():

    try:

        with open(
            "assets/styles.css",
            encoding="utf-8"
        ) as css_file:

            st.markdown(
                f"<style>{css_file.read()}</style>",
                unsafe_allow_html=True
            )

    except FileNotFoundError:

        pass


load_css()


# ==========================================================
# Sidebar Navigation
# ==========================================================

page = render_sidebar()


# ==========================================================
# Page Header
# ==========================================================

st.title(
    "🤖 Enterprise AI Knowledge Assistant"
)

st.subheader(
    page
)


# ==========================================================
# HOME
# ==========================================================

if page == "Home":

    st.write(
        "### Dashboard"
    )

    try:

        health = get_health()

        st.success(
            "Backend connected successfully."
        )

        st.json(
            health
        )

    except Exception as error:

        st.error(
            "Cannot connect to FastAPI backend."
        )

        st.exception(
            error
        )


# ==========================================================
# UPLOAD DOCUMENTS
# ==========================================================

elif page == "Upload Documents":

    st.header(
        "📂 Upload Documents"
    )

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

            with st.spinner(
                "Uploading document..."
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


# ==========================================================
# OCR
# ==========================================================

elif page == "OCR":

    st.header(
        "📝 OCR Text Extraction"
    )

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

                height=350,

                key="ocr_extracted_text"

            )


# ==========================================================
# CHUNK VIEWER
# ==========================================================

elif page == "Chunk Viewer":

    st.header(
        "📑 Chunk Viewer"
    )

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

            for chunk_index, chunk in enumerate(

                result["chunks"]

            ):

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

                    chunk_key = (

                        f"chunk_"
                        f"{chunk_index}_"
                        f"{chunk['chunk_id']}"

                    )

                    st.text_area(

                        "Chunk Text",

                        chunk["text"],

                        height=180,

                        key=chunk_key

                    )


# ==========================================================
# DOCUMENTS
# ==========================================================

elif page == "Documents":

    st.header(
        "📚 Uploaded Documents"
    )

    try:

        documents = get_documents()

        st.success(
            f"Retrieved {len(documents)} documents."
        )

        st.json(
            documents
        )

    except Exception as error:

        st.error(
            "Unable to fetch document list."
        )

        st.exception(
            error
        )


# ==========================================================
# EMBEDDING STATUS
# ==========================================================

elif page == "Embedding Status":

    st.header(
        "🧠 Embedding Service Status"
    )

    if st.button(
        "Check Status"
    ):

        try:

            result = get_embedding_status()

            st.success(
                "Embedding service is available."
            )

            st.json(
                result
            )

        except Exception as error:

            st.error(
                "Unable to fetch embedding status."
            )

            st.exception(
                error
            )


# ==========================================================
# CREATE EMBEDDING
# ==========================================================

elif page == "Create Embedding":

    st.header(
        "🧠 Index Uploaded Document"
    )

    st.info(
        "Index a document that has already been uploaded."
    )

    filename = st.text_input(

        "Document Name",

        placeholder="sample_chunk_testing.pdf",

        key="embedding_filename"

    )

    if st.button(

        "Create Embeddings",

        key="create_embeddings_button"

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

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Chunks",
                        result["total_chunks"]
                    )

                    st.metric(
                        "Embedding Dimension",
                        result["embedding_dimension"]
                    )

                with col2:

                    st.metric(
                        "Stored Vectors",
                        result["total_vectors"]
                    )

                    st.write(
                        f"**Document:** "
                        f"{result['document']}"
                    )


# ==========================================================
# SIMILARITY SEARCH
# ==========================================================

elif page == "Similarity Search":

    st.header(
        "🔎 Similarity Search"
    )

    st.info(
        "Search semantically similar chunks "
        "from all indexed documents."
    )

    query = st.text_input(

        "Enter Search Query",

        placeholder="Machine Learning",

        key="similarity_query"

    )

    top_k = st.slider(

        "Top K Results",

        min_value=1,

        max_value=10,

        value=5,

        key="similarity_top_k"

    )

    if st.button(

        "Search",

        key="similarity_search_button"

    ):

        if query.strip() == "":

            st.warning(
                "Please enter a query."
            )

        else:

            with st.spinner(
                "Searching FAISS Vector Database..."
            ):

                try:

                    results = search_embeddings(
                        query,
                        top_k
                    )

                except Exception as error:

                    st.error(
                        "Similarity search failed."
                    )

                    st.exception(
                        error
                    )

                    results = None

            if results is not None:

                # ==================================================
                # ERROR RESPONSE
                # ==================================================

                if "detail" in results:

                    st.error(
                        results["detail"]
                    )

                # ==================================================
                # NO RESULTS
                # ==================================================

                elif results.get(
                    "total_results",
                    0
                ) == 0:

                    st.warning(
                        "No matching chunks found."
                    )

                # ==================================================
                # RESULTS FOUND
                # ==================================================

                else:

                    search_results = (
                        results["results"]
                    )

                    total_results = len(
                        search_results
                    )

                    unique_documents = set()

                    for item in search_results:

                        document_name = item.get(
                            "document"
                        )

                        if document_name:

                            unique_documents.add(
                                document_name
                            )

                    documents_found = len(
                        unique_documents
                    )

                    # ----------------------------------------------
                    # Search Summary
                    # ----------------------------------------------

                    st.success(
                        "Similarity search completed successfully."
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Total Results",
                            total_results
                        )

                    with col2:

                        st.metric(
                            "Documents Found",
                            documents_found
                        )

                    # ----------------------------------------------
                    # Document List
                    # ----------------------------------------------

                    st.subheader(
                        "📚 Documents Retrieved"
                    )

                    for document in sorted(
                        unique_documents
                    ):

                        st.write(
                            f"📄 {document}"
                        )

                    # ----------------------------------------------
                    # Search Results
                    # ----------------------------------------------

                    st.subheader(
                        "🔎 Search Results"
                    )

                    for result_index, item in enumerate(

                        search_results,

                        start=1

                    ):

                        document = item.get(

                            "document",

                            "Unknown"

                        )

                        chunk_id = item.get(

                            "chunk_id",

                            "Unknown"

                        )

                        with st.expander(

                            f"📄 {document} | "
                            f"Chunk {chunk_id}",

                            expanded=False

                        ):

                            col1, col2 = st.columns(2)

                            with col1:

                                st.write(
                                    f"**Document:** {document}"
                                )

                                st.write(
                                    f"**Page:** "
                                    f"{item.get('page', 1)}"
                                )

                                st.write(
                                    f"**Source:** "
                                    f"{item.get('source', document)}"
                                )

                                st.write(
                                    f"**Chunk ID:** "
                                    f"{chunk_id}"
                                )

                            with col2:

                                st.write(
                                    f"**Characters:** "
                                    f"{item.get('chunk_length', 0)}"
                                )

                                st.write(
                                    f"**Start Index:** "
                                    f"{item.get('start_index', 0)}"
                                )

                                st.write(
                                    f"**End Index:** "
                                    f"{item.get('end_index', 0)}"
                                )

                                distance = float(

                                    item.get(
                                        "distance",
                                        0
                                    )

                                )

                                st.write(
                                    f"**Distance:** "
                                    f"{distance:.4f}"
                                )

                            # ------------------------------------------
                            # Citation
                            # ------------------------------------------

                            citation = item.get(
                                "citation"
                            )

                            if citation:

                                st.markdown(
                                    "### 📌 Citation"
                                )

                                st.info(
                                    citation
                                )

                            else:

                                st.warning(
                                    "Citation information "
                                    "is not available."
                                )

                            # ------------------------------------------
                            # Citation Details
                            # ------------------------------------------

                            citation_document = item.get(
                                "citation_document"
                            )

                            citation_page = item.get(
                                "citation_page"
                            )

                            citation_chunk = item.get(
                                "citation_chunk"
                            )

                            if (
                                citation_document
                                is not None
                            ):

                                with st.expander(
                                    "Citation Details"
                                ):

                                    st.write(
                                        f"**Document:** "
                                        f"{citation_document}"
                                    )

                                    st.write(
                                        f"**Page:** "
                                        f"{citation_page}"
                                    )

                                    st.write(
                                        f"**Chunk:** "
                                        f"{citation_chunk}"
                                    )

                            # ------------------------------------------
                            # Similarity Indicator
                            # ------------------------------------------

                            similarity_score = max(

                                0.0,

                                min(

                                    1.0,

                                    1 - (
                                        distance / 2
                                    )

                                )

                            )

                            st.progress(
                                similarity_score
                            )

                            st.caption(
                                f"Similarity indicator: "
                                f"{similarity_score:.4f}"
                            )

                            # ------------------------------------------
                            # Chunk Text
                            # ------------------------------------------

                            st.text_area(

                                "Chunk Text",

                                item.get(
                                    "text",
                                    ""
                                ),

                                height=220,

                                key=(

                                    f"search_chunk_"
                                    f"{result_index}_"
                                    f"{chunk_id}_"
                                    f"{document}"

                                )

                            )


# ==========================================================
# AI CHAT
# ==========================================================

elif page == "Chat":

    render_chat_page()


# ==========================================================
# INFORMATION EXTRACTION
# ==========================================================

elif page == "Information Extraction":

    render_extraction()


# ==========================================================
# MULTI-DOCUMENT SEARCH
# ==========================================================

elif page == "Search":

    render_search()


# ==========================================================
# SETTINGS
# ==========================================================

elif page == "Settings":

    st.header(
        "⚙️ Settings"
    )

    st.info(
        "Application configuration and diagnostics."
    )

    # ======================================================
    # Backend Status
    # ======================================================

    st.subheader(
        "Backend Status"
    )

    try:

        health = get_health()

        st.success(
            "Backend is online."
        )

        st.json(
            health
        )

    except Exception as error:

        st.error(
            "Unable to connect to backend."
        )

        st.exception(
            error
        )

    st.divider()

    # ======================================================
    # Embedding Service
    # ======================================================

    st.subheader(
        "Embedding Service"
    )

    try:

        embedding_status = get_embedding_status()

        st.json(
            embedding_status
        )

    except Exception:

        st.warning(
            "Embedding service status unavailable."
        )

    st.divider()

    # ======================================================
    # Application Information
    # ======================================================

    st.subheader(
        "Application Information"
    )

    st.markdown("""

**Enterprise AI Knowledge Assistant**

### Current Modules

- ✅ Document Upload
- ✅ OCR
- ✅ Chunk Viewer
- ✅ Embedding Generation
- ✅ Similarity Search
- ✅ RAG Chat
- ✅ Citation Generation
- ✅ Source Tracking
- ✅ Multi-document Search
- ✅ Information Extraction

### Backend

- FastAPI
- FAISS
- Ollama
- Streamlit

""")


# ==========================================================
# UNKNOWN PAGE FALLBACK
# ==========================================================

else:

    st.error(
        f"Unknown page selected: {page}"
    )