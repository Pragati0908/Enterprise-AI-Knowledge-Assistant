from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.metadata_store import MetadataStore
from app.services.parsers.document_parser import DocumentParser
from app.services.text_cleaner import TextCleaner
from app.services.chunker import TextChunker


router = APIRouter(
    prefix="/embeddings",
    tags=["Embeddings"]
)

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[4]

UPLOAD_DIR = PROJECT_ROOT / "backend" / "uploads"

VECTOR_DB = PROJECT_ROOT / "backend" / "vector_db"

VECTOR_DB.mkdir(
    parents=True,
    exist_ok=True
)

FAISS_PATH = VECTOR_DB / "faiss.index"

# ==========================================================
# Request Models
# ==========================================================

class IndexRequest(BaseModel):
    filename: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


# ==========================================================
# Stores
# ==========================================================

vector_store = None
metadata_store = MetadataStore()

# ==========================================================
# Load Existing Database
# ==========================================================

try:

    dimension = len(
        EmbeddingService.generate_embedding("test")
    )

    vector_store = VectorStore(dimension)

    if FAISS_PATH.exists():

        vector_store.load()

    metadata_store.load()

    print("\nExisting Vector Database Loaded")
    print(f"Vectors  : {vector_store.total_vectors()}")
    print(f"Metadata : {metadata_store.total()}\n")

except Exception as e:

    print(f"\nNo existing vector database found ({e})")
    print("A new database will be created after indexing.\n")

# ==========================================================
# Status
# ==========================================================

@router.get("/status")
def embedding_status():

    return {

        "status": "running",

        "service": "Embedding API",

        "vector_database":
            "initialized"
            if vector_store and vector_store.total_vectors() > 0
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
def create_embeddings(request: IndexRequest):

    global vector_store

    # ======================================================
    # Locate uploaded document
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
            UPLOAD_DIR /
            extension /
            request.filename
        )

        if candidate.exists():

            file_path = candidate
            break

    if file_path is None:

        raise HTTPException(
            status_code=404,
            detail=f"Document not found : {request.filename}"
        )

    # ======================================================
    # Extract Text
    # ======================================================

    try:

        text = DocumentParser.parse_document(
            str(file_path)
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    # ======================================================
    # Clean Text
    # ======================================================

    cleaned_text = TextCleaner.clean_text(
        text
    )

    # ======================================================
    # Chunk Text
    # ======================================================

    chunks = TextChunker.chunk_text(
        text=cleaned_text,
        source=request.filename,
        chunk_size=800,
        overlap=150
    )

    if len(chunks) == 0:

        raise HTTPException(
            status_code=400,
            detail="No chunks generated."
        )

    # ======================================================
    # Generate Embeddings
    # ======================================================

    chunk_texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = EmbeddingService.generate_embeddings(
        chunk_texts
    )

    # ======================================================
    # Development Mode
    # Rebuild Database
    # ======================================================

    vector_store = VectorStore(
        len(embeddings[0])
    )

    metadata_store.metadata = []

    # ======================================================
    # Store Embeddings
    # ======================================================

    vector_store.add_embeddings(
        embeddings
    )

    # ======================================================
    # Metadata
    # ======================================================

    metadata = []

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        metadata.append(
            {
                "chunk_id": index,
                "document": request.filename,
                "page": 1,
                "source": request.filename,
                "start_index": chunk["start_index"],
                "end_index": chunk["end_index"],
                "chunk_length": chunk["chunk_length"],
                "text": chunk["text"]
            }
        )

    metadata_store.add_many(
        metadata
    )

    # ======================================================
    # Save Database
    # ======================================================

    vector_store.save()

    metadata_store.save()

    print("\nVector Database Rebuilt Successfully")
    print(f"Vectors  : {vector_store.total_vectors()}")
    print(f"Metadata : {metadata_store.total()}\n")

    return {
        "message": "Document indexed successfully.",
        "document": request.filename,
        "total_chunks": len(chunks),
        "embedding_dimension": len(embeddings[0]),
        "total_vectors": vector_store.total_vectors()
    }

# ==========================================================
# Similarity Search
# ==========================================================

@router.post("/search")
def search_embeddings(request: SearchRequest):

    global vector_store

    if (
        vector_store is None
        or
        vector_store.total_vectors() == 0
    ):

        raise HTTPException(
            status_code=400,
            detail="Vector database is empty."
        )

    query_embedding = EmbeddingService.generate_embedding(
        request.query
    )

    results = vector_store.search(
        query_embedding,
        request.top_k
    )

    output = []

    for result in results:

        metadata = metadata_store.get(
            result["vector_id"]
        )

        if metadata is None:
            continue

        output.append(

            {

                "chunk_id": metadata["chunk_id"],

                "document": metadata["document"],

                "page": metadata["page"],

                "source": metadata["source"],

                "start_index": metadata["start_index"],

                "end_index": metadata["end_index"],

                "chunk_length": metadata["chunk_length"],

                "distance": round(
                    result["distance"],
                    4
                ),

                "text": metadata["text"]

            }

        )

    return {

        "query": request.query,

        "top_k": request.top_k,

        "total_results": len(output),

        "results": output

    }