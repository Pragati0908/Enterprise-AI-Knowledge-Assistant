"""
==========================================================
Enterprise AI Knowledge Assistant

Embedding API

Responsibilities
----------------
• Generate document embeddings
• Add embeddings to persistent FAISS index
• Add corresponding metadata
• Preserve previously indexed documents
• Perform semantic similarity search
• Maintain FAISS ↔ Metadata alignment
• Generate citations for search results

Multiple documents are stored in the SAME FAISS index.

Example:

    Document A
        ↓
        12 chunks
        ↓
    FAISS vectors 0-11

    Document B
        ↓
        15 chunks
        ↓
    FAISS vectors 12-26

    Total:
        27 vectors

Metadata follows exactly the same vector order.
==========================================================
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.metadata_store import MetadataStore
from app.services.citation_service import CitationService

from app.services.parsers.document_parser import DocumentParser
from app.services.text_cleaner import TextCleaner
from app.services.chunker import TextChunker


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/embeddings",
    tags=["Embeddings"]
)


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = (
    Path(__file__).resolve().parents[4]
)

UPLOAD_DIR = (
    PROJECT_ROOT
    / "backend"
    / "uploads"
)

VECTOR_DB = (
    PROJECT_ROOT
    / "backend"
    / "vector_db"
)

VECTOR_DB.mkdir(
    parents=True,
    exist_ok=True
)

FAISS_PATH = (
    VECTOR_DB
    / "faiss.index"
)


# ==========================================================
# Request Models
# ==========================================================

class IndexRequest(BaseModel):

    filename: str


class SearchRequest(BaseModel):

    query: str

    top_k: int = 5


# ==========================================================
# Persistent Stores
# ==========================================================

vector_store = None

metadata_store = MetadataStore()


# ==========================================================
# Load Existing Database
# ==========================================================

try:

    # ------------------------------------------------------
    # Determine embedding dimension
    # ------------------------------------------------------

    test_embedding = (
        EmbeddingService.generate_embedding(
            "test"
        )
    )

    dimension = len(
        test_embedding
    )

    # ------------------------------------------------------
    # Create VectorStore
    # ------------------------------------------------------

    vector_store = VectorStore(
        dimension
    )

    # ------------------------------------------------------
    # Load existing FAISS index
    # ------------------------------------------------------

    if FAISS_PATH.exists():

        vector_store.load()

    else:

        print(
            "\nNo existing FAISS index found."
        )

        print(
            "A new index will be created "
            "when the first document is indexed.\n"
        )

    # MetadataStore automatically loads
    # existing metadata.

    print(
        "\nExisting Vector Database Status"
    )

    print(
        f"Vectors  : "
        f"{vector_store.total_vectors()}"
    )

    print(
        f"Metadata : "
        f"{metadata_store.total()}"
    )

    print()

    # ------------------------------------------------------
    # Validate FAISS ↔ Metadata alignment
    # ------------------------------------------------------

    if (
        vector_store.total_vectors()
        != metadata_store.total()
    ):

        print(
            "\nWARNING:"
        )

        print(
            "FAISS vector count and metadata "
            "record count do not match."
        )

        print(
            f"FAISS vectors : "
            f"{vector_store.total_vectors()}"
        )

        print(
            f"Metadata      : "
            f"{metadata_store.total()}"
        )

        print()


except Exception as error:

    print(
        "\nUnable to initialize vector database."
    )

    print(
        f"Reason : {error}"
    )

    print(
        "A new database will be created "
        "when indexing begins.\n"
    )

    vector_store = None


# ==========================================================
# Embedding Status
# ==========================================================

@router.get("/status")
def embedding_status():

    """
    Return current embedding/vector database status.
    """

    return {

        "status":
            "running",

        "service":
            "Embedding API",

        "vector_database":

            "initialized"

            if (
                vector_store
                and
                vector_store.total_vectors() > 0
            )

            else "empty",

        "total_vectors":

            vector_store.total_vectors()

            if vector_store

            else 0,

        "total_metadata":

            metadata_store.total()

    }


# ==========================================================
# Create Embeddings
# ==========================================================

@router.post("/create")
def create_embeddings(
    request: IndexRequest
):

    """
    Create embeddings for one uploaded document
    and APPEND them to the existing FAISS index.

    Existing documents remain indexed.
    """

    global vector_store

    # ======================================================
    # Step 1
    # Locate Uploaded Document
    # ======================================================

    supported_extensions = [

        "pdf",
        "docx",
        "pptx",
        "xlsx"

    ]

    file_path = None

    for extension in supported_extensions:

        candidate = (

            UPLOAD_DIR
            / extension
            / request.filename

        )

        if candidate.exists():

            file_path = candidate

            break

    if file_path is None:

        raise HTTPException(

            status_code=404,

            detail=(
                "Document not found : "
                f"{request.filename}"
            )

        )

    # ======================================================
    # Step 2
    # Extract Text
    # ======================================================

    try:

        text = (
            DocumentParser.parse_document(
                str(file_path)
            )
        )

    except ValueError as error:

        raise HTTPException(

            status_code=400,

            detail=str(error)

        )

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(
                "Document parsing failed : "
                f"{error}"
            )

        )

    # ======================================================
    # Step 3
    # Clean Text
    # ======================================================

    cleaned_text = (
        TextCleaner.clean_text(
            text
        )
    )

    if not cleaned_text.strip():

        raise HTTPException(

            status_code=400,

            detail=(
                "Document contains no usable text."
            )

        )

    # ======================================================
    # Step 4
    # Chunk Text
    # ======================================================

    chunks = (
        TextChunker.chunk_text(

            text=cleaned_text,

            source=request.filename,

            chunk_size=800,

            overlap=150

        )
    )

    if not chunks:

        raise HTTPException(

            status_code=400,

            detail="No chunks generated."

        )

    # ======================================================
    # Step 5
    # Generate Embeddings
    # ======================================================

    chunk_texts = [

        chunk["text"]

        for chunk in chunks

    ]

    try:

        embeddings = (
            EmbeddingService.generate_embeddings(
                chunk_texts
            )
        )

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(
                "Embedding generation failed : "
                f"{error}"
            )

        )

    # IMPORTANT:
    # Do NOT use:
    #
    #     if not embeddings:
    #
    # because embeddings may be a NumPy array.
    #
    # Use len() instead.

    if (
        embeddings is None
        or len(embeddings) == 0
    ):

        raise HTTPException(

            status_code=400,

            detail="No embeddings generated."

        )

    # ======================================================
    # Step 6
    # Initialize VectorStore
    # ======================================================

    embedding_dimension = len(
        embeddings[0]
    )

    if vector_store is None:

        vector_store = VectorStore(
            embedding_dimension
        )

        if FAISS_PATH.exists():

            vector_store.load()

    # ======================================================
    # Verify Embedding Dimension
    # ======================================================

    if (
        vector_store.dimension
        != embedding_dimension
    ):

        raise HTTPException(

            status_code=500,

            detail=(

                "Embedding dimension mismatch. "

                f"FAISS dimension = "
                f"{vector_store.dimension}, "

                f"embedding dimension = "
                f"{embedding_dimension}"

            )

        )

    # ======================================================
    # Step 7
    # Determine Starting Vector ID
    # ======================================================

    starting_vector_id = (
        vector_store.total_vectors()
    )

    print(
        "\n=================================================="
    )

    print(
        "ADDING DOCUMENT TO EXISTING VECTOR DATABASE"
    )

    print(
        "=================================================="
    )

    print(
        f"Document         : "
        f"{request.filename}"
    )

    print(
        f"Existing vectors : "
        f"{starting_vector_id}"
    )

    print(
        f"New chunks       : "
        f"{len(chunks)}"
    )

    # ======================================================
    # Step 8
    # Add Embeddings to FAISS
    # ======================================================

    vector_store.add_embeddings(
        embeddings
    )

    # ======================================================
    # Step 9
    # Create Metadata
    # ======================================================

    metadata = []

    for offset, chunk in enumerate(
        chunks
    ):

        vector_id = (
            starting_vector_id
            + offset
        )

        metadata.append(

            {

                "vector_id":
                    vector_id,

                "chunk_id":
                    chunk.get(
                        "chunk_id",
                        offset + 1
                    ),

                "document":
                    request.filename,

                "page":
                    chunk.get(
                        "page",
                        1
                    ),

                "source":
                    request.filename,

                "start_index":
                    chunk["start_index"],

                "end_index":
                    chunk["end_index"],

                "chunk_length":
                    chunk["chunk_length"],

                "text":
                    chunk["text"]

            }

        )

    # ======================================================
    # Step 10
    # Append Metadata
    # ======================================================

    metadata_store.add_many(
        metadata
    )

    # ======================================================
    # Step 11
    # Validate Alignment
    # ======================================================

    faiss_count = (
        vector_store.total_vectors()
    )

    metadata_count = (
        metadata_store.total()
    )

    if faiss_count != metadata_count:

        raise HTTPException(

            status_code=500,

            detail=(

                "FAISS and metadata count mismatch. "

                f"FAISS = {faiss_count}, "

                f"Metadata = {metadata_count}"

            )

        )

    # ======================================================
    # Step 12
    # Save FAISS Index
    # ======================================================

    vector_store.save()

    # ======================================================
    # Step 13
    # Save Metadata
    # ======================================================

    metadata_store.save()

    # ======================================================
    # Final Logging
    # ======================================================

    print(
        "\n=================================================="
    )

    print(
        "DOCUMENT INDEXED SUCCESSFULLY"
    )

    print(
        "=================================================="
    )

    print(
        f"Document           : "
        f"{request.filename}"
    )

    print(
        f"New chunks         : "
        f"{len(chunks)}"
    )

    print(
        f"Embedding dimension: "
        f"{embedding_dimension}"
    )

    print(
        f"Total vectors      : "
        f"{faiss_count}"
    )

    print(
        f"Total metadata     : "
        f"{metadata_count}"
    )

    print(
        "==================================================\n"
    )

    return {

        "message":
            "Document indexed successfully.",

        "document":
            request.filename,

        "total_chunks":
            len(chunks),

        "embedding_dimension":
            embedding_dimension,

        "new_vectors":
            len(chunks),

        "previous_vectors":
            starting_vector_id,

        "total_vectors":
            faiss_count,

        "total_metadata":
            metadata_count

    }


# ==========================================================
# Similarity Search
# ==========================================================

@router.post("/search")
def search_embeddings(
    request: SearchRequest
):

    """
    Search all indexed documents using FAISS.

    Flow:

        Query
          ↓
        Query Embedding
          ↓
        FAISS Search
          ↓
        Vector ID
          ↓
        MetadataStore
          ↓
        CitationService
          ↓
        Search Result + Citation
    """

    global vector_store

    # ======================================================
    # Step 1
    # Validate Vector Database
    # ======================================================

    if (
        vector_store is None
        or
        vector_store.total_vectors() == 0
    ):

        raise HTTPException(

            status_code=400,

            detail="Vector database is empty."

        )

    # ======================================================
    # Step 2
    # Validate FAISS ↔ Metadata Alignment
    # ======================================================

    if (
        metadata_store.total()
        != vector_store.total_vectors()
    ):

        raise HTTPException(

            status_code=500,

            detail=(

                "FAISS and metadata are out of sync. "

                f"FAISS = "
                f"{vector_store.total_vectors()}, "

                f"Metadata = "
                f"{metadata_store.total()}"

            )

        )

    # ======================================================
    # Step 3
    # Generate Query Embedding
    # ======================================================

    try:

        query_embedding = (
            EmbeddingService.generate_embedding(
                request.query
            )
        )

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(

                "Query embedding generation failed : "
                f"{error}"

            )

        )

    # ======================================================
    # Step 4
    # Search FAISS
    # ======================================================

    try:

        results = vector_store.search(

            query_embedding,

            request.top_k

        )

    except Exception as error:

        raise HTTPException(

            status_code=500,

            detail=(

                "FAISS similarity search failed : "
                f"{error}"

            )

        )

    # ======================================================
    # Step 5
    # Convert FAISS Result → Metadata
    # ======================================================

    output = []

    for result in results:

        # --------------------------------------------------
        # FAISS gives us vector_id
        # --------------------------------------------------

        vector_id = (
            result["vector_id"]
        )

        # --------------------------------------------------
        # Retrieve corresponding metadata
        # --------------------------------------------------

        metadata = (
            metadata_store.get(
                vector_id
            )
        )

        if metadata is None:

            continue

        # ==================================================
        # IMPORTANT
        # Build ONE combined result.
        #
        # CitationService receives the SAME information
        # that came from FAISS + MetadataStore.
        # ==================================================

        result_with_metadata = {

            "vector_id":
                vector_id,

            "chunk_id":
                metadata.get(
                    "chunk_id",
                    "Unknown"
                ),

            "document":
                metadata.get(
                    "document",
                    "Unknown document"
                ),

            "page":
                metadata.get(
                    "page",
                    1
                ),

            "source":
                metadata.get(
                    "source",
                    ""
                ),

            "start_index":
                metadata.get(
                    "start_index",
                    0
                ),

            "end_index":
                metadata.get(
                    "end_index",
                    0
                ),

            "chunk_length":
                metadata.get(
                    "chunk_length",
                    0
                ),

            "distance":
                round(
                    result["distance"],
                    4
                ),

            "text":
                metadata.get(
                    "text",
                    ""
                )

        }

        # ==================================================
        # STEP 5 / CITATION GENERATION
        # ==================================================

        citation = (
            CitationService.create_citation(
                result_with_metadata
            )
        )

        # ==================================================
        # Add Citation to Search Result
        # ==================================================

        result_with_metadata["citation"] = (
            citation["citation"]
        )

        # Optional structured citation fields
        # are also returned so the frontend can
        # use them independently if required.

        result_with_metadata["citation_document"] = (
            citation["document"]
        )

        result_with_metadata["citation_page"] = (
            citation["page"]
        )

        result_with_metadata["citation_chunk"] = (
            citation["chunk_id"]
        )

        # --------------------------------------------------
        # Add final result
        # --------------------------------------------------

        output.append(
            result_with_metadata
        )

    # ======================================================
    # Step 6
    # Calculate Documents Found
    # ======================================================

    documents_found = len(

        set(

            item["document"]

            for item in output

        )

    )

    # ======================================================
    # Return Search Results
    # ======================================================

    return {

        "query":
            request.query,

        "top_k":
            request.top_k,

        "total_results":
            len(output),

        "documents_found":
            documents_found,

        "results":
            output

    }