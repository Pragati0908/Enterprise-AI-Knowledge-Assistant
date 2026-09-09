"""
===============================================================
Enterprise AI Knowledge Assistant

Embedding API
===============================================================

Responsibilities
----------------
1. Generate document embeddings
2. Store embeddings in FAISS
3. Store corresponding metadata
4. Search the vector database
5. Maintain FAISS/metadata alignment
6. Prevent indexing when the vector database is inconsistent

Important
---------
FAISS vector IDs are positional and must correspond to metadata
records at the same positions.

Therefore:

    FAISS vector count == metadata record count

must always be true before a new document is indexed.
===============================================================
"""

from pathlib import Path
from typing import Any

import numpy as np

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.core.config import settings

from app.db.database import get_db

from app.services.embedding_service import (
    EmbeddingService,
)

from app.services.vector_store import (
    VectorStore,
)

from app.services.metadata_store import (
    MetadataStore,
)

from app.services.document_processing_service import (
    process_document_file,
)


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/embeddings",
    tags=["Embeddings"],
)


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[4]
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

FAISS_PATH = (
    VECTOR_DB
    / "faiss.index"
)

METADATA_PATH = (
    VECTOR_DB
    / "metadata.json"
)


# ==========================================================
# Metadata Store
# ==========================================================

metadata_store = MetadataStore()


# ==========================================================
# Determine Embedding Dimension
# ==========================================================

try:

    test_embedding = (
        EmbeddingService
        .generate_embedding(
            "test"
        )
    )

    dimension = len(
        test_embedding
    )

except Exception as error:

    raise RuntimeError(
        "Unable to initialize embedding model. "
        f"Error: {error}"
    )


# ==========================================================
# Vector Store
# ==========================================================

vector_store = VectorStore(
    dimension=dimension
)


# ==========================================================
# Initial Vector Database Status
# ==========================================================

try:

    vectors = (
        vector_store
        .total_vectors()
    )

except Exception:

    vectors = 0


metadata_count = len(
    metadata_store.metadata
)


print()
print("=" * 70)
print("EXISTING VECTOR DATABASE STATUS")
print("=" * 70)

print(
    f"Vectors   : {vectors}"
)

print(
    f"Metadata  : {metadata_count}"
)

print(
    f"Dimension : {dimension}"
)

if vectors != metadata_count:

    print(
        "WARNING: FAISS vector count and "
        "metadata record count do not match."
    )

print(
    "=" * 70
)


# ==========================================================
# Helper: Get Vector/Metadata Counts
# ==========================================================

def get_database_counts():
    """
    Return the current FAISS and metadata counts.
    """

    vector_count = (
        vector_store.total_vectors()
    )

    metadata_count = len(
        metadata_store.metadata
    )

    return (
        vector_count,
        metadata_count,
    )


# ==========================================================
# Helper: Validate Alignment
# ==========================================================

def validate_alignment():
    """
    Ensure FAISS and metadata contain exactly the same
    number of records.
    """

    vector_count, metadata_count = (
        get_database_counts()
    )

    if vector_count != metadata_count:

        raise HTTPException(
            status_code=409,
            detail={
                "message": (
                    "FAISS vector count and metadata "
                    "record count do not match."
                ),
                "faiss_vectors": vector_count,
                "metadata_records": metadata_count,
                "action": (
                    "Repair the FAISS index before "
                    "creating new embeddings."
                ),
            },
        )

    return True


# ==========================================================
# Helper: Find Uploaded File
# ==========================================================

def find_uploaded_file(
    filename: str,
) -> Path | None:
    """
    Search the uploads directory for a document.

    The project stores uploaded files in extension-specific
    folders, therefore the complete uploads directory is
    searched recursively.
    """

    if not UPLOAD_DIR.exists():

        return None

    direct_path = (
        UPLOAD_DIR
        / filename
    )

    if direct_path.exists():

        return direct_path


    # ------------------------------------------------------
    # Recursive search
    # ------------------------------------------------------

    for file_path in UPLOAD_DIR.rglob(
        filename
    ):

        if file_path.is_file():

            return file_path


    return None


# ==========================================================
# GET EMBEDDING STATUS
# ==========================================================

@router.get(
    "/status"
)
def embedding_status():
    """
    Return current FAISS and metadata status.
    """

    vector_count, metadata_count = (
        get_database_counts()
    )

    return {
        "success": True,
        "faiss_vectors": vector_count,
        "metadata_records": metadata_count,
        "embedding_dimension": dimension,
        "aligned": (
            vector_count
            == metadata_count
        ),
        "faiss_path": str(
            FAISS_PATH
        ),
        "metadata_path": str(
            METADATA_PATH
        ),
    }


