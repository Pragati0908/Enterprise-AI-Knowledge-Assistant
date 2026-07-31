from pathlib import Path

from fastapi import APIRouter
from fastapi import HTTPException

from pydantic import BaseModel

from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.metadata_store import MetadataStore
from app.services.parsers.pdf_parser import PDFParser
from app.services.text_cleaner import TextCleaner
from app.services.chunker import TextChunker


router = APIRouter(

    prefix="/embeddings",

    tags=["Embeddings"]

)

UPLOAD_DIR = Path("uploads/pdf")

# ==========================================================
# Request Models
# ==========================================================

class IndexRequest(BaseModel):

    filename: str


class SearchRequest(

    BaseModel

):

    query: str

    top_k: int = 5


# ==========================================================
# Temporary In-Memory Stores
# (Week 6 will replace these with persistent loading)
# ==========================================================

vector_store = None

metadata_store = MetadataStore()


# ==========================================================
# GET /embeddings/status
# ==========================================================

@router.get(

    "/status"

)

def embedding_status():

    return {

        "status": "running",

        "service": "Embedding API",

        "vector_database":

        "initialized"

        if vector_store

        else "empty"

    }


# ==========================================================
# POST /embeddings/create
# ==========================================================

@router.post("/create")
def create_embeddings(

    request: IndexRequest

):

    global vector_store

    file_path = UPLOAD_DIR / request.filename

    if not file_path.exists():

        raise HTTPException(

            status_code=404,

            detail="Document not found."

        )

    # ------------------------------------------
    # Step 1 : Extract Text
    # ------------------------------------------

    text = PDFParser.extract_text(

        str(file_path)

    )

    # ------------------------------------------
    # Step 2 : Clean Text
    # ------------------------------------------

    cleaned_text = TextCleaner.clean_text(

        text

    )

    # ------------------------------------------
    # Step 3 : Chunk Text
    # ------------------------------------------

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

    # ------------------------------------------
    # Step 4 : Generate Embeddings
    # ------------------------------------------

    chunk_texts = [

        chunk["text"]

        for chunk in chunks

    ]

    embeddings = EmbeddingService.generate_embeddings(

        chunk_texts

    )

    # ------------------------------------------
    # Step 5 : Initialize FAISS
    # ------------------------------------------

    if vector_store is None:

        vector_store = VectorStore(

            len(

                embeddings[0]

            )

        )
    vector_store.add_embeddings(
        embeddings
    )

    metadata = []

    current_id = metadata_store.total()

    for index, chunk in enumerate(
        chunks,
        start=1
    ):

        metadata.append(

            {
                "chunk_id": current_id + index,

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

    vector_store.save(
        "backend/vector_db/faiss.index"
    )

    metadata_store.save(
        "backend/vector_db/metadata.json"
    )

    return {

        "message": "Document indexed successfully.",

        "document": request.filename,

        "total_chunks": len(chunks),

        "embedding_dimension": len(embeddings[0]),

        "total_vectors": vector_store.total_vectors()

    }


# ==========================================================
# POST /embeddings/search
# ==========================================================

@router.post(

    "/search"

)

def search_embeddings(

    request: SearchRequest

):

    if vector_store is None:

        raise HTTPException(

            status_code=400,

            detail="Vector database is empty."

        )

    query_embedding = (

        EmbeddingService.generate_embedding(

            request.query

        )

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

        # Skip invalid metadata
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