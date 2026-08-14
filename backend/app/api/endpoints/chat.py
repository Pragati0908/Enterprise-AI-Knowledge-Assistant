from fastapi import APIRouter
from pydantic import BaseModel

from app.services.retriever import Retriever
from app.services.prompt_builder import PromptBuilder
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService


# ==========================================================
# Router
# ==========================================================

router = APIRouter(
    prefix="/chat",
    tags=["RAG Chat"]
)


# ==========================================================
# Request Models
# ==========================================================

class ChatRequest(BaseModel):
    question: str
    top_k: int = 3


class SummaryRequest(BaseModel):
    context: str


# ==========================================================
# Initialize Services (Singleton)
# ==========================================================

from app.services.vector_store import VectorStore
from app.services.metadata_store import MetadataStore

# Load FAISS Vector Store
vector_store = VectorStore()

if vector_store.exists():
    vector_store.load()
else:
    print("No FAISS index found. Starting with an empty vector database.")

# Load Metadata Store
metadata_store = MetadataStore()
metadata_store.load()

print(f"Vectors Loaded  : {vector_store.total_vectors()}")
print(f"Metadata Loaded : {metadata_store.total()}")

# Create Retriever
retriever = Retriever(
    vector_store=vector_store,
    metadata_store=metadata_store
)

# Other Services
prompt_builder = PromptBuilder()

llm_service = LLMService()

rag_service = RAGService(
    retriever=retriever,
    prompt_builder=prompt_builder,
    llm_service=llm_service
)


# ==========================================================
# Status Endpoint
# ==========================================================

@router.get("/status")
def chat_status():

    return {

        "status": "running",

        "service": "Enterprise AI Chat API",

        "rag": "ready",

        "retriever": "initialized",

        "prompt_builder": "initialized",

        "llm_model": llm_service.MODEL

    }


# ==========================================================
# Ask Question
# ==========================================================

@router.post("/ask")
def ask_question(request: ChatRequest):

    """
    Ask a question using the complete RAG pipeline.

    Flow

    User Question
            ↓
       Retriever
            ↓
     Prompt Builder
            ↓
         LLM
            ↓
        Final Answer
    """

    result = rag_service.ask(

        question=request.question,

        top_k=request.top_k

    )

    return result


# ==========================================================
# Summarize Text
# ==========================================================

@router.post("/summary")
def summarize_document(request: SummaryRequest):

    """
    Summarize supplied text using the LLM.
    """

    result = rag_service.summarize(

        context=request.context

    )

    return result


# ==========================================================
# Generic Prompt (Optional)
# ==========================================================

@router.post("/generate")
def generate(prompt: str):

    """
    Direct prompt execution.

    Mainly useful for debugging/testing.
    """

    result = rag_service.generate(

        prompt=prompt

    )

    return result