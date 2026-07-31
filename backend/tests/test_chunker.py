from app.services.parsers.pdf_parser import PDFParser
from app.services.chunker import TextChunker


# ==========================================================
# Extract Text from PDF
# ==========================================================

text = PDFParser.extract_text(

    "tests/sample_chunk_testing.pdf"

)

print()

print("=" * 60)
print("PDF EXTRACTION")
print("=" * 60)

print(

    "Type:",

    type(text)

)

print(

    "Length:",

    len(text)

)

print(

    "\nFirst 300 Characters:\n"

)

print(

    text[:300]

)


# ==========================================================
# Generate Chunks
# ==========================================================

chunks = TextChunker.chunk_text(

    text=text,

    source="sample_chunk_testing.pdf",

    chunk_size=800,

    overlap=150

)

print()

print("=" * 60)
print("CHUNK GENERATION")
print("=" * 60)

print(

    f"\nTotal Chunks : {len(chunks)}"

)

for chunk in chunks:

    print()

    print(

        f"Chunk ID : {chunk['chunk_id']}"

    )

    print(

        f"Source : {chunk['source']}"

    )

    print(

        f"Start Index : {chunk['start_index']}"

    )

    print(

        f"End Index : {chunk['end_index']}"

    )

    print(

        f"Chunk Length : {chunk['chunk_length']}"

    )

    print(

        "\nText:\n"

    )

    print(

        chunk['text']

    )

    print(

        "-" * 60

    )


# ==========================================================
# Prepare Chunk Texts for Embedding Service
# ==========================================================

chunk_texts = [

    chunk["text"]

    for chunk in chunks

]

print()

print("=" * 60)
print("PREPARE FOR EMBEDDING SERVICE")
print("=" * 60)

print(

    f"\nTotal Chunk Texts : {len(chunk_texts)}"

)

print()

for index, chunk_text in enumerate(

    chunk_texts,

    start=1

):

    print(

        f"Chunk {index}"

    )

    print(

        f"Characters : {len(chunk_text)}"

    )

    print(

        "Preview:"

    )

    print(

        chunk_text[:100]

    )

    print(

        "-" * 60

    )


print()

print("=" * 60)
print("READY FOR EMBEDDING SERVICE")
print("=" * 60)