# ==========================================================
# CREATE EMBEDDINGS
# ==========================================================

@router.post(
    "/create"
)
def create_embeddings(
    filename: str,
    db: Session = Depends(
        get_db
    ),
):
    """
    Generate embeddings for an uploaded document.

    Processing flow
    ---------------

    Uploaded document
          ↓
    process_document_file()
          ↓
    Extract text
          ↓
    Clean text
          ↓
    Generate chunks
          ↓
    Generate embeddings
          ↓
    Add vectors to FAISS
          ↓
    Add metadata
          ↓
    Save FAISS
          ↓
    Save metadata
    """

    # ======================================================
    # Validate Filename
    # ======================================================

    if not filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )


    # ======================================================
    # Locate Uploaded File
    # ======================================================

    file_path = (
        find_uploaded_file(
            filename
        )
    )

    if file_path is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Uploaded document not found: "
                f"{filename}"
            ),
        )


    # ======================================================
    # Check Existing Document
    # ======================================================

    try:

        existing_records = (
            metadata_store
            .get_by_document(
                filename
            )
        )

    except Exception:

        existing_records = []


    if existing_records:

        raise HTTPException(
            status_code=409,
            detail={
                "message": (
                    "Document has already been "
                    "indexed."
                ),
                "filename": filename,
                "existing_chunks": len(
                    existing_records
                ),
            },
        )


    # ======================================================
    # Validate Current Database Alignment
    # ======================================================
    #
    # This is extremely important.
    #
    # If:
    #
    #     FAISS = 31
    #     Metadata = 19
    #
    # we MUST NOT add another document.
    #
    # Otherwise the mismatch becomes even worse.
    #
    # ======================================================

    vectors_before, metadata_before = (
        get_database_counts()
    )

    if (
        vectors_before
        != metadata_before
    ):

        raise HTTPException(
            status_code=409,
            detail={
                "message": (
                    "Vector database is inconsistent. "
                    "New embeddings cannot be created."
                ),
                "faiss_vectors": vectors_before,
                "metadata_records": metadata_before,
                "required": (
                    "FAISS vector count must equal "
                    "metadata record count."
                ),
            },
        )


    # ======================================================
    # Process Document
    # ======================================================
    #
    # IMPORTANT:
    #
    # document_processing_service.py contains the
    # module-level function:
    #
    #     process_document_file()
    #
    # It does NOT contain:
    #
    #     DocumentProcessingService
    #
    # ======================================================

    try:

        processed = (
            process_document_file(
                file_path=file_path,
                filename=filename,
                db=db,
            )
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Document processing failed: "
                f"{error}"
            ),
        )


    # ======================================================
    # Validate Processing Result
    # ======================================================

    if not isinstance(
        processed,
        dict
    ):

        raise HTTPException(
            status_code=500,
            detail=(
                "Document processing returned "
                "an invalid result."
            ),
        )


    # ======================================================
    # Extract Chunks
    # ======================================================

    chunks = processed.get(
        "chunks",
        []
    )

    if not chunks:

        raise HTTPException(
            status_code=400,
            detail=(
                "No chunks were generated "
                f"for {filename}"
            ),
        )


    # ======================================================
    # Extract Chunk Text
    # ======================================================

    chunk_texts = []

    for chunk in chunks:

        if isinstance(
            chunk,
            dict
        ):

            chunk_text = chunk.get(
                "text",
                ""
            )

        else:

            chunk_text = str(
                chunk
            )

        chunk_text = (
            chunk_text
            .strip()
        )

        if chunk_text:

            chunk_texts.append(
                chunk_text
            )


    # ======================================================
    # Validate Chunk Text
    # ======================================================

    if not chunk_texts:

        raise HTTPException(
            status_code=400,
            detail=(
                "Generated chunks contain "
                "no usable text."
            ),
        )


    # ======================================================
    # Display Processing Information
    # ======================================================

    print()
    print("=" * 70)
    print("EMBEDDING CREATION")
    print("=" * 70)

    print(
        f"Document : {filename}"
    )

    print(
        f"Chunks   : {len(chunk_texts)}"
    )

    print(
        f"FAISS before : {vectors_before}"
    )

    print(
        f"Metadata before : {metadata_before}"
    )


    # ======================================================
    # Generate Embeddings
    # ======================================================

    try:

        embeddings = (
            EmbeddingService
            .generate_embeddings(
                chunk_texts
            )
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Embedding generation failed: "
                f"{error}"
            ),
        )


    # ======================================================
    # Convert to NumPy Float32
    # ======================================================

    embeddings = np.asarray(
        embeddings,
        dtype=np.float32
    )


    # ======================================================
    # Validate Embedding Shape
    # ======================================================

    if embeddings.ndim != 2:

        raise HTTPException(
            status_code=500,
            detail=(
                "Generated embeddings have "
                "an invalid shape: "
                f"{embeddings.shape}"
            ),
        )


    # ======================================================
    # Validate Embedding Count
    # ======================================================

    if (
        embeddings.shape[0]
        != len(chunk_texts)
    ):

        raise HTTPException(
            status_code=500,
            detail={
                "message": (
                    "Embedding count does not "
                    "match chunk count."
                ),
                "embeddings": int(
                    embeddings.shape[0]
                ),
                "chunks": len(
                    chunk_texts
                ),
            },
        )


    # ======================================================
    # Validate Embedding Dimension
    # ======================================================

    embedding_dimension = (
        embeddings.shape[1]
    )

    if (
        embedding_dimension
        != dimension
    ):

        raise HTTPException(
            status_code=500,
            detail={
                "message": (
                    "Embedding dimension does "
                    "not match FAISS dimension."
                ),
                "embedding_dimension":
                    int(
                        embedding_dimension
                    ),
                "faiss_dimension":
                    dimension,
            },
        )


    # ======================================================
    # Record Starting Vector ID
    # ======================================================

    starting_vector_id = (
        vectors_before
    )


    # ======================================================
    # Add Embeddings to FAISS
    # ======================================================

    try:

        vector_store.add_embeddings(
            embeddings
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to add embeddings "
                f"to FAISS: {error}"
            ),
        )


    # ======================================================
    # Verify FAISS Addition
    # ======================================================

    vectors_after_add = (
        vector_store.total_vectors()
    )

    expected_vectors = (
        vectors_before
        + len(chunk_texts)
    )

    if (
        vectors_after_add
        != expected_vectors
    ):

        raise HTTPException(
            status_code=500,
            detail={
                "message": (
                    "FAISS vector count after "
                    "insertion is incorrect."
                ),
                "before": vectors_before,
                "expected": expected_vectors,
                "actual": vectors_after_add,
            },
        )


    # ======================================================
    # Build Metadata Records
    # ======================================================

    metadata_records = []

    for index, chunk in enumerate(
        chunks
    ):

        if isinstance(
            chunk,
            dict
        ):

            text = chunk.get(
                "text",
                ""
            )

            text = (
                text
                .strip()
            )

            if not text:

                continue

            metadata_record = {
                "vector_id": (
                    starting_vector_id
                    + len(
                        metadata_records
                    )
                ),
                "chunk_id": chunk.get(
                    "chunk_id",
                    (
                        starting_vector_id
                        + len(
                            metadata_records
                        )
                    ),
                ),
                "document": chunk.get(
                    "document",
                    filename,
                ),
                "source": chunk.get(
                    "source",
                    filename,
                ),
                "page": chunk.get(
                    "page",
                    1,
                ),
                "text": text,
            }

        else:

            text = str(
                chunk
            ).strip()

            if not text:

                continue

            metadata_record = {
                "vector_id": (
                    starting_vector_id
                    + len(
                        metadata_records
                    )
                ),
                "chunk_id": (
                    starting_vector_id
                    + len(
                        metadata_records
                    )
                ),
                "document": filename,
                "source": filename,
                "page": 1,
                "text": text,
            }

        metadata_records.append(
            metadata_record
        )


    # ======================================================
    # Validate Metadata Count
    # ======================================================

    if (
        len(metadata_records)
        != len(chunk_texts)
    ):

        raise HTTPException(
            status_code=500,
            detail={
                "message": (
                    "Metadata record count does "
                    "not match embedding count."
                ),
                "metadata": len(
                    metadata_records
                ),
                "embeddings": len(
                    chunk_texts
                ),
            },
        )


    # ======================================================
    # Add Metadata
    # ======================================================

    try:

        metadata_store.add_many(
            metadata_records
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to store metadata: "
                f"{error}"
            ),
        )


    # ======================================================
    # Validate FAISS/Metadata Alignment
    # ======================================================

    vectors_after_metadata = (
        vector_store.total_vectors()
    )

    metadata_after = len(
        metadata_store.metadata
    )

    if (
        vectors_after_metadata
        != metadata_after
    ):

        raise HTTPException(
            status_code=500,
            detail={
                "message": (
                    "FAISS and metadata are "
                    "not aligned after indexing."
                ),
                "faiss_vectors":
                    vectors_after_metadata,
                "metadata_records":
                    metadata_after,
            },
        )


    # ======================================================
    # Save FAISS
    # ======================================================

    try:

        vector_store.save()

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to save FAISS index: "
                f"{error}"
            ),
        )


    # ======================================================
    # Save Metadata
    # ======================================================

    try:

        metadata_store.save()

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to save metadata: "
                f"{error}"
            ),
        )


    # ======================================================
    # Final Verification
    # ======================================================

    final_vectors = (
        vector_store.total_vectors()
    )

    final_metadata = len(
        metadata_store.metadata
    )

    aligned = (
        final_vectors
        == final_metadata
    )


    # ======================================================
    # Final Output
    # ======================================================

    print()
    print("=" * 70)
    print("EMBEDDING CREATION COMPLETE")
    print("=" * 70)

    print(
        f"Document       : {filename}"
    )

    print(
        f"Chunks         : {len(chunk_texts)}"
    )

    print(
        f"Vectors before : {vectors_before}"
    )

    print(
        f"Vectors after  : {final_vectors}"
    )

    print(
        f"Metadata       : {final_metadata}"
    )

    print(
        f"Aligned        : {aligned}"
    )

    print(
        "=" * 70
    )


    # ======================================================
    # Return Response
    # ======================================================

    return {
        "success": True,
        "message": (
            "Embeddings created successfully."
        ),
        "filename": filename,
        "chunks": len(
            chunk_texts
        ),
        "embeddings": len(
            embeddings
        ),
        "embedding_dimension": dimension,
        "faiss_vectors_before":
            vectors_before,
        "faiss_vectors_after":
            final_vectors,
        "metadata_records":
            final_metadata,
        "aligned": aligned,
        "analytics_id":
            processed.get(
                "analytics_id"
            ),
    }


