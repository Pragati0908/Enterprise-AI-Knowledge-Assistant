from app.services.embedding_service import EmbeddingService
from app.services.parsers.pdf_parser import PDFParser
from app.services.chunker import TextChunker


# ==========================================================
# TEST 1 : SINGLE EMBEDDING
# ==========================================================

print("\n")
print("=" * 70)
print("TEST 1 : SINGLE EMBEDDING")
print("=" * 70)

text = (
    "Artificial Intelligence is transforming industries."
)

embedding = EmbeddingService.generate_embedding(
    text
)

print("\nEmbedding Generated Successfully")

print(
    f"\nEmbedding Dimension : {len(embedding)}"
)

print("\nFirst 10 Values:")

print(
    embedding[:10]
)


# ==========================================================
# TEST 2 : MULTIPLE EMBEDDINGS
# ==========================================================

print("\n")
print("=" * 70)
print("TEST 2 : MULTIPLE EMBEDDINGS")
print("=" * 70)

texts = [

    "Artificial Intelligence is transforming industries.",

    "Machine Learning helps computers learn from data.",

    "Natural Language Processing understands human language.",

    "Deep Learning uses neural networks for complex tasks."

]

embeddings = EmbeddingService.generate_embeddings(
    texts
)

print(
    f"\nTotal Texts : {len(texts)}"
)

print(
    f"Total Embeddings : {len(embeddings)}"
)

print(
    f"Embedding Dimension : {len(embeddings[0])}"
)

print("\nSummary:\n")

for index, (text, embedding) in enumerate(

    zip(texts, embeddings),

    start=1

):

    print(
        f"Text {index}"
    )

    print(
        text
    )

    print(
        f"\nEmbedding Dimension : {len(embedding)}"
    )

    print(
        f"First 5 Values : {embedding[:5]}"
    )

    print("-" * 70)


# ==========================================================
# TEST 3 : GENERATE EMBEDDINGS FROM PDF CHUNKS
# ==========================================================

print("\n")
print("=" * 70)
print("TEST 3 : PDF CHUNKS TO EMBEDDINGS")
print("=" * 70)

text = PDFParser.extract_text(

    "tests/sample_chunk_testing.pdf"

)

chunks = TextChunker.chunk_text(

    text=text,

    source="sample_chunk_testing.pdf",

    chunk_size=800,

    overlap=150

)

chunk_texts = [

    chunk["text"]

    for chunk in chunks

]

chunk_embeddings = EmbeddingService.generate_embeddings(

    chunk_texts

)

print()

print(
    f"Total Chunks : {len(chunks)}"
)

print(
    f"Total Embeddings : {len(chunk_embeddings)}"
)

print(
    f"Embedding Dimension : {len(chunk_embeddings[0])}"
)

print("\nChunk Embedding Summary\n")

for chunk, embedding in zip(

    chunks,

    chunk_embeddings

):

    print(
        f"Chunk ID : {chunk['chunk_id']}"
    )

    print(
        f"Source : {chunk['source']}"
    )

    print(
        f"Characters : {chunk['chunk_length']}"
    )

    print(
        "Chunk Preview:"
    )

    preview = chunk["text"][:120]

    if " " in preview:
       preview = preview.rsplit(" ", 1)[0]

    print(preview + " ...")

    print()

    print(
        f"Embedding Dimension : {len(embedding)}"
    )

    print(
        f"First 5 Values : {embedding[:5]}"
    )

    print("-" * 70)


print("\n")
print("=" * 70)
print("EMBEDDING COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    "\n✓ Single embedding generated."
)

print(
    "✓ Multiple embeddings generated."
)

print(
    "✓ PDF converted into chunks."
)

print(
    "✓ Chunks converted into embeddings."
)

print(
    "✓ Ready for FAISS Vector Database."
)