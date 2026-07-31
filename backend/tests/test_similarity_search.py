from app.services.parsers.pdf_parser import PDFParser
from app.services.chunker import TextChunker
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.metadata_store import MetadataStore


# ==========================================================
# STEP 1 : Extract Text from PDF
# ==========================================================

print()
print("=" * 70)
print("STEP 1 : PDF EXTRACTION")
print("=" * 70)

text = PDFParser.extract_text(

    "tests/sample_chunk_testing.pdf"

)

print(f"\nTotal Characters : {len(text)}")


# ==========================================================
# STEP 2 : Generate Chunks
# ==========================================================

print()
print("=" * 70)
print("STEP 2 : CHUNK GENERATION")
print("=" * 70)

chunks = TextChunker.chunk_text(

    text=text,

    source="sample_chunk_testing.pdf",

    chunk_size=800,

    overlap=150

)

print(f"\nTotal Chunks : {len(chunks)}")


# ==========================================================
# STEP 3 : Prepare Chunk Texts
# ==========================================================

chunk_texts = [

    chunk["text"]

    for chunk in chunks

]


# ==========================================================
# STEP 4 : Generate Embeddings
# ==========================================================

print()
print("=" * 70)
print("STEP 3 : GENERATE EMBEDDINGS")
print("=" * 70)

embeddings = EmbeddingService.generate_embeddings(

    chunk_texts

)

print(f"\nEmbeddings Generated : {len(embeddings)}")

dimension = len(

    embeddings[0]

)

print(f"Embedding Dimension : {dimension}")


# ==========================================================
# STEP 5 : Create Vector Store
# ==========================================================

print()
print("=" * 70)
print("STEP 4 : VECTOR STORE")
print("=" * 70)

vector_store = VectorStore(

    dimension

)

vector_store.add_embeddings(

    embeddings

)

print(

    f"\nVectors Stored : {vector_store.total_vectors()}"

)


# ==========================================================
# STEP 6 : Create Metadata Store
# ==========================================================

print()
print("=" * 70)
print("STEP 5 : METADATA STORE")
print("=" * 70)

metadata_store = MetadataStore()

metadata = []

for chunk in chunks:

    metadata.append(

        {

            "chunk_id": chunk["chunk_id"],

            "document": "sample_chunk_testing.pdf",

            "page": 1,

            "source": "sample_chunk_testing.pdf",

            "start_index": chunk["start_index"],

            "end_index": chunk["end_index"],

            "text": chunk["text"]

        }

    )

metadata_store.add_many(

    metadata

)

print(

    f"\nMetadata Records : {metadata_store.total()}"

)


# ==========================================================
# STEP 7 : Similarity Search
# ==========================================================

print()
print("=" * 70)
print("STEP 6 : SIMILARITY SEARCH")
print("=" * 70)

query = "Artificial Intelligence"

print(f"\nQuery : {query}")

query_embedding = EmbeddingService.generate_embedding(

    query

)

results = vector_store.search(

    query_embedding,

    k=3

)


# ==========================================================
# STEP 8 : Display Results
# ==========================================================

print()
print("=" * 70)
print("SEARCH RESULTS")
print("=" * 70)

for rank, result in enumerate(

    results,

    start=1

):

    item = metadata_store.get(

        result["vector_id"]

    )

    print()

    print(f"Rank : {rank}")

    print(f"Vector ID : {result['vector_id']}")

    print(f"Distance : {result['distance']:.6f}")

    print(f"Chunk ID : {item['chunk_id']}")

    print(f"Document : {item['document']}")

    print(f"Page : {item['page']}")

    print(f"Source : {item['source']}")

    print(f"Start Index : {item['start_index']}")

    print(f"End Index : {item['end_index']}")

    print(f"Characters : {len(item['text'])}")

    print()

    print("Chunk Preview:\n")

    print(

        item["text"][:300]

    )

    print()

    print("-" * 70)


print()
print("=" * 70)
print("TEST COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\n✓ PDF parsed successfully.")
print("✓ Text chunked successfully.")
print("✓ Embeddings generated.")
print("✓ Embeddings stored in FAISS.")
print("✓ Metadata mapped successfully.")
print("✓ Similarity search completed.")