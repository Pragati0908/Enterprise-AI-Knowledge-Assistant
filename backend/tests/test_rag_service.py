from app.services.vector_store import VectorStore
from app.services.metadata_store import MetadataStore
from app.services.retriever import Retriever
from app.services.prompt_builder import PromptBuilder
from app.services.llm_service import LLMService
from app.services.rag_service import RAGService


# ==========================================================
# Load Vector Database
# ==========================================================

vector_store = VectorStore(
    dimension=384
)

vector_store.load()

print("\nFAISS loaded successfully.")
print(f"Vectors : {vector_store.total_vectors()}")


# ==========================================================
# Load Metadata
# ==========================================================

metadata_store = MetadataStore()

metadata_store.load()

print("Metadata loaded successfully.")
print(f"Records : {metadata_store.total()}")


# ==========================================================
# Create Services
# ==========================================================

retriever = Retriever(

    vector_store,

    metadata_store

)

prompt_builder = PromptBuilder()

llm_service = LLMService()

rag_service = RAGService(

    retriever,

    prompt_builder,

    llm_service

)


# ==========================================================
# Test Questions
# ==========================================================

questions = [

    "What is Artificial Intelligence?",

    "Explain Machine Learning.",

    "What is OCR?",

    "Explain Chunking.",

    "What is Metadata?",

    "How does Retrieval-Augmented Generation work?",

    "What is Deep Learning?",

    "What is Blockchain?"

]


# ==========================================================
# Execute Tests
# ==========================================================

for question in questions:

    print("\n")
    print("=" * 80)
    print(f"QUESTION : {question}")
    print("=" * 80)

    response = rag_service.ask(

        question=question,

        top_k=3

    )

    if not response["success"]:

        print("\nFAILED")
        print("-" * 80)

        if response.get("error"):

            print(response["error"])

        else:

            print(response["answer"])

        continue

    print("\nANSWER")
    print("-" * 80)
    print(response["answer"])

    print("\nCHUNKS USED")
    print("-" * 80)
    print(response["chunks_used"])

    print("\nSOURCE DOCUMENTS")
    print("-" * 80)

    for source in response["sources"]:

        print(

            f"Chunk ID : {source['chunk_id']}"

        )

        print(

            f"Document : {source['document']}"

        )

        print(

            f"Page     : {source['page']}"

        )

        print(

            f"Distance : {source['distance']:.4f}"

        )

        print("-" * 40)

print("\n")
print("=" * 80)
print("RAG PIPELINE TEST COMPLETED SUCCESSFULLY")
print("=" * 80)