# ==========================================================
# SEARCH EMBEDDINGS
# ==========================================================

@router.post(
    "/search"
)
def search_embeddings(
    query: str,
    top_k: int = 5,
):
    """
    Search the FAISS vector database.
    """

    # ======================================================
    # Validate Query
    # ======================================================

    if not query or not query.strip():

        raise HTTPException(
            status_code=400,
            detail="Query is required.",
        )


    # ======================================================
    # Validate Top K
    # ======================================================

    if top_k <= 0:

        raise HTTPException(
            status_code=400,
            detail=(
                "top_k must be greater than zero."
            ),
        )


    # ======================================================
    # Validate Alignment
    # ======================================================

    vector_count, metadata_count = (
        get_database_counts()
    )

    if (
        vector_count
        != metadata_count
    ):

        raise HTTPException(
            status_code=409,
            detail={
                "message": (
                    "FAISS vector count and "
                    "metadata count do not match."
                ),
                "faiss_vectors":
                    vector_count,
                "metadata_records":
                    metadata_count,
            },
        )


    # ======================================================
    # Validate Empty Database
    # ======================================================

    if vector_count == 0:

        return {
            "success": True,
            "query": query,
            "top_k": top_k,
            "results": [],
            "total_results": 0,
        }


    # ======================================================
    # Generate Query Embedding
    # ======================================================

    try:

        query_embedding = (
            EmbeddingService
            .generate_embedding(
                query
            )
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Query embedding generation failed: "
                f"{error}"
            ),
        )


    # ======================================================
    # Search FAISS
    # ======================================================

    try:

        results = (
            vector_store.search(
                query_embedding,
                top_k
            )
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "FAISS search failed: "
                f"{error}"
            ),
        )


    # ======================================================
    # Map Results to Metadata
    # ======================================================

    search_results = []

    for result in results:

        vector_id = result.get(
            "vector_id"
        )

        distance = result.get(
            "distance"
        )


        metadata = (
            metadata_store.get(
                vector_id
            )
        )

        if metadata is None:

            continue


        search_results.append(
            {
                "vector_id": vector_id,
                "chunk_id": metadata.get(
                    "chunk_id"
                ),
                "document": metadata.get(
                    "document"
                ),
                "source": metadata.get(
                    "source",
                    metadata.get(
                        "document"
                    )
                ),
                "page": metadata.get(
                    "page",
                    1
                ),
                "text": metadata.get(
                    "text",
                    ""
                ),
                "distance": distance,
            }
        )


    # ======================================================
    # Return Results
    # ======================================================

    return {
        "success": True,
        "query": query,
        "top_k": top_k,
        "results": search_results,
        "total_results": len(
            search_results
        ),
    }