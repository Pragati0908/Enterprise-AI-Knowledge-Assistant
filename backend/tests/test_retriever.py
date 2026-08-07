from app.services.vector_store import VectorStore
from app.services.metadata_store import MetadataStore
from app.services.retriever import Retriever


# ==========================================================
# Load FAISS Index
# ==========================================================

vector_store = VectorStore(
    dimension=384
)

# Uses default:
# backend/vector_db/faiss.index
vector_store.load()


# ==========================================================
# Load Metadata
# ==========================================================

metadata_store = MetadataStore()

# Uses default:
# backend/vector_db/metadata.json
metadata_store.load()


# ==========================================================
# Create Retriever
# ==========================================================

retriever = Retriever(
    vector_store,
    metadata_store
)


# ==========================================================
# Test Queries
# ==========================================================

queries = [

    "Artificial Intelligence",

    "Machine Learning",

    "Deep Learning",

    "Natural Language Processing"

]


# ==========================================================
# Run Tests
# ==========================================================

for query in queries:

    print()
    print("=" * 70)
    print(f"Query : {query}")
    print("=" * 70)

    results = retriever.retrieve(
        query,
        top_k=3
    )

    if not results:

        print("\nNo matching chunks found.\n")
        continue

    for result in results:

        print()

        print(f"Chunk : {result['chunk_id']}")
        print(f"Document : {result['document']}")
        print(f"Page : {result['page']}")
        print(f"Distance : {result['distance']:.4f}")

        print()
        print(result["text"][:250])

        print("-" * 